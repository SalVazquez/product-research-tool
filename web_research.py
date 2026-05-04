"""
Enhanced web research using WebFetch for deep analysis
"""

import subprocess
import json
import re
from typing import Dict, List, Optional
import urllib.parse


def search_and_analyze_competitor(competitor: str, pain_point: str) -> Dict:
    """
    Search for competitor information and analyze documentation
    Returns structured analysis
    """
    print(f"Researching {competitor} for '{pain_point}'...")

    # Try getting pre-researched intelligence first
    from competitive_intel import get_competitive_intel

    intel = get_competitive_intel(pain_point, competitor)
    if intel:
        print(f"  ✓ Using pre-researched intelligence")
        return intel

    # Step 1: Perform web search
    print(f"  → Performing web search...")
    search_results = perform_web_search(competitor, pain_point)

    if not search_results:
        return {
            'name': competitor,
            'has_feature': None,
            'description': f'Unable to find public documentation about {competitor}\'s {pain_point} capabilities. This may require manual research or the feature may not be publicly documented.',
            'pricing': 'Unknown - requires manual research',
            'limitations': [],
            'links': [],
            'notes': 'No search results found. Consider manual documentation review.'
        }

    # Step 2: Analyze search results
    print(f"  → Analyzing {len(search_results)} results...")
    has_feature = analyze_feature_availability(search_results, pain_point)
    description = extract_description(search_results, competitor, pain_point)
    pricing = extract_pricing_info(search_results)
    limitations = extract_limitations(search_results)
    links = [r['url'] for r in search_results[:5]]

    return {
        'name': competitor,
        'has_feature': has_feature,
        'description': description,
        'pricing': pricing,
        'limitations': limitations,
        'links': links,
        'notes': f'Based on {len(search_results)} web search results'
    }


def perform_web_search(competitor: str, pain_point: str, max_results: int = 5) -> List[Dict]:
    """
    Perform web search using multiple strategies
    Returns list of {title, url, snippet} dictionaries
    """
    # Try DuckDuckGo first
    results = duckduckgo_search(f"{competitor} {pain_point} feature", max_results)

    if not results:
        # Fallback: Try alternative search terms
        alternative_queries = [
            f"{competitor} {pain_point} documentation",
            f"{competitor} {pain_point} help",
            f"{competitor} {pain_point} support"
        ]

        for query in alternative_queries:
            results = duckduckgo_search(query, max_results)
            if results:
                break

    # Also try searching specific competitor domains
    if not results:
        domain = get_competitor_domain(competitor)
        if domain:
            results = duckduckgo_search(f"site:{domain} {pain_point}", max_results)

    return results


def duckduckgo_search(query: str, num_results: int = 5) -> List[Dict]:
    """
    Perform DuckDuckGo search using curl (no API key needed)
    """
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    try:
        cmd = [
            'curl', '-s', '-A',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            search_url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode != 0:
            return []

        html = result.stdout
        return parse_duckduckgo_results(html, num_results)

    except Exception as e:
        print(f"  Search error: {str(e)}")
        return []


def parse_duckduckgo_results(html: str, max_results: int) -> List[Dict]:
    """Parse DuckDuckGo HTML results"""
    results = []

    try:
        # Extract result blocks using regex
        result_pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
        snippet_pattern = r'<a class="result__snippet"[^>]*>([^<]+)</a>'

        url_title_matches = list(re.finditer(result_pattern, html))
        snippet_matches = list(re.finditer(snippet_pattern, html))

        for i in range(min(len(url_title_matches), max_results)):
            match = url_title_matches[i]
            url = match.group(1)
            title = match.group(2)

            # Decode DuckDuckGo redirect URL
            if 'uddg=' in url:
                url_match = re.search(r'uddg=([^&]+)', url)
                if url_match:
                    url = urllib.parse.unquote(url_match.group(1))

            snippet = ''
            if i < len(snippet_matches):
                snippet = snippet_matches[i].group(1)

            results.append({
                'title': clean_html_text(title),
                'url': url.strip(),
                'snippet': clean_html_text(snippet)
            })

    except Exception as e:
        print(f"  Parse error: {str(e)}")

    return results


def clean_html_text(text: str) -> str:
    """Remove HTML entities and clean text"""
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#x27;', "'")
    return text.strip()


def analyze_feature_availability(results: List[Dict], pain_point: str) -> Optional[bool]:
    """Determine if competitor has the feature"""
    positive_indicators = [
        'feature', 'support', 'available', 'how to', 'enable',
        'documentation', 'guide', 'tutorial', 'use'
    ]
    negative_indicators = [
        'not available', 'coming soon', 'roadmap', 'planned',
        'feature request', 'not supported', 'does not'
    ]

    positive_score = 0
    negative_score = 0

    for result in results:
        text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()

        # Score based on indicators
        for indicator in positive_indicators:
            if indicator in text:
                positive_score += 1

        for indicator in negative_indicators:
            if indicator in text:
                negative_score += 2  # Negative indicators weigh more

    if positive_score > negative_score and positive_score >= 2:
        return True
    elif negative_score > positive_score and negative_score >= 2:
        return False

    return None  # Unknown


def extract_description(results: List[Dict], competitor: str, pain_point: str) -> str:
    """Extract description from search results"""
    snippets = []

    for result in results[:3]:
        snippet = result.get('snippet', '').strip()
        if snippet and len(snippet) > 40:
            # Clean up snippet
            snippet = re.sub(r'\s+', ' ', snippet)
            snippets.append(snippet)

    if snippets:
        combined = ' '.join(snippets)
        # Truncate if too long
        if len(combined) > 600:
            combined = combined[:600] + '...'
        return combined

    # Fallback: use titles
    titles = [r.get('title', '') for r in results[:2]]
    if titles:
        return f"{competitor} - {', '.join(titles)}"

    return f'Limited public documentation available for {competitor}\'s {pain_point} feature. See links for more details.'


def extract_pricing_info(results: List[Dict]) -> str:
    """Extract pricing information from results"""
    pricing_keywords = {
        'enterprise': 'Enterprise tier',
        'premium': 'Premium tier',
        'professional': 'Professional tier',
        'add-on': 'Available as add-on',
        'free tier': 'Available in free tier',
        'included': 'Included in standard plans',
        'additional cost': 'Requires additional payment'
    }

    for result in results:
        text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()

        for keyword, pricing_desc in pricing_keywords.items():
            if keyword in text and ('pricing' in text or 'plan' in text or 'tier' in text):
                return pricing_desc

    return 'Pricing information not specified in public documentation'


def extract_limitations(results: List[Dict]) -> List[str]:
    """Extract known limitations"""
    limitations = []
    limitation_keywords = [
        'limitation', 'does not support', 'cannot', 'only available',
        'requires', 'restricted to', 'not compatible'
    ]

    for result in results:
        snippet = result.get('snippet', '')

        for keyword in limitation_keywords:
            if keyword.lower() in snippet.lower():
                # Extract the sentence containing the limitation
                sentences = re.split(r'[.!?]', snippet)
                for sentence in sentences:
                    if keyword.lower() in sentence.lower() and 50 < len(sentence) < 300:
                        clean_sentence = sentence.strip().capitalize()
                        if clean_sentence and clean_sentence not in limitations:
                            limitations.append(clean_sentence)
                            break

    return limitations[:4]  # Return up to 4 limitations


def get_competitor_domain(competitor: str) -> Optional[str]:
    """Get the primary domain for a competitor"""
    domains = {
        'Intercom': 'intercom.com',
        'Freshdesk': 'freshdesk.com',
        'Freshworks': 'freshworks.com',
        'ServiceNow': 'servicenow.com',
        'Salesforce Service Cloud': 'salesforce.com',
        'HubSpot Service Hub': 'hubspot.com',
        'Jira Service Management': 'atlassian.com',
        'Gorgias': 'gorgias.com',
        'Kustomer': 'kustomer.com'
    }

    return domains.get(competitor)
