# 🌟 Universal Code Validator v3.0

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen.svg)]()

**Comprehensive code quality analyzer untuk ANY Python project dengan Role-Aware Validation**

Universal Code Validator adalah tool analisis kode Python yang menggunakan AST (Abstract Syntax Tree) untuk mendeteksi masalah kualitas kode secara mendalam. Yang membuatnya unik adalah kemampuan **Role-Aware Validation** yang secara otomatis mendeteksi apakah kode Anda adalah SCRIPT, ENGINE, atau FRAMEWORK, lalu menyesuaikan metrik validasi sesuai konteks.

## ✨ Fitur Utama

### 🎯 Role-Aware Validation (NEW in v3.0)
- **Deteksi otomatis** peran kode: SCRIPT / ENGINE / FRAMEWORK
- **Adaptive rule weighting** berdasarkan purpose kode
- **Context-intelligent scoring** - tidak ada false positive pada framework yang kompleks
- **Zero penalty** untuk kompleksitas yang memang diperlukan

### 🔍 Comprehensive Analysis
- ✅ **Syntax & Parsing** - Deteksi error sintaks
- 🔒 **Security Vulnerabilities** - AST-based, context-aware
- 📊 **Complexity Metrics** - Cyclomatic & cognitive complexity
- ⚡ **Performance Issues** - Deteksi bottleneck potensial
- 📝 **Code Quality** - PEP 8, best practices
- 📖 **Documentation Coverage** - Docstring analysis
- 🚫 **Anti-patterns** - Deteksi code smell
- 🔧 **Maintainability Index** - Halstead metrics

### 📈 Advanced Metrics
- Cyclomatic Complexity
- Cognitive Complexity
- Maintainability Index
- Documentation Coverage
- Security Risk Score
- Role Classification Confidence

## 🚀 Quick Start

### Instalasi

```bash
# Clone repository
git clone https://github.com/yourusername/universal-code-validator.git
cd universal-code-validator

# Tidak perlu dependency eksternal - Pure Python!
python UNIVERSAL_CODE_VALIDATOR_V3.py
```

### Penggunaan Dasar

```bash
# Analyze single file
python UNIVERSAL_CODE_VALIDATOR_V3.py myfile.py

# Analyze entire directory
python UNIVERSAL_CODE_VALIDATOR_V3.py /path/to/project

# Analyze current directory
python UNIVERSAL_CODE_VALIDATOR_V3.py .
```

## 📊 Output & Reports

Validator menghasilkan 2 jenis report:

### 1. Console Output (Real-time)
```
╔════════════════════════════════════════════════════════════════╗
║           🌟 UNIVERSAL CODE VALIDATOR v3.0 🌟                ║
╚════════════════════════════════════════════════════════════════╝

📊 ANALYSIS RESULTS
==================================================================
📁 Target: my_project/
📄 Files analyzed: 5
⏱️  Duration: 2.34s

🎯 ROLE DISTRIBUTION
==================================================================
  SCRIPT: 2 files (40%)
  ENGINE: 2 files (40%)
  FRAMEWORK: 1 file (20%)
```

### 2. HTML Report (Interactive)
- Visual dashboard dengan charts
- Per-file role analysis dengan confidence score
- Color-coded issue severity
- Role-adjusted weight indicators
- Detailed metrics & suggestions

### 3. JSON Report (Machine-readable)
- Structured data untuk CI/CD integration
- Semua metrics & issues dalam format JSON
- Easy parsing untuk automated workflows

## 🎯 Role Classification Explained

### SCRIPT (Linear Utilities)
- **Karakteristik**: Simple, sequential logic
- **Contoh**: CLI tools, helper scripts, utilities
- **Validasi**: Strict pada complexity & maintainability

### ENGINE (Logic-Heavy Systems)
- **Karakteristik**: State management, complex algorithms
- **Contoh**: Data processors, game engines, business logic
- **Validasi**: Balanced approach, fokus pada security

### FRAMEWORK (Meta-Analyzers)
- **Karakteristik**: Visitor patterns, high abstraction
- **Contoh**: Code analyzers, compilers, orchestrators
- **Validasi**: Lenient pada complexity, strict pada security

## 📋 Requirements

- Python 3.7+
- **No external dependencies!** (Pure Python standard library)

## 🛠️ Configuration

Edit `THRESHOLDS` dan `ROLE_WEIGHTS` di dalam script untuk menyesuaikan:

```python
THRESHOLDS = {
    'max_function_length': 50,
    'max_class_length': 300,
    'max_cyclomatic_complexity': 10,
    'max_cognitive_complexity': 15,
    'max_nesting_depth': 4,
    'max_parameters': 5,
    'min_maintainability_index': 20,
    'min_comment_ratio': 0.10,
    'min_docstring_coverage': 0.50,
}
```

## 💡 Use Cases

### 1. Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
python UNIVERSAL_CODE_VALIDATOR_V3.py . --json-only
if [ $? -ne 0 ]; then
    echo "Code quality check failed!"
    exit 1
fi
```

### 2. CI/CD Integration
```yaml
# .github/workflows/code-quality.yml
- name: Code Quality Check
  run: |
    python UNIVERSAL_CODE_VALIDATOR_V3.py . --json-only
```

### 3. Code Review Automation
```bash
# Review PR changes
git diff --name-only main | grep '\.py$' | xargs python UNIVERSAL_CODE_VALIDATOR_V3.py
```

## 📸 Screenshots

### Console Output
![Console Analysis](docs/screenshots/console.png)

### HTML Report
![HTML Dashboard](docs/screenshots/html-report.png)

### Role Classification
![Role Analysis](docs/screenshots/role-classification.png)

## 🤝 Contributing

Contributions are welcome! Silakan:

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## 📝 Changelog

### v3.0.0 (Latest)
- ✨ **NEW**: Role-Aware Validation system
- ✨ **NEW**: Adaptive rule weighting
- ✨ **NEW**: Context-intelligent scoring
- 🐛 Fixed: Zero false positives on framework complexity

### v2.1
- ✨ Context-aware security scanning (AST-based)
- 🐛 Eliminated false positives from strings/comments
- 🐛 Duplicate issue detection prevention

### v2.0
- Complete rewrite with AST-based analysis
- Added multiple report formats
- Enhanced metric calculations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by tools like pylint, flake8, and radon
- Built with Python's powerful `ast` module
- Thanks to the open-source community

## 📧 Contact

- **Author**: [Your Name]
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ and Python**
