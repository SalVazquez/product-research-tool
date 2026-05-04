# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### 1. Start the Server

```bash
cd ~/product-research-tool
python3 app.py
```

You should see:
```
Starting Product Research Tool...
Open http://localhost:5000 in your browser
```

### 2. Open the Web Interface

Open your browser and go to:
```
http://localhost:5000
```

### 3. Run Your First Analysis

Try one of these pain points:

**Example 1: Search Attachments**
```
search attachments
```

**Example 2: AI Features**
```
AI ticket routing
```

**Example 3: Custom Query**
```
mobile app offline support
```

Click **"Analyze"** and wait 30-60 seconds.

## 📊 Understanding the Results

### Customer Feedback Section

- **Total Suggestions**: How many UserVoice suggestions match this pain point
- **Total Supporters**: Number of customers who upvoted these suggestions
- **Unique Customers**: Count of distinct customers requesting this
- **Total ARR**: Combined annual recurring revenue of affected customers

**Key Themes**: Common patterns in customer feedback grouped by category

**Top Customers**: Highest-value customers (by ARR) requesting this feature

**Key Quotes**: Actual customer feedback with links to UserVoice

### Competitive Analysis Section

For each competitor, you'll see:

✅ **Has Feature** - Competitor offers this capability
❌ **Doesn't Have** - Competitor lacks this feature  
❓ **Unknown** - No public information available

Plus:
- **Description**: How the competitor implements it
- **Pricing**: Which tier/plan includes this feature
- **Limitations**: Known constraints or restrictions
- **Links**: Documentation and resource URLs

## 🎯 Supported Pain Points

### Fully Researched (8 competitors):
- **Search attachments** - Searching content within PDFs, images, documents
- **AI features** - Artificial intelligence, automation, intelligent routing

### Partial Support (via UserVoice only):
- Any other pain point will search UserVoice feedback
- Competitive analysis will attempt web search (results may vary)

## 💡 Tips

1. **Be Specific**: "AI-powered ticket routing" is better than "AI stuff"

2. **Use Keywords**: The tool matches on keywords like:
   - Search, attachment, file, PDF → Search attachments intel
   - AI, automation, intelligent, machine learning → AI features intel

3. **Check Links**: UserVoice and documentation links are clickable - use them!

4. **Export Results**: Copy/paste from browser or screenshot for reports

5. **Multiple Analyses**: Run different pain points back-to-back

## 🐛 Troubleshooting

**Server won't start?**
```bash
# Check if port 5000 is in use
lsof -ti:5000

# Kill existing server
kill $(lsof -ti:5000)
```

**No UserVoice results?**
- Check your UserVoice API credentials in `~/.claude/settings.local.json`
- Verify UserVoice CLI is working: `python3 ~/uservoice-cli/uservoice-cli.py forums`

**Slow performance?**
- Normal: 30-60 seconds for full analysis
- UserVoice search can take time with many results
- Be patient, especially on first run

## 📝 Example Output

For "search attachments" you'll see:

**UserVoice**: 20+ suggestions, key themes like "Search & Discovery", "Attachments"

**Competitors**:
- ✅ Freshdesk: Available in Estate/Forest plans
- ✅ ServiceNow: Included in standard platform
- ✅ Salesforce: Enterprise edition and above
- ❌ Intercom: Not available
- ❌ HubSpot: Filename search only

## 🔄 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running, or:

```bash
kill $(lsof -ti:5000)
```

## 📚 Next Steps

- Read [USAGE.md](USAGE.md) for detailed documentation
- Check [README.md](README.md) for technical details
- Add more pain points to `competitive_intel.py` for your use cases
- Customize the UI in `templates/index.html`

---

**Questions?** Check the server logs or README.md for troubleshooting.
