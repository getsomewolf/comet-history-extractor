# 🤝 Contributing to Comet History Extractor

Thank you for your interest in contributing to the Comet History Extractor! This project helps the Comet Browser community organize and leverage their browsing data with AI tools.

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Found a bug? Create an [issue](https://github.com/yourusername/comet-history-extractor/issues)
- Include your OS, Python version, and Comet Browser version
- Provide steps to reproduce the issue
- Share error messages and logs if possible

### 💡 Feature Requests
- Have an idea? Start a [discussion](https://github.com/yourusername/comet-history-extractor/discussions)
- Explain the use case and benefit to the community
- Include examples or mockups if applicable

### 📚 Documentation
- Improve README, guides, or code comments
- Add translations for international users
- Create video tutorials or blog posts
- Share AI prompt templates that work well

### 🔧 Code Contributions
- Fix bugs or implement new features
- Improve performance or add platform support
- Add tests or improve code quality
- Follow our development guidelines below

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ installed
- Git for version control
- Comet Browser installed (for testing)
- Basic understanding of SQLite databases

### Development Setup

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/yourusername/comet-history-extractor.git
   cd comet-history-extractor
   ```

2. **Create a Development Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number
   ```

3. **Set Up Environment**
   ```bash
   # No additional dependencies needed for basic functionality
   # For development tools (optional):
   pip install pytest black flake8
   ```

4. **Test Current Setup**
   ```bash
   python extract_comet_history.py --help  # Should show usage info
   ```

## 📝 Development Guidelines

### Code Style
- **Follow PEP 8** for Python code style
- **Use meaningful names** for variables and functions
- **Add docstrings** for classes and functions
- **Comment complex logic** for maintainability

### Project Structure
```
comet-history-extractor/
├── extract_comet_history.py    # Main extraction script
├── examples/                   # Sample outputs and usage
├── guides/                     # Documentation and tutorials
├── templates/                  # AI prompt templates
├── tests/                      # Test files (coming soon)
└── .github/                    # GitHub templates
```

### Code Patterns
Following the repository's MVT (Model-View-Template) and DRY principles:

- **Model**: `HistoryEntry` dataclass for data structure
- **View**: Console output and file generation
- **Template**: Reusable components and functions
- **DRY**: Shared utilities and consistent patterns

### Adding New Features

1. **Database Schema Changes**
   - Update the `HistoryExtractor` class
   - Modify SQL queries carefully
   - Test with different database states

2. **Output Formats**
   - Add new export methods to `HistoryExtractor`
   - Update documentation and examples
   - Ensure consistent data structure

3. **Categorization Rules**
   - Modify `_categorize_url()` method
   - Add comprehensive domain patterns
   - Include tests for edge cases

## 🧪 Testing

### Manual Testing
1. **Test with Real Data**
   - Use your own Comet Browser history
   - Test with different history sizes
   - Verify output file integrity

2. **Cross-Platform Testing**
   - Test on Windows, macOS, and Linux
   - Verify path handling across platforms
   - Check Unicode/encoding support

3. **Edge Cases**
   - Empty history databases
   - Corrupted or locked databases
   - Very large history files (10,000+ URLs)

### Automated Testing (Coming Soon)
We're working on adding automated tests:
- Unit tests for core functions
- Integration tests for database operations
- Output validation tests

## 📖 Documentation Standards

### Code Documentation
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Add type annotations for clarity
- **Comments**: Explain "why" not just "what"

### User Documentation
- **Clear examples**: Include practical use cases
- **Step-by-step guides**: Make them beginner-friendly
- **Screenshots**: Add visuals where helpful
- **Troubleshooting**: Include common issues and solutions

## 🔄 Submission Process

### Before Submitting
- [ ] Test your changes thoroughly
- [ ] Update documentation if needed
- [ ] Follow the code style guidelines
- [ ] Write clear commit messages

### Pull Request Process

1. **Create Descriptive PR**
   - Use clear title and description
   - Reference related issues
   - Explain what changes and why
   - Include testing details

2. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement

   ## Testing
   - [ ] Tested manually
   - [ ] Added/updated tests
   - [ ] Verified on multiple platforms

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   ```

3. **Code Review Process**
   - Maintainers will review your PR
   - Address feedback and suggestions
   - Update your branch as needed
   - Squash commits if requested

## 🎯 Priority Areas

We're especially looking for help with:

### 🔥 High Priority
- **GUI Application**: User-friendly interface for non-technical users
- **Browser Extension**: Real-time history export
- **Multi-Browser Support**: Chrome, Firefox, Safari compatibility
- **Performance Optimization**: Handle very large history files

### 📈 Medium Priority
- **Advanced AI Integration**: Local LLM support
- **Automated Organization**: Smart bookmark creation
- **Data Visualization**: Browsing pattern charts
- **Cloud Backup**: Secure history backup options

### 🌱 Nice to Have
- **Mobile App**: iOS/Android companion
- **Web Interface**: Browser-based tool
- **API**: Programmatic access to features
- **Plugins**: Extensible architecture

## 🌍 Community Guidelines

### Be Respectful
- Welcome newcomers and different experience levels
- Provide constructive feedback
- Focus on the contribution, not the contributor
- Help others learn and grow

### Communication
- Use clear, professional language
- Ask questions when unsure
- Share knowledge and experiences
- Be patient with response times

### Privacy Considerations
- Never request or share personal browsing data
- Use sample/test data in examples
- Respect user privacy in all features
- Follow data protection best practices

## 🏷️ Issue and PR Labels

### Issue Labels
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to docs
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested

### Priority Labels
- `priority:high`: Urgent issues
- `priority:medium`: Important improvements
- `priority:low`: Nice-to-have features

### Status Labels
- `in progress`: Currently being worked on
- `needs review`: Ready for maintainer review
- `needs testing`: Requires testing
- `blocked`: Waiting on external factors

## 📞 Getting Help

### Questions and Discussions
- **General Questions**: Use [GitHub Discussions](https://github.com/yourusername/comet-history-extractor/discussions)
- **Development Help**: Tag maintainers in relevant issues
- **Feature Planning**: Start a discussion before big changes

### Maintainer Contact
- Create an issue for bugs or features
- Use discussions for general questions
- Tag `@maintainer` for urgent matters

## 🎉 Recognition

All contributors will be:
- Listed in the README contributors section
- Credited in release notes
- Invited to join our contributor community
- Eligible for special contributor badges

## 📋 Contributor Checklist

Before your first contribution:
- [ ] Read and understand this guide
- [ ] Set up your development environment
- [ ] Look through existing issues and discussions
- [ ] Choose something to work on
- [ ] Introduce yourself in discussions (optional but welcome!)

Thank you for helping make Comet History Extractor better for everyone! 🚀

---

*This contributing guide is inspired by best practices from successful open-source projects. We welcome feedback on how to improve it.*
