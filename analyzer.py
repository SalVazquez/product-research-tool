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
            'total_supporters': sum(s.get('account_supporters_count', 0) for s in search_results),
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
                themes[theme_name]['supporters'] += suggestion.get('account_supporters_count', 0)
                themes[theme_name]['suggestions'].append({
                    'id': suggestion.get('id'),
                    'title': suggestion.get('title'),
                    'url': suggestion.get('admin_url')  # Use admin_url from API
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
        """Calculate customer impact metrics from UserVoice custom view fields"""

        # Aggregate ARR data from all suggestions
        # UserVoice stores this in cv_* fields like cv_1m_arr.revenue, cv_commercial.revenue
        total_arr = 0
        total_customers = 0
        arr_segments = []

        for suggestion in suggestions:
            # Extract ARR from custom view fields
            for key in suggestion.keys():
                if key.startswith('cv_') and key.endswith('.revenue'):
                    segment_name = key.replace('cv_', '').replace('.revenue', '').replace('_', ' ').title()
                    revenue = suggestion.get(key, 0)
                    accounts = suggestion.get(key.replace('.revenue', '.accounts_count'), 0)

                    if revenue > 0:
                        arr_segments.append({
                            'name': segment_name,
                            'arr': revenue,
                            'accounts': accounts,
                            'suggestion_id': suggestion.get('id')
                        })

        # Calculate totals from the top suggestion (most comprehensive)
        if suggestions:
            top_suggestion = suggestions[0]

            # Sum all cv_* revenue fields
            for key in top_suggestion.keys():
                if key.startswith('cv_') and key.endswith('.revenue'):
                    total_arr += top_suggestion.get(key, 0)
                    accounts = top_suggestion.get(key.replace('.revenue', '.accounts_count'), 0)
                    total_customers += accounts

        # Sort segments by ARR
        arr_segments.sort(key=lambda x: x['arr'], reverse=True)

        # Format top segments as "customers"
        top_customers = []
        for segment in arr_segments[:5]:
            top_customers.append({
                'name': f"{segment['name']} ({segment['accounts']} accounts)",
                'arr': segment['arr'],
                'accounts': segment['accounts']
            })

        return {
            'top_customers': top_customers,
            'total_customers': total_customers,
            'total_arr': total_arr
        }

    def _extract_key_quotes(self, suggestions: List[Dict]) -> List[Dict]:
        """Extract key quotes from suggestions"""
        quotes = []

        for suggestion in suggestions[:10]:  # Top 10 suggestions
            # Use the body field from UserVoice API
            body = suggestion.get('body', '').strip()
            title = suggestion.get('title', 'Unknown')
            url = suggestion.get('admin_url', '')
            supporters = suggestion.get('account_supporters_count', 0)

            # Skip if body is too short
            if not body or len(body) < 50:
                continue

            # Get ARR data for this suggestion
            total_arr = 0
            for key in suggestion.keys():
                if key.startswith('cv_') and key.endswith('.revenue'):
                    total_arr += suggestion.get(key, 0)

            quotes.append({
                'text': body[:500] + ('...' if len(body) > 500 else ''),
                'source': title,
                'url': url,
                'supporters': supporters,
                'arr': total_arr
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
        # Import here to avoid circular dependencies
        from web_research import search_and_analyze_competitor

        results = []

        for competitor in self.competitors:
            try:
                analysis = search_and_analyze_competitor(competitor, pain_point)
                results.append(analysis)
            except Exception as e:
                print(f"Error analyzing {competitor}: {str(e)}")
                import traceback
                traceback.print_exc()
                # Return placeholder on error
                results.append({
                    'name': competitor,
                    'has_feature': None,
                    'description': f'Research error: {str(e)}',
                    'pricing': 'Unknown',
                    'limitations': [],
                    'links': [],
                    'notes': 'Error during research'
                })

        return results

