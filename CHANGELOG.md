# Changelog

All notable changes to Universal Code Validator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-02-07

### 🎯 Major Release - Role-Aware Validation System

This is a **major update** that fundamentally changes how code quality is assessed, introducing context-intelligent scoring that eliminates false positives on framework and engine code.

### ✨ Added
- **Role-Aware Validation System**
  - Automatic code role detection (SCRIPT/ENGINE/FRAMEWORK)
  - Context-intelligent scoring normalization
  - Adaptive rule weighting based on code purpose
  - Expected complexity ranges for each role type
  
- **Enhanced Role Classification**
  - Visitor pattern detection for framework identification
  - Logic-utility ratio analysis
  - Structural profiling system
  - Confidence scoring for role assignments
  
- **Role-Specific Insights**
  - Per-file role analysis in reports
  - Complexity verdict (BELOW/WITHIN/ABOVE expected)
  - Role-adjusted issue weights
  - Reasoning explanations for classifications

### 🔧 Changed
- **Scoring Algorithm**
  - Overall score is now role-normalized
  - Frameworks no longer penalized for natural complexity
  - Scripts held to stricter simplicity standards
  - Engines receive balanced treatment
  
- **Issue Reporting**
  - Issues now include role-adjusted weights
  - Priority calculations account for code role
  - Security rules have role-specific multipliers
  
- **HTML Reports**
  - Added role distribution visualization
  - Per-file role insights section
  - Role-aware complexity verdicts
  - Enhanced visual indicators

### 🐛 Fixed
- Zero false positives on legitimate framework complexity
- Eliminated inappropriate warnings for meta-analyzers
- Fixed scoring bias against architectural patterns
- Improved accuracy of issue prioritization

### 📱 Android Support
- Full compatibility with Pydroid 3
- Full compatibility with Termux
- Interactive mode works perfectly on mobile
- No external dependencies required

---

## [2.1.0] - 2026-01-15

### ✨ Added
- **Context-Aware Security Scanning**
  - AST-based security analysis
  - Eliminated false positives from strings
  - Eliminated false positives from comments
  - Proper node type validation
  
- **Duplicate Detection**
  - Issue deduplication system
  - Hash-based issue comparison
  - Prevents duplicate warnings

### 🔧 Changed
- Security checks now inspect actual code nodes only
- Improved regex pattern matching accuracy
- Enhanced issue equality checking

### 🐛 Fixed
- False positives on SQL queries in string literals
- False positives on 'exec' in documentation
- False positives on 'eval' in comments
- Duplicate issues in reports

---

## [2.0.0] - 2025-12-01

### 🎉 Initial Public Release

### ✨ Added
- **Core Analysis Features**
  - Syntax and parsing validation
  - Security vulnerability detection
  - Complexity metrics (cyclomatic & cognitive)
  - Performance issue detection
  - Code quality analysis
  - Best practices checking
  - Documentation coverage analysis
  - Anti-pattern detection
  - Maintainability index calculation

- **Multiple Output Formats**
  - Colored terminal output
  - JSON reports
  - HTML reports with visualizations

- **Comprehensive Metrics**
  - Halstead metrics
  - Nesting depth analysis
  - Function and class size metrics
  - Comment ratio calculations

- **Security Checks**
  - SQL injection detection
  - Command injection detection
  - Path traversal detection
  - Dangerous function usage (eval, exec, pickle)
  - Hardcoded credentials detection

### 📚 Documentation
- Comprehensive README
- Usage examples
- Configuration guide

---

## [1.0.0] - 2025-11-01 [Internal Beta]

### ✨ Added
- Initial proof of concept
- Basic AST parsing
- Simple complexity metrics
- Console output only

---

## Upcoming Features

### 🔮 Planned for v3.1.0
- [ ] Support for type hint analysis
- [ ] Async/await pattern detection
- [ ] Custom rule configuration files
- [ ] Integration with popular IDEs
- [ ] CI/CD pipeline examples

### 🔮 Planned for v3.2.0
- [ ] Multi-language support (JavaScript, TypeScript)
- [ ] Team collaboration features
- [ ] Historical trend analysis
- [ ] Code smell detection improvements

### 🔮 Planned for v4.0.0
- [ ] Machine learning-based pattern detection
- [ ] Auto-fix suggestions with code generation
- [ ] Real-time analysis mode
- [ ] Cloud-based team dashboards

---

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

---

## Migration Guides

### Migrating from v2.x to v3.0

**Breaking Changes:**
- None! v3.0 is fully backwards compatible

**New Features:**
- Role detection runs automatically - no action needed
- Scores may change due to role-aware normalization (usually improving)
- HTML reports include new role insights section

**Recommendations:**
- Review role classifications in your first run
- Check if any files are misclassified (rare)
- Enjoy more accurate scoring! 🎉

### Migrating from v1.x to v2.0

**Breaking Changes:**
- Output format changed slightly in JSON reports
- Some security check behavior improved

**New Features:**
- Context-aware scanning eliminates false positives
- Duplicate detection prevents noise

**Recommendations:**
- Re-run analysis on your codebase
- Compare results with v1.x
- Report any regressions

---

## Support

Having issues with a specific version?
- Check the documentation for that version
- Search [closed issues](https://github.com/goinboxme/universal-code-validator/issues?q=is%3Aissue+is%3Aclosed)
- Open a new issue with version information

---

**Last Updated:** 2026-02-07
