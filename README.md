# Product Research Tool

A web-based tool for analyzing customer feedback from UserVoice and researching competitive solutions for product pain points.

## Features

### Customer Feedback Analysis
- Search UserVoice for related suggestions
- Group feedback into common themes
- Extract key customer quotes with links
- Calculate customer impact:
  - Total suggestions and supporters
  - Unique customers affected
  - Top customers by ARR
  - Total ARR at risk

### Competitive Analysis
- Research how 8 major competitors solve the same problem:
  - Intercom
  - Freshdesk
  - ServiceNow
  - Salesforce Service Cloud
  - HubSpot Service Hub
  - Jira Service Management
  - Gorgias
  - Kustomer
- Details on implementation, pricing, and limitations

## Setup

### Prerequisites
- Python 3.9+
- UserVoice CLI configured with API credentials
- UserVoice CLI installed at `~/uservoice-cli/uservoice-cli.py`

### Installation

1. Clone the repository:
```bash
cd ~/product-research-tool
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Ensure your UserVoice API credentials are configured in `~/.claude/settings.local.json`:
```json
{
  "env": {
    "USERVOICE_API_KEY": "your-key",
    "USERVOICE_API_SECRET": "your-secret"
  }
}
```

## Usage

1. Start the server:
```bash
python3 app.py
```

2. Open your browser to:
```
http://localhost:5000
```

3. Enter a pain point description (e.g., "searching attachments in Zendesk")

4. Click "Analyze" and wait 30-60 seconds for results

5. Review:
   - Customer feedback themes and quotes
   - Top customers by ARR
   - Total ARR impact
   - Competitive landscape

## Architecture

- **app.py**: Flask web server with `/analyze` endpoint
- **analyzer.py**: 
  - `UserVoiceAnalyzer`: Searches and analyzes UserVoice feedback
  - `CompetitiveAnalyzer`: Researches competitor solutions (placeholder for web search)
- **templates/index.html**: Single-page frontend with results display

## Roadmap

- [ ] Implement actual competitive research (web search + documentation scraping)
- [ ] Add caching for repeated searches
- [ ] Export results as PDF/Markdown
- [ ] Batch analysis of multiple pain points
- [ ] Integration with Zendesk Community posts
- [ ] Trending analysis (feedback over time)

## Development

The tool uses:
- Flask for the web framework
- UserVoice CLI (Python) for data access
- Vanilla JavaScript for frontend interactivity

## Notes

- Competitive analysis is currently a placeholder - actual web research needs implementation
- UserVoice CLI must be accessible at `~/uservoice-cli/uservoice-cli.py`
- Analysis can take 30-60 seconds depending on search results volume
