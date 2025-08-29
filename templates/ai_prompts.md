# 🤖 AI Prompt Templates for Comet History Analysis

This file contains proven prompts for different use cases when analyzing your extracted Comet browser history with AI tools.

## 📚 Learning Resource Organization

```
I have my complete browser history extracted from Comet Browser (JSON attached). Please analyze it and:

1. **Extract Educational Content:**
   - Programming tutorials and documentation
   - Online courses and certifications
   - Technical articles and blog posts
   - Video tutorials and educational content

2. **Organize by Technology/Topic:**
   - Group similar resources together
   - Identify learning paths and progressions
   - Note frequently visited resources (high visit_count)

3. **Prioritize and Rank:**
   - Mark as High/Medium/Low priority based on:
     - Visit frequency and recency
     - Content quality and relevance
     - Progression in learning path

4. **Output Format:** Markdown with links, categories, and priority levels

Focus on actionable learning resources that show a clear learning progression.
```

## 🎯 Project-Specific Resource Extraction

```
Context: I'm working on a [PROJECT TYPE - e.g., "React web application", "Python data analysis", "mobile app"] project.

From my browser history JSON, please:

1. **Identify Relevant Resources:**
   - Documentation and official guides
   - Tutorials and code examples
   - Tools and libraries I've researched
   - Problem-solving resources (Stack Overflow, etc.)

2. **Categorize by Development Phase:**
   - Planning & Architecture
   - Development & Implementation  
   - Testing & Debugging
   - Deployment & Optimization

3. **Highlight Key Resources:**
   - Most visited pages (visit_count > 3)
   - Recently accessed resources
   - Resources I might have forgotten about

4. **Suggest Study Order:** Recommend a logical sequence for reviewing these resources

Remove social media, entertainment, and unrelated browsing data.
```

## 🧹 History Cleanup & Organization

```
Please help me clean up and organize my browser history data:

1. **Identify Duplicates:**
   - Very similar URLs from the same domain
   - Different URLs with identical or near-identical titles
   - Redundant resources covering the same topics

2. **Quality Assessment:**
   - High-value resources (frequently visited, educational)
   - Medium-value resources (useful but not essential)
   - Low-value resources (outdated, one-time visits)

3. **Categorize Actions:**
   - **Keep:** Essential resources, frequently used
   - **Archive:** Useful but not currently relevant
   - **Delete:** Outdated, broken, or low-value content

4. **Create Bookmark Structure:**
   Suggest a hierarchical bookmark organization based on:
   - Categories (Dev, Learning, Work, etc.)
   - Frequency of use
   - Logical grouping

Provide clear reasoning for each categorization decision.
```

## 📊 Browsing Pattern Analysis

```
Analyze my browsing patterns from this history data and provide insights on:

1. **Interest Analysis:**
   - What are my main professional/learning interests?
   - Which technologies or topics am I focusing on?
   - Are there emerging patterns in my recent browsing?

2. **Learning Path Identification:**
   - What learning progressions can you identify?
   - Which skills am I developing based on visited resources?
   - Are there gaps in my learning that I should address?

3. **Productivity Insights:**
   - Which resources do I return to most often? (high visit_count)
   - What types of content do I engage with deeply? (long visit duration)
   - Are there productivity tools I should explore more?

4. **Recommendations:**
   - Complementary resources I might be missing
   - Areas for deeper exploration
   - Potential distractions to minimize

Focus on professional development and learning opportunities.
```

## 🔍 Domain-Specific Analysis

```
Focus on [SPECIFIC DOMAIN - e.g., "github.com", "stackoverflow.com", "youtube.com"] from my history:

1. **Content Analysis:**
   - What types of content do I access most on this domain?
   - Which specific pages/resources are most valuable?
   - What patterns emerge in my usage?

2. **Learning Extraction:**
   - What skills or knowledge areas does this represent?
   - How has my usage of this domain evolved over time?
   - What are the key takeaways from my activity?

3. **Optimization Suggestions:**
   - How can I better leverage this domain for learning/productivity?
   - Are there related resources on this domain I should explore?
   - What organizational system would work best for these resources?

Include visit counts, timestamps, and any search terms associated with this domain.
```

## 🎨 Content Curation by Category

```
From my browser history, create curated lists for each category:

**Categories to focus on:**
- Development & Tech
- Learning & Education
- Work & Productivity
- [Add any specific categories you're interested in]

**For each category:**
1. **Top 20 Resources:** Most valuable based on visit frequency and quality
2. **Recent Discoveries:** Resources visited in the last [timeframe]
3. **Hidden Gems:** Low visit count but potentially high value
4. **Quick Reference:** Resources perfect for bookmarking

**Output Format:**
- Markdown with clear headings
- Include URL, title, and brief description
- Mark priority level (⭐⭐⭐ = essential)
- Note visit count and last access date

Exclude social media and entertainment unless specifically relevant to professional growth.
```

## 🔄 Migration & Bookmark Creation

```
I want to create an organized bookmark structure from my browser history. Please:

1. **Analyze Current Data:**
   - Identify the most important resources (visit_count > 5)
   - Group related resources together
   - Note resources that should be easily accessible

2. **Design Bookmark Structure:**
   ```
   📁 Development
     📁 Documentation
     📁 Tools & Resources
     📁 Learning
   📁 Work
     📁 Daily Tools
     📁 Reference Materials
   📁 Learning
     📁 Current Focus
     📁 Future Learning
   ```

3. **Create Import-Ready Format:**
   - Generate HTML bookmark file format
   - Or provide organized lists for manual creation
   - Include descriptions and tags where helpful

4. **Maintenance Recommendations:**
   - Which bookmarks to review regularly
   - How to keep the structure organized
   - Suggested review intervals

Prioritize accessibility and logical organization over completeness.
```

## 💡 Usage Tips

### For Best Results:
1. **Be Specific:** Mention your current projects, interests, or goals
2. **Set Context:** Explain what you're trying to achieve
3. **Request Formats:** Ask for specific output formats (Markdown, JSON, etc.)
4. **Iterate:** Use follow-up prompts to refine results

### File Size Considerations:
- **Large histories (>5MB):** Use the CSV file for initial analysis
- **Comprehensive analysis:** Upload the complete JSON file
- **Quick insights:** Share just the statistics JSON first

### Follow-up Prompts:
- "Can you focus more on [specific technology/topic]?"
- "Please provide this in a different format"
- "What are the top 10 resources I should bookmark immediately?"
- "Create a study plan based on these resources"

---

*These prompts are designed to work with any AI assistant (ChatGPT, Claude, Gemini, etc.). Adjust the language and specificity based on your chosen AI tool's capabilities.*
