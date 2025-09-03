# 🚀 Comet History Extractor

> **Extract, organize, and AI-enhance your Comet browser history data**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Comet Browser](https://img.shields.io/badge/Comet-Browser-purple.svg)](https://www.perplexity.ai/comet)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**Comet History Extractor** is a powerful tool that extracts your complete browsing history from [Comet Browser](https://www.perplexity.ai/comet) and formats it for AI-powered organization and analysis. Perfect for users who want to leverage AI to filter, categorize, and organize thousands of bookmarks and browsing data.

## 🎯 Why This Tool Exists

Comet Browser has security restrictions that prevent its AI assistant from accessing your browsing history directly. This tool bridges that gap by:

- 📤 **Extracting** your complete browsing history safely
- 🤖 **Formatting** data for AI processing (ChatGPT, Claude, etc.)
- 🗂️ **Categorizing** URLs automatically by domain patterns
- 📊 **Analyzing** your browsing patterns and statistics
- 🔒 **Respecting** your privacy - everything runs locally

## ✨ Features

### 🔍 **Complete Data Extraction**
- Extract all URLs with titles, visit counts, and timestamps
- Include search terms and referrer information
- Preserve visit history for each URL
- Handle large histories (10,000+ URLs tested)

### 🤖 **AI-Ready Output**
- **JSON format** for comprehensive AI analysis
- **CSV format** for spreadsheet compatibility  
- **Statistics file** with browsing insights
- Pre-categorized URLs by domain patterns
- **🆕 LLM Chunking** - Split large histories into token-compatible chunks

### 🧠 **Intelligent Chunking for LLMs**
- **Default 200k token chunks** (compatible with most modern LLMs)
- **1M token chunks** for models like Perplexity AI and Gemini Pro
- **Token estimation** based on content analysis
- **Seamless splitting** without losing data
- **Chunk metadata** for tracking and organization

### 🛡️ **Privacy & Security**
- Runs completely offline
- No data sent to external servers
- Creates temporary database copy (auto-cleaned)
- Open source - audit the code yourself

### 📈 **Smart Categorization**
Automatically categorizes your URLs into:
- 💻 Development & Tech
- 📚 Learning & Education  
- 💼 Work & Productivity
- 📰 News & Information
- 📱 Social Media
- 🛒 Shopping
- 🎮 Entertainment

## 🚀 Quick Start

### Prerequisites
- **Comet Browser** installed with browsing history
- **Python 3.8+** with `sqlite3` support
- **Windows/macOS/Linux** (tested on all platforms)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/comet-history-extractor.git
cd comet-history-extractor

# No additional dependencies needed - uses Python standard library!
```

### Usage

1. **Close Comet Browser** (to unlock the database)
2. **Run the extractor:**
   
   **Basic extraction (single file):**
   ```bash
   python extract_comet_history.py
   ```
   
   **🆕 LLM-compatible chunking:**
   ```bash
   # Split into 200k token chunks (recommended for most LLMs)
   python extract_comet_history.py --chunk-size 200k
   
   # Split into 1M token chunks (for large context models like Perplexity AI)
   python extract_comet_history.py --chunk-size 1M
   ```

3. **Get your organized data:**
   - **Without chunking:** `comet_history_complete.json`, `comet_history_summary.csv`, `comet_history_statistics.json`
   - **With chunking:** `comet_history_chunk_1.json`, `comet_history_chunk_2.json`, etc.

### AI Processing Example

Upload `comet_history_complete.json` to ChatGPT with this prompt:

```
I have 10,000+ URLs in my browser history. Please:
1. Filter for learning resources and tutorials
2. Remove duplicates and low-value content  
3. Categorize by programming languages/topics
4. Suggest a study plan based on my interests

Focus on the most visited and recent resources.
```

## 🧠 LLM Chunking Feature

### Why Chunking?
Large browser histories can exceed the token limits of even modern LLMs, causing:
- Truncated data processing
- Failed API calls
- Loss of important context
- Need for manual splitting

### Smart Chunking Solution
Our intelligent chunking feature automatically splits your history into LLM-compatible pieces:

```bash
# Default chunking (200k tokens) - works with most LLMs
python extract_comet_history.py --chunk-size 200k

# Large context models (1M tokens) - for Perplexity AI, Gemini Pro
python extract_comet_history.py --chunk-size 1M

# Custom sizes supported
python extract_comet_history.py --chunk-size 500k
```

### Output Format
Chunked files include metadata for easy tracking:
```json
{
  "chunk_info": {
    "chunk_id": 1,
    "total_chunks": 3,
    "total_entries": 1247,
    "estimated_tokens": 199850,
    "extraction_date": "2025-08-29T...",
    "categories": ["Development & Tech", "Learning & Education", ...]
  },
  "history": [
    // Your history entries here
  ]
}
```

### Recommended Chunk Sizes by LLM
| LLM | Context Window | Recommended Size |
|-----|----------------|------------------|
| GPT-4 Turbo | 128k tokens | `--chunk-size 100k` |
| Claude 3 | 200k tokens | `--chunk-size 200k` |
| Perplexity AI | 1M tokens | `--chunk-size 1M` |
| Gemini Pro | 1M tokens | `--chunk-size 1M` |

## 📁 Output Files Explained

### `comet_history_complete.json`
**Best for AI processing** - Complete structured data with metadata
```json
{
  "metadata": {
    "total_entries": 10325,
    "extraction_date": "2025-08-29T...",
    "categories": ["Development & Tech", "Learning & Education", ...]
  },
  "history": [
    {
      "url": "https://github.com/...",
      "title": "Amazing Project",
      "category": "Development & Tech",
      "visit_count": 15,
      "visits": [...],
      "search_terms": [...]
    }
  ]
}
```

### `comet_history_summary.csv`
**Best for spreadsheet analysis** - Simplified format for Excel/Google Sheets

| url | title | domain | category | visit_count | last_visit_time |
|-----|-------|--------|----------|-------------|------------------|
| https://... | Page Title | domain.com | Development & Tech | 5 | 2025-08-29... |

## 🔧 Advanced Configuration

### Custom Categories
Edit the `_categorize_url()` method to add your own classification rules:

```python
# Add your custom patterns
if 'your-domain.com' in domain:
    return "Your Custom Category"
```

### Database Location
For non-standard Comet installations, specify the database path:

```python
extractor = HistoryExtractor("path/to/your/History")
```

## 🗂️ Browser Migration Guide

### Migrating TO Comet Browser

#### From Chrome/Chromium
1. **Export Chrome bookmarks:** Chrome Menu → Bookmarks → Bookmark manager → ⋮ → Export bookmarks
2. **Import to Comet:** Comet Menu → Bookmarks → Import bookmarks and settings → Choose Chrome
3. **Run this tool** to extract organized data

#### From Firefox  
1. **Export Firefox data:** Firefox Menu → Library → Bookmarks → Show All Bookmarks → Import and Backup → Export Bookmarks to HTML
2. **Import to Comet:** Comet Menu → Bookmarks → Import bookmarks and settings → Choose HTML file
3. **Run this tool** to get AI-ready format

#### From Safari (macOS)
1. **Export Safari bookmarks:** Safari → File → Export Bookmarks
2. **Import to Comet:** Use the HTML file import option
3. **Extract with this tool** for AI organization

#### From Edge
1. **Export Edge favorites:** Edge Menu → Favorites → ⋮ → Export favorites  
2. **Import to Comet:** Standard HTML bookmark import
3. **Use this tool** to create structured data

> **💡 Pro Tip:** After migration, use this tool regularly to maintain an AI-ready backup of your browsing data!

## 📊 Example Statistics

From a real extraction of 10,325 URLs:

```
📝 Total URLs: 10,325
👁️ Total Visits: 22,377
🔍 Total Search Terms: 4
🏆 Most Visited: chess.com (3,516 visits)

🗂️ Categories:
   • Other: 8,215 URLs
   • Learning & Education: 756 URLs  
   • Development & Tech: 586 URLs
   • Social Media: 505 URLs
   • Work & Productivity: 77 URLs
```

## 🤖 AI Processing Prompts

### 📚 Learning Resource Organization
```
Extract all educational content and organize by:
1. Programming tutorials and documentation
2. Online courses and certifications  
3. Technical articles and blog posts
4. Video tutorials and lectures

Prioritize by visit count and recency.
```

### 🧹 History Cleanup
```
Analyze this browser history and:
1. Identify duplicate or similar URLs
2. Find outdated or broken links
3. Categorize into Keep/Archive/Delete
4. Create a prioritized bookmark structure

Provide reasoning for each decision.
```

### 🎯 Project-Focused Filtering
```
I'm working on a [TECHNOLOGY] project. From my history:
1. Find all related resources and documentation
2. Identify the most useful references I've found
3. Suggest additional resources I might need
4. Create a study/reference guide

Remove social media and entertainment.
```

## 🛠️ Development

### Project Structure
```
comet-history-extractor/
├── extract_comet_history.py    # Main extraction script
├── examples/                   # Example outputs and prompts
├── guides/                     # Migration and usage guides  
├── templates/                  # AI prompt templates
└── tests/                      # Test files
```

### Contributing

We welcome contributions! Please see:
- 🐛 [Report issues](https://github.com/yourusername/comet-history-extractor/issues)
- 💡 [Suggest features](https://github.com/yourusername/comet-history-extractor/discussions)
- 🔧 [Submit pull requests](https://github.com/yourusername/comet-history-extractor/pulls)

### Roadmap
- [ ] GUI application for non-technical users
- [ ] Support for other Chromium-based browsers
- [ ] Built-in AI integration (local LLMs)
- [ ] Automated bookmark organization
- [ ] Browser extension for real-time export

## ❓ FAQ

**Q: Is this safe to use?**  
A: Yes! The tool only reads your local browser database and runs completely offline. No data is sent anywhere.

**Q: Will this work with other browsers?**  
A: Currently designed for Comet Browser, but the SQLite structure is similar to other Chromium browsers. PRs welcome for multi-browser support!

**Q: Can I run this while Comet is open?**  
A: No, the browser locks the database. Close Comet Browser before running the extraction.

**Q: What if I have a huge history?**  
A: Tested with 10,000+ URLs without issues. Large histories may take a few minutes to process.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Perplexity AI** for creating the excellent Comet Browser
- **Community contributors** who help improve this tool
- **AI researchers** making history analysis accessible to everyone

## 🌟 Star This Repository

If this tool helped you organize your browsing data, please ⭐ star this repository to help others discover it!

---

**Made with ❤️ for the Comet Browser community**

*Want to contribute? Check out our [Contributing Guidelines](CONTRIBUTING.md)*
