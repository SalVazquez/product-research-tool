"""
Competitive intelligence database
Pre-researched competitor capabilities for common pain points
"""

# Hardcoded competitive intelligence for common pain points
COMPETITIVE_INTEL = {
    'search attachments': {
        'Intercom': {
            'has_feature': False,
            'description': 'Intercom does not currently support searching within attachment content. Users can search conversation text but not the contents of PDFs, images, or other attached files.',
            'pricing': 'N/A - Feature not available',
            'limitations': ['Cannot search PDF content', 'Cannot search image text', 'Attachment search limited to filename only'],
            'links': ['https://www.intercom.com/help/en/articles/180-search-for-conversations']
        },
        'Freshdesk': {
            'has_feature': True,
            'description': 'Freshdesk offers attachment search capabilities through their advanced search feature. Users can search for tickets based on attachment names and in some plans, attachment content indexing is available.',
            'pricing': 'Available in Estate and Forest plans',
            'limitations': ['Content indexing may have file size limits', 'Limited file format support for content search'],
            'links': ['https://support.freshdesk.com/support/solutions/articles/212480-searching-for-tickets']
        },
        'ServiceNow': {
            'has_feature': True,
            'description': 'ServiceNow provides full-text search capabilities including attachment content search. The platform indexes various file types including PDFs, Word documents, and Excel spreadsheets for searchability.',
            'pricing': 'Included in standard platform',
            'limitations': ['Requires proper indexing configuration', 'Performance impact on large attachments'],
            'links': ['https://docs.servicenow.com/bundle/vancouver-platform-user-interface/page/use/common-ui-elements/concept/c_TextSearch.html']
        },
        'Salesforce Service Cloud': {
            'has_feature': True,
            'description': 'Salesforce Service Cloud supports searching file content through Salesforce Files and Enhanced Search. Files attached to cases and records are indexed and searchable, including PDFs and Office documents.',
            'pricing': 'Available in Enterprise edition and above',
            'limitations': ['File size limits apply', 'Indexing delays for newly uploaded files'],
            'links': ['https://help.salesforce.com/s/articleView?id=sf.search_files.htm']
        },
        'HubSpot Service Hub': {
            'has_feature': False,
            'description': 'HubSpot Service Hub allows searching by attachment filename but does not currently support full-text search within attachment content.',
            'pricing': 'N/A - Feature not available',
            'limitations': ['No content indexing', 'Filename search only'],
            'links': ['https://knowledge.hubspot.com/files/search-for-files']
        },
        'Jira Service Management': {
            'has_feature': True,
            'description': 'Jira Service Management supports attachment search through Confluence integration and native search. When files are indexed, content from PDFs and Office documents becomes searchable.',
            'pricing': 'Available in Premium and Enterprise tiers',
            'limitations': ['Requires Confluence integration for best results', 'Limited file format support'],
            'links': ['https://support.atlassian.com/jira-service-management-cloud/docs/search-for-issues/']
        },
        'Gorgias': {
            'has_feature': False,
            'description': 'Gorgias focuses on e-commerce support and does not currently offer attachment content search. Users can filter tickets by presence of attachments but not search within them.',
            'pricing': 'N/A - Feature not available',
            'limitations': ['No attachment content indexing', 'Basic attachment filtering only'],
            'links': ['https://docs.gorgias.com/en-US/tickets-234447']
        },
        'Kustomer': {
            'has_feature': False,
            'description': 'Kustomer allows searching conversations and customer data but does not currently index attachment content for search purposes.',
            'pricing': 'N/A - Feature not available',
            'limitations': ['Attachment search not supported', 'Filename search only'],
            'links': ['https://help.kustomer.com/en_us/search-conversations-rJZ0ZdYX8']
        }
    },
    'ai': {
        'Intercom': {
            'has_feature': True,
            'description': 'Intercom offers Fin AI Agent which can answer customer questions automatically using AI, resolve tickets, and provide intelligent routing based on conversation context.',
            'pricing': 'Starting at $0.99 per resolution, available as add-on',
            'limitations': ['Requires English language content for best performance', 'May need significant content library'],
            'links': ['https://www.intercom.com/ai']
        },
        'Freshdesk': {
            'has_feature': True,
            'description': 'Freshdesk provides Freddy AI for intelligent ticket assignment, suggested responses, and automated categorization. Also includes sentiment analysis.',
            'pricing': 'Available in Forest plan and above',
            'limitations': ['Limited language support', 'Requires training period'],
            'links': ['https://www.freshworks.com/freshdesk/features/ai-chatbots/']
        },
        'ServiceNow': {
            'has_feature': True,
            'description': 'ServiceNow Now Assist provides generative AI capabilities including case summarization, intelligent routing, and automated resolution suggestions.',
            'pricing': 'Enterprise tier feature',
            'limitations': ['Requires substantial configuration', 'High enterprise pricing'],
            'links': ['https://www.servicenow.com/products/now-assist-generative-ai.html']
        },
        'Salesforce Service Cloud': {
            'has_feature': True,
            'description': 'Einstein AI provides case classification, routing, recommended responses, and predictive analytics for service cases.',
            'pricing': 'Einstein features priced separately, starting at $50/user/month',
            'limitations': ['Requires Einstein add-on purchase', 'Minimum user requirements'],
            'links': ['https://www.salesforce.com/products/einstein/ai-for-service/']
        },
        'HubSpot Service Hub': {
            'has_feature': True,
            'description': 'HubSpot offers AI-powered conversation intelligence, ticket routing, and ChatSpot AI assistant for support teams.',
            'pricing': 'AI features included in Professional and Enterprise tiers',
            'limitations': ['Limited customization of AI behavior', 'English-first AI models'],
            'links': ['https://www.hubspot.com/products/service/ai']
        },
        'Jira Service Management': {
            'has_feature': True,
            'description': 'Atlassian Intelligence provides AI-powered issue summarization, suggested responses, and automated ticket categorization.',
            'pricing': 'Available in Premium and Enterprise with Atlassian Intelligence add-on',
            'limitations': ['Requires Atlassian Intelligence subscription', 'Limited to certain regions'],
            'links': ['https://www.atlassian.com/software/jira/service-management/features/ai']
        },
        'Gorgias': {
            'has_feature': True,
            'description': 'Gorgias Automate uses AI to handle repetitive e-commerce support queries, provide instant responses, and suggest macros.',
            'pricing': 'Available in Pro plan and above',
            'limitations': ['Optimized for e-commerce use cases', 'Limited general AI capabilities'],
            'links': ['https://www.gorgias.com/automate']
        },
        'Kustomer': {
            'has_feature': True,
            'description': 'Kustomer IQ provides AI-powered insights, intelligent routing, and automated conversation categorization.',
            'pricing': 'Enterprise tier feature',
            'limitations': ['Requires Enterprise plan', 'Setup complexity'],
            'links': ['https://www.kustomer.com/platform/kustomer-iq']
        }
    }
}


def get_competitive_intel(pain_point: str, competitor: str) -> dict:
    """
    Get pre-researched competitive intelligence
    Returns None if not found in database
    """
    # Normalize pain point keywords
    pain_point_lower = pain_point.lower()

    # Match pain point to intel categories
    category = None
    if any(keyword in pain_point_lower for keyword in ['search', 'attachment', 'file', 'pdf', 'document']):
        if 'attach' in pain_point_lower:
            category = 'search attachments'
    elif any(keyword in pain_point_lower for keyword in ['ai', 'artificial intelligence', 'machine learning', 'automation', 'intelligent', 'smart']):
        category = 'ai'

    if category and category in COMPETITIVE_INTEL:
        intel_data = COMPETITIVE_INTEL[category]
        if competitor in intel_data:
            data = intel_data[competitor].copy()
            data['name'] = competitor
            data['notes'] = f'Pre-researched intelligence for {category}'
            return data

    return None


def has_competitive_intel(pain_point: str) -> bool:
    """Check if we have pre-researched intel for this pain point"""
    pain_point_lower = pain_point.lower()

    if any(keyword in pain_point_lower for keyword in ['search', 'attachment']):
        if 'attach' in pain_point_lower:
            return True
    elif any(keyword in pain_point_lower for keyword in ['ai', 'artificial']):
        return True

    return False
