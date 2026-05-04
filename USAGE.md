# How to Use the Product Research Tool

## Quick Start

1. **Start the server:**
   ```bash
   cd ~/product-research-tool
   python3 app.py
   ```

2. **Open your browser:**
   ```
   http://localhost:5000
   ```

3. **Enter a pain point** in the text box, for example:
   - "search attachments"
   - "AI-powered ticket routing"
   - "custom reporting dashboards"
   - "integration with Slack"

4. **Click "Analyze"** and wait 30-60 seconds

5. **Review the results:**
   - Total suggestions, supporters, customers
   - Total ARR at risk
   - Common themes
   - Top customers by ARR
   - Key customer quotes
   - Competitive landscape (placeholder for now)

## Example Queries

### Good Pain Point Descriptions
- ✅ "search attachments in tickets"
- ✅ "AI agents for customer support"
- ✅ "custom fields in reporting"
- ✅ "mobile app offline mode"

### Less Effective
- ❌ "better search" (too vague)
- ❌ "fix bugs" (not specific enough)

## What the Tool Does

### UserVoice Analysis
1. Searches UserVoice for suggestions matching your pain point
2. Groups results into themes (Search, Attachments, AI, Integration, etc.)
3. Extracts customer quotes and links
4. Calculates:
   - Total unique customers affected
   - Top 5 customers by ARR
   - Combined ARR at risk

### Competitive Analysis (Placeholder)
Currently shows placeholders for:
- Intercom
- Freshdesk
- ServiceNow
- Salesforce Service Cloud
- HubSpot Service Hub
- Jira Service Management
- Gorgias
- Kustomer

**Note:** Actual competitive research needs to be implemented with web search/scraping.

## Troubleshooting

### Server won't start
- Check if port 5000 is already in use: `lsof -ti:5000`
- Kill existing process: `kill $(lsof -ti:5000)`

### UserVoice search fails
- Verify your API credentials are set in `~/.claude/settings.local.json`
- Check that UserVoice CLI is at `~/uservoice-cli/uservoice-cli.py`
- Test the CLI directly: `python3 ~/uservoice-cli/uservoice-cli.py forums`

### Analysis takes too long
- Normal analysis takes 30-60 seconds
- If it times out, try a more specific pain point
- Check server logs for errors

## Next Steps

To enhance this tool:
1. Implement actual competitive research (web search + scraping)
2. Add export to PDF/Markdown
3. Cache results for faster repeated searches
4. Add trending analysis (feedback over time)
5. Integrate Zendesk Community posts

## Repository

GitHub: https://github.com/SalVazquez/product-research-tool
