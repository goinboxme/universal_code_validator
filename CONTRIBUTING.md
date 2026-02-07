# Contributing to Universal Code Validator

First off, thank you for considering contributing to Universal Code Validator! 🎉

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When creating a bug report, include:
- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Python version**
- **Platform** (Desktop/Android/Pydroid 3/Termux)
- **Sample code** (if applicable)
- **Output/error messages**

Example:
```
**Bug:** False positive on string containing 'eval'

**Steps:**
1. Create file with string: `message = "Please evaluate your options"`
2. Run validator
3. See security warning

**Expected:** No warning (it's just a string)
**Actual:** Security warning about eval usage
**Python:** 3.9.5
**Platform:** Pydroid 3 on Android 12
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating one:

- **Use clear, descriptive title**
- **Explain the problem** this enhancement would solve
- **Describe the solution** you'd like
- **Describe alternatives** you've considered
- **Provide examples** if applicable

### 🔧 Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** on various Python files
4. **Test on Android** if changes affect mobile users
5. **Update documentation** if needed
6. **Write clear commit messages**
7. **Submit the pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/universal-code-validator.git
cd universal-code-validator

# Create a branch
git checkout -b feature/your-feature-name
```

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and single-purpose

### Example:
```python
def analyze_complexity(node: ast.Node) -> float:
    """
    Calculate cyclomatic complexity of an AST node.
    
    Args:
        node: AST node to analyze
        
    Returns:
        Complexity score as float
    """
    # Implementation
    pass
```

### Code Organization
- Group related functions together
- Use clear, descriptive names
- Add comments for complex logic
- Keep files under 2000 lines when possible

### Testing
Test your changes on:
- Simple scripts
- Complex frameworks
- Various Python versions (3.7+)
- Edge cases
- **Android devices** (if applicable)

Example test:
```bash
# Test on a simple script
python UNIVERSAL_CODE_VALIDATOR_V3.py examples/simple_script.py

# Test on a complex project
python UNIVERSAL_CODE_VALIDATOR_V3.py examples/django_project/

# Test interactive mode
python UNIVERSAL_CODE_VALIDATOR_V3.py
# Press Enter to test default behavior
```

## Commit Messages

Use clear, descriptive commit messages:

```
✅ Good:
- "Add support for detecting asyncio anti-patterns"
- "Fix false positive on type hints with 'eval' string"
- "Improve maintainability index calculation"
- "Update Android setup documentation"

❌ Bad:
- "Update code"
- "Fix bug"
- "Changes"
```

### Commit Message Format
```
[Type] Brief description

Detailed explanation of what and why (if needed)

Examples:
- [Feature] Add asyncio anti-pattern detection
- [Fix] Resolve false positive on type hints with 'eval'
- [Docs] Update Android setup guide
- [Refactor] Simplify complexity calculation logic
- [Test] Add test cases for role detection
```

## Issue Labels

We use these labels:
- `bug` - Something isn't working
- `enhancement` - New feature request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `android` - Android-specific issues
- `security` - Security-related
- `performance` - Performance improvements

## Testing on Android

If your changes affect mobile users, test on:
- Pydroid 3
- Termux
- Different Android versions

Report results in your PR:
```
Tested on:
- Pydroid 3 (Android 12) ✅
- Termux (Android 11) ✅
- Desktop Python 3.9 ✅
- Desktop Python 3.11 ✅
```

## Adding New Checks

When adding new validation checks:

1. **Add to appropriate analyzer class**
2. **Define clear severity levels**
3. **Include helpful suggestions**
4. **Test for false positives**
5. **Update documentation**
6. **Consider role-aware weighting**

Example:
```python
def check_new_pattern(self, node: ast.Node) -> None:
    """
    Check for [pattern name] anti-pattern.
    
    This detects when...
    """
    if self._is_bad_pattern(node):
        issue = Issue(
            type=IssueType.ANTI_PATTERN,
            severity=Severity.HIGH,
            message="Clear description of the problem",
            suggestion="How to fix it",
            file_path=self.file_path,
            line_number=node.lineno,
        )
        self.issues.append(issue)
```

## Adding New Role Types

If proposing a new code role:

1. **Justify the need** - Why is this role distinct?
2. **Define clear characteristics** - What makes code this role?
3. **Set appropriate thresholds** - Complexity ranges, etc.
4. **Update role weights** - How should rules be weighted?
5. **Provide examples** - Real code that fits this role
6. **Test extensively** - Ensure accurate detection

## Documentation

Update documentation when you:
- Add new features
- Change behavior
- Add new checks
- Fix bugs that users might encounter
- Modify Android compatibility

Files to update:
- `README.md` - Main documentation
- `QUICK_START.md` - If it affects getting started
- `ANDROID_SETUP.md` - If it affects Android users
- Code docstrings - Always!
- Changelog section in README

## Review Process

1. **Automated checks** run on your PR (if set up)
2. **Maintainer review** (usually within 48 hours)
3. **Address feedback** if needed
4. **Testing** on multiple platforms
5. **Approval** and merge

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards other contributors

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## Areas Needing Help

Current priorities:
- 🐛 Bug fixes for false positives
- 📱 Android-specific improvements
- 📚 Documentation improvements
- ✨ New pattern detections
- 🧪 Test case additions
- 🌍 Performance optimizations

## Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in documentation (for significant contributions)

## Getting Started Ideas

Good first contributions:
1. Fix typos in documentation
2. Add examples to README
3. Improve error messages
4. Add test cases
5. Report bugs with detailed reproduction steps
6. Suggest Android-specific features

## Questions?

- 💬 Open a [Discussion](https://github.com/goinboxme/universal-code-validator/discussions)
- 📧 Email: inbox.globaltrade@gmail.com
- 🐛 Check existing [Issues](https://github.com/goinboxme/universal-code-validator/issues)

## Thank You! 🙏

Every contribution matters:
- Reporting bugs 🐛
- Suggesting features 💡
- Improving docs 📚
- Writing code 💻
- Helping others 🤝
- Testing on different platforms 🧪

Thank you for making Universal Code Validator better!

---

**Happy Contributing! 🚀**
