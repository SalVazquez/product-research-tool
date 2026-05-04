"""
Competitive research using web search and documentation analysis
"""

import subprocess
import json
import re
from typing import Dict, List, Optional


class CompetitiveResearcher:
    """Performs competitive research using web searches and documentation"""

    def __init__(self):
        self.competitor_domains = {
            'Intercom': 'intercom.com',
            'Freshdesk': 'freshdesk.com',
            'ServiceNow': 'servicenow.com',
            'Salesforce Service Cloud': 'salesforce.com',
            'HubSpot Service Hub': 'hubspot.com',
            'Jira Service Management': 'atlassian.com',
            'Gorgias': 'gorgias.com',
            'Kustomer': 'kustomer.com'
        }

    def research_competitor(self, competitor: str, pain_point: str) -> Dict:
        """
        Research how a competitor addresses a specific pain point
        Uses web searches and documentation analysis
        """
        print(f"Researching {competitor} for '{pain_point}'...")

        # Build search queries
        queries = self._build_search_queries(competitor, pain_point)

        # Perform searches and analyze results
        findings = []
        for query in queries[:3]:  # Limit to 3 searches per competitor
            result = self._perform_web_search(query)
            if result:
                findings.append(result)

        # Analyze and synthesize findings
        analysis = self._synthesize_findings(competitor, pain_point, findings)

        return analysis

    def _build_search_queries(self, competitor: str, pain_point: str) -> List[str]:
        """Build effective search queries for the competitor and pain point"""
        domain = self.competitor_domains.get(competitor, '')

        queries = [
            f"{competitor} {pain_point} feature documentation",
            f"{competitor} {pain_point} how to",
            f"site:{domain} {pain_point}",
            f"{competitor} {pain_point} pricing",
            f"{competitor} vs zendesk {pain_point}"
        ]

        return queries

    def _perform_web_search(self, query: str) -> Optional[Dict]:
        """
        Perform a web search using DuckDuckGo (no API key needed)
        Returns search results with titles, snippets, and URLs
        """
        try:
            # Use ddgr (DuckDuckGo CLI) if available
            cmd = ['ddgr', '--json', '-n', '5', query]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                try:
                    results = json.loads(result.stdout)
                    return {
                        'query': query,
                        'results': results[:5]  # Top 5 results
                    }
                except json.JSONDecodeError:
                    pass

        except FileNotFoundError:
            # ddgr not installed, fall back to manual search
            pass
        except Exception as e:
            print(f"Search error for '{query}': {str(e)}")

        return None

    def _synthesize_findings(self, competitor: str, pain_point: str, findings: List[Dict]) -> Dict:
        """
        Synthesize research findings into structured competitor analysis
        """
        # Extract key information from findings
        has_feature = self._determine_feature_availability(findings)
        description = self._extract_description(competitor, pain_point, findings)
        pricing = self._extract_pricing_info(findings)
        limitations = self._extract_limitations(findings)
        links = self._extract_relevant_links(findings)

        return {
            'name': competitor,
            'has_feature': has_feature,
            'description': description,
            'pricing': pricing,
            'limitations': limitations,
            'links': links[:5],  # Top 5 links
            'notes': self._generate_notes(competitor, findings)
        }

    def _determine_feature_availability(self, findings: List[Dict]) -> Optional[bool]:
        """Determine if the competitor has the feature based on search results"""
        if not findings:
            return None

        # Look for positive indicators in search results
        positive_keywords = ['feature', 'support', 'available', 'how to', 'documentation']
        negative_keywords = ['not available', 'coming soon', 'roadmap', 'feature request']

        positive_count = 0
        negative_count = 0

        for finding in findings:
            results = finding.get('results', [])
            for result in results:
                snippet = (result.get('abstract', '') + ' ' + result.get('title', '')).lower()

                if any(kw in snippet for kw in positive_keywords):
                    positive_count += 1
                if any(kw in snippet for kw in negative_keywords):
                    negative_count += 1

        if positive_count > negative_count and positive_count > 0:
            return True
        elif negative_count > positive_count:
            return False

        return None  # Unknown

    def _extract_description(self, competitor: str, pain_point: str, findings: List[Dict]) -> str:
        """Extract a description of how the competitor addresses the pain point"""
        if not findings:
            return f"No specific information found about {competitor}'s {pain_point} capabilities."

        # Collect relevant snippets
        snippets = []
        for finding in findings:
            results = finding.get('results', [])
            for result in results[:2]:  # Top 2 per search
                snippet = result.get('abstract', '')
                if snippet and len(snippet) > 50:
                    snippets.append(snippet)

        if snippets:
            # Combine and truncate
            combined = ' '.join(snippets[:3])
            if len(combined) > 400:
                combined = combined[:400] + '...'
            return combined

        return f"Limited documentation available for {competitor}'s {pain_point} feature."

    def _extract_pricing_info(self, findings: List[Dict]) -> str:
        """Extract pricing information from search results"""
        for finding in findings:
            results = finding.get('results', [])
            for result in results:
                snippet = (result.get('abstract', '') + ' ' + result.get('title', '')).lower()

                # Look for pricing indicators
                if 'pricing' in snippet or 'plan' in snippet or 'tier' in snippet:
                    if 'enterprise' in snippet:
                        return "Enterprise tier"
                    if 'premium' in snippet or 'professional' in snippet:
                        return "Premium/Professional tier"
                    if 'free' in snippet:
                        return "Available in free tier"
                    if 'add-on' in snippet or 'additional' in snippet:
                        return "Available as add-on"

        return "Pricing information not found"

    def _extract_limitations(self, findings: List[Dict]) -> List[str]:
        """Extract known limitations from search results"""
        limitations = []

        limitation_keywords = [
            'limitation', 'does not support', 'cannot', 'not available',
            'restricted', 'only available', 'requires'
        ]

        for finding in findings:
            results = finding.get('results', [])
            for result in results:
                snippet = result.get('abstract', '').lower()

                for keyword in limitation_keywords:
                    if keyword in snippet:
                        # Extract the sentence containing the limitation
                        sentences = snippet.split('.')
                        for sentence in sentences:
                            if keyword in sentence:
                                limitations.append(sentence.strip().capitalize())
                                break

        return limitations[:3]  # Top 3 limitations

    def _extract_relevant_links(self, findings: List[Dict]) -> List[str]:
        """Extract relevant documentation and resource links"""
        links = []

        for finding in findings:
            results = finding.get('results', [])
            for result in results:
                url = result.get('url', '')
                title = result.get('title', '')

                if url and url not in links:
                    # Prefer documentation, feature, and help center links
                    url_lower = url.lower()
                    if any(term in url_lower for term in ['doc', 'help', 'feature', 'guide', 'support']):
                        links.insert(0, url)  # Priority links at the front
                    else:
                        links.append(url)

        return links

    def _generate_notes(self, competitor: str, findings: List[Dict]) -> str:
        """Generate additional notes about the research"""
        if not findings:
            return f"Unable to find detailed information about {competitor}. Manual research recommended."

        total_results = sum(len(f.get('results', [])) for f in findings)

        if total_results == 0:
            return f"No search results found for {competitor}. The feature may not be documented publicly."

        return f"Based on {total_results} search results. Review links for detailed information."


# Standalone search function using curl and DuckDuckGo HTML search
def perform_duckduckgo_search(query: str, num_results: int = 5) -> List[Dict]:
    """
    Perform DuckDuckGo search using curl (no API key or external tool needed)
    Returns list of {title, url, snippet} dictionaries
    """
    import urllib.parse

    # URL encode the query
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    try:
        # Fetch search results page
        cmd = [
            'curl', '-s', '-A',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            search_url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            return []

        html = result.stdout

        # Parse results using regex (simple parsing)
        results = []

        # Extract result blocks
        result_pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
        snippet_pattern = r'<a class="result__snippet"[^>]*>([^<]+)</a>'

        matches = re.finditer(result_pattern, html)
        snippets = re.finditer(snippet_pattern, html)

        snippet_list = [m.group(1) for m in snippets]

        for i, match in enumerate(matches):
            if i >= num_results:
                break

            url = match.group(1)
            title = match.group(2)

            # Decode URL (DuckDuckGo uses redirect URLs)
            if 'uddg=' in url:
                url_match = re.search(r'uddg=([^&]+)', url)
                if url_match:
                    url = urllib.parse.unquote(url_match.group(1))

            snippet = snippet_list[i] if i < len(snippet_list) else ''

            results.append({
                'title': title.strip(),
                'url': url.strip(),
                'snippet': snippet.strip()
            })

        return results

    except Exception as e:
        print(f"DuckDuckGo search error: {str(e)}")
        return []
