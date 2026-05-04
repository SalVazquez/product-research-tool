"""
Analysis modules for UserVoice feedback and competitive research
"""

import subprocess
import json
import re
from collections import defaultdict
from typing import List, Dict, Any
import os

class UserVoiceAnalyzer:
    """Analyzes UserVoice feedback for a given pain point"""

    def __init__(self):
        self.uservoice_cli_path = os.path.expanduser("~/uservoice-cli/uservoice-cli.py")

    def analyze(self, pain_point: str) -> Dict[str, Any]:
        """
        Analyze UserVoice feedback for the given pain point
        Returns themes, quotes, customer impact metrics
        """
        # Search UserVoice
        search_results = self._search_uservoice(pain_point)

        if not search_results:
            return {
                'total_suggestions': 0,
                'total_supporters': 0,
                'themes': [],
                'top_customers': [],
                'total_arr': 0,
                'key_quotes': []
            }

        # Get detailed info for top suggestions
        detailed_suggestions = self._get_detailed_suggestions(search_results[:10])

        # Analyze and synthesize
        themes = self._extract_themes(detailed_suggestions)
        customer_impact = self._calculate_customer_impact(detailed_suggestions)
        key_quotes = self._extract_key_quotes(detailed_suggestions)

        return {
            'total_suggestions': len(search_results),
            'total_supporters': sum(s.get('supporters', 0) for s in search_results),
            'themes': themes,
            'top_customers': customer_impact['top_customers'],
            'total_arr': customer_impact['total_arr'],
            'total_customers': customer_impact['total_customers'],
            'key_quotes': key_quotes,
            'top_suggestions': detailed_suggestions[:5]  # Top 5 for display
        }

    def _search_uservoice(self, query: str) -> List[Dict]:
        """Execute UserVoice CLI search"""
        try:
            cmd = ['python3', self.uservoice_cli_path, '--json', 'search', query]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                print(f"UserVoice search error: {result.stderr}")
                return []

            data = json.loads(result.stdout)
            return data.get('suggestions', [])

        except Exception as e:
            print(f"Error searching UserVoice: {str(e)}")
            return []

    def _get_detailed_suggestions(self, suggestions: List[Dict]) -> List[Dict]:
        """Get detailed info including feedback for top suggestions"""
        detailed = []

        for suggestion in suggestions:
            suggestion_id = suggestion.get('id')
            if not suggestion_id:
                continue

            # Get detailed suggestion info
            try:
                cmd = ['python3', self.uservoice_cli_path, '--json', 'get', str(suggestion_id)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    detail_data = json.loads(result.stdout)
                    suggestion_detail = detail_data.get('suggestion', suggestion)
                else:
                    suggestion_detail = suggestion

                # Get feedback/supporters
                cmd = ['python3', self.uservoice_cli_path, '--json', 'feedback', str(suggestion_id)]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    feedback_data = json.loads(result.stdout)
                    suggestion_detail['feedback_records'] = feedback_data.get('feedback', [])
                else:
                    suggestion_detail['feedback_records'] = []

                detailed.append(suggestion_detail)

            except Exception as e:
                print(f"Error getting details for suggestion {suggestion_id}: {str(e)}")
                detailed.append(suggestion)

        return detailed

    def _extract_themes(self, suggestions: List[Dict]) -> List[Dict]:
        """Extract common themes from suggestions"""
        themes = defaultdict(lambda: {'count': 0, 'supporters': 0, 'suggestions': []})

        for suggestion in suggestions:
            title = suggestion.get('title', '').lower()
            description = suggestion.get('description', '').lower()

            # Simple keyword-based theme detection
            text = f"{title} {description}"

            # Define theme keywords
            theme_keywords = {
                'Search & Discovery': ['search', 'find', 'discover', 'query', 'filter'],
                'Attachments': ['attachment', 'file', 'document', 'pdf', 'upload'],
                'AI & Automation': ['ai', 'artificial intelligence', 'automat', 'ml', 'machine learning'],
                'Integration': ['integrat', 'api', 'connect', 'sync', 'import', 'export'],
                'User Experience': ['ui', 'ux', 'interface', 'design', 'usability'],
                'Performance': ['speed', 'slow', 'fast', 'performance', 'latency'],
                'Reporting & Analytics': ['report', 'analytics', 'metric', 'dashboard', 'insight']
            }

            matched_themes = []
            for theme_name, keywords in theme_keywords.items():
                if any(keyword in text for keyword in keywords):
                    matched_themes.append(theme_name)

            # If no theme matched, use "Other"
            if not matched_themes:
                matched_themes = ['Other']

            for theme_name in matched_themes:
                themes[theme_name]['count'] += 1
                themes[theme_name]['supporters'] += suggestion.get('supporters', 0)
                themes[theme_name]['suggestions'].append({
                    'id': suggestion.get('id'),
                    'title': suggestion.get('title'),
                    'url': suggestion.get('url')
                })

        # Convert to list and sort by count
        theme_list = [
            {
                'name': name,
                'count': data['count'],
                'supporters': data['supporters'],
                'suggestions': data['suggestions'][:3]  # Top 3 per theme
            }
            for name, data in themes.items()
        ]

        theme_list.sort(key=lambda x: x['count'], reverse=True)
        return theme_list[:5]  # Top 5 themes

    def _calculate_customer_impact(self, suggestions: List[Dict]) -> Dict:
        """Calculate customer impact metrics"""
        customers = {}

        for suggestion in suggestions:
            feedback_records = suggestion.get('feedback_records', [])

            for feedback in feedback_records:
                customer_name = feedback.get('customer_name', 'Unknown')
                account_name = feedback.get('account_name', customer_name)
                mrr = feedback.get('mrr', 0)

                if account_name not in customers:
                    customers[account_name] = {
                        'name': account_name,
                        'mrr': mrr,
                        'arr': mrr * 12 if mrr else 0,
                        'feedback_count': 0
                    }

                customers[account_name]['feedback_count'] += 1

        # Sort by ARR
        customer_list = sorted(customers.values(), key=lambda x: x['arr'], reverse=True)

        return {
            'top_customers': customer_list[:5],  # Top 5 by ARR
            'total_customers': len(customers),
            'total_arr': sum(c['arr'] for c in customers.values())
        }

    def _extract_key_quotes(self, suggestions: List[Dict]) -> List[Dict]:
        """Extract key quotes from suggestions and feedback"""
        quotes = []

        for suggestion in suggestions[:5]:  # Top 5 suggestions
            # Add suggestion description as a quote
            description = suggestion.get('description', '').strip()
            if description and len(description) > 50:
                quotes.append({
                    'text': description[:500] + ('...' if len(description) > 500 else ''),
                    'source': suggestion.get('title', 'Unknown'),
                    'url': suggestion.get('url', ''),
                    'supporters': suggestion.get('supporters', 0)
                })

            # Extract quotes from feedback
            feedback_records = suggestion.get('feedback_records', [])
            for feedback in feedback_records[:3]:  # Top 3 feedback per suggestion
                feedback_text = feedback.get('feedback_text', '').strip()
                if feedback_text and len(feedback_text) > 50:
                    quotes.append({
                        'text': feedback_text[:300] + ('...' if len(feedback_text) > 300 else ''),
                        'source': feedback.get('account_name', 'Customer'),
                        'url': suggestion.get('url', ''),
                        'arr': feedback.get('mrr', 0) * 12
                    })

        return quotes[:10]  # Return top 10 quotes


class CompetitiveAnalyzer:
    """Analyzes competitor solutions for a given pain point"""

    def __init__(self):
        self.competitors = [
            'Intercom',
            'Freshdesk',
            'ServiceNow',
            'Salesforce Service Cloud',
            'HubSpot Service Hub',
            'Jira Service Management',
            'Gorgias',
            'Kustomer'
        ]

    def analyze(self, pain_point: str) -> List[Dict]:
        """
        Research how competitors solve this pain point
        Returns list of competitor analyses
        """
        results = []

        for competitor in self.competitors:
            analysis = self._analyze_competitor(competitor, pain_point)
            results.append(analysis)

        return results

    def _analyze_competitor(self, competitor: str, pain_point: str) -> Dict:
        """Analyze a single competitor's solution"""
        # This is a placeholder - in production, this would do web searches,
        # scrape documentation, etc.

        # For now, return a structure that the frontend can display
        return {
            'name': competitor,
            'has_feature': None,  # True/False/None (unknown)
            'description': 'Research in progress...',
            'pricing': 'TBD',
            'limitations': [],
            'links': [],
            'notes': f'Competitive research for {competitor} will be implemented with web search and documentation analysis.'
        }
