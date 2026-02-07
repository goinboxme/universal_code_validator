# 🌟 Universal Code Validator v3.0

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Android-lightgrey.svg)]()
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen.svg)]()

**Comprehensive code quality analyzer untuk ANY Python project dengan Role-Aware Validation**

Universal Code Validator adalah tool analisis kode Python yang menggunakan AST (Abstract Syntax Tree) untuk mendeteksi masalah kualitas kode secara mendalam. Yang membuatnya unik adalah kemampuan **Role-Aware Validation** yang secara otomatis mendeteksi apakah kode Anda adalah SCRIPT, ENGINE, atau FRAMEWORK, lalu menyesuaikan metrik validasi sesuai konteks.

### 📱 **Cross-Platform Ready!**
Bekerja di **Desktop** (Windows/Linux/macOS) dan **Android** (Pydroid 3/Termux) - No external dependencies!

## ✨ Fitur Utama

### 🎯 Role-Aware Validation (NEW in v3.0)
- **Deteksi otomatis** peran kode: SCRIPT / ENGINE / FRAMEWORK dengan confidence score
- **Adaptive rule weighting** - Complexity penalty disesuaikan dengan role:
  - SCRIPT: Strict validation (weight 1.0x)
  - ENGINE: Balanced approach (weight 0.6-0.7x)
  - FRAMEWORK: Lenient on complexity (weight 0.3-0.4x)
- **Context-intelligent scoring** - Tidak ada false positive pada framework yang kompleks
- **Zero penalty** untuk kompleksitas yang memang diperlukan (lihat: UNIVERSAL_CODE_VALIDATOR_V3.py detected as FRAMEWORK = no complexity penalty!)

### 🔍 Comprehensive Analysis (AST-Based)
- ✅ **Syntax & Parsing** - Deteksi error sintaks sebelum runtime
- 🔒 **Security Vulnerabilities** - Context-aware (no false positives dari comments/strings)
  - `exec()` detection dengan severity scoring
  - Command injection patterns
  - Path traversal vulnerabilities
  - Pickle usage warnings
- 📊 **Complexity Metrics** - Role-normalized scoring
  - Cyclomatic complexity (per function)
  - Cognitive complexity (human readability)
  - Max nesting depth detection
- ⚡ **Performance Issues** - Deteksi bottleneck potensial
  - Inefficient loops
  - Repeated operations
  - Memory-intensive patterns
- 📝 **Code Quality** - PEP 8 & best practices
  - Function/class length violations
  - Parameter count warnings
  - Code duplication hints
- 📖 **Documentation Coverage** - Docstring analysis
  - Missing docstrings detection
  - Comment ratio calculation
- 🚫 **Anti-patterns** - Deteksi code smell
  - Empty except blocks ⭐ (see output: detects all empty excepts!)
  - God objects
  - Dead code
- 🔧 **Maintainability Index** - Halstead metrics calculation

### 📈 Advanced Metrics
- **Cyclomatic Complexity**: Independent code paths
- **Cognitive Complexity**: Mental effort to understand
- **Maintainability Index**: 0-100 scale (calculated per file)
- **Documentation Coverage**: Percentage of documented code
- **Security Risk Score**: Weighted by role
- **Role Classification Confidence**: 0-100%

### 🚀 Deployment Features
- ✅ **Zero Dependencies** - Pure Python stdlib only
- ✅ **Cross-Platform** - Windows/Linux/macOS/Android
- ✅ **Interactive Mode** - Perfect untuk mobile (no CLI args needed)
- ✅ **Batch Processing** - Analyze multiple files at once
- ✅ **Real-time Progress** - Streaming output saat analysis
- ✅ **Multiple Report Formats** - Console + HTML + JSON

## 🚀 Quick Start

### Instalasi

#### 🖥️ **Desktop (Windows/Linux/macOS)**
```bash
# Clone repository
git clone https://github.com/goinboxme/universal-code-validator.git
cd universal-code-validator

# Tidak perlu dependency eksternal - Pure Python!
python UNIVERSAL_CODE_VALIDATOR_V3.py
```

#### 📱 **Android (Pydroid 3 / Termux)**
```bash
# Di Termux
pkg install python git
git clone https://github.com/goinboxme/universal-code-validator.git
cd universal-code-validator
python UNIVERSAL_CODE_VALIDATOR_V3.py

# Di Pydroid 3
# Download file UNIVERSAL_CODE_VALIDATOR_V3.py
# Buka di Pydroid 3 dan run!
```

### Penggunaan

#### **Mode 1: Command Line Arguments**
```bash
# Analyze single file
python UNIVERSAL_CODE_VALIDATOR_V3.py myfile.py

# Analyze entire directory
python UNIVERSAL_CODE_VALIDATOR_V3.py /path/to/project

# Analyze current directory (where the script is located)
python UNIVERSAL_CODE_VALIDATOR_V3.py .
```

#### **Mode 2: Interactive Menu** (Perfect untuk Android!)
```bash
# Run tanpa arguments untuk menu interaktif
python UNIVERSAL_CODE_VALIDATOR_V3.py

# Anda akan melihat:
╔════════════════════════════════════════════════════════════════╗
║           🌟 UNIVERSAL CODE VALIDATOR v3.0.0 🌟              ║
║                                                               ║
║     Analyze ANY Python code without prior knowledge           ║
║   Now with ROLE-AWARE VALIDATION - Context-Intelligent!      ║
╚════════════════════════════════════════════════════════════════╝

Usage options:
  1. Analyze single file:    python validator.py myfile.py
  2. Analyze directory:      python validator.py /path/to/project
  3. Analyze current dir:    python validator.py .

Enter file or directory path (or '.' for current): 

# Ketik '.' untuk scan folder saat ini
# Atau ketik nama file: mycode.py
# Atau ketik path lengkap: /sdcard/projects/myapp.py
```

## 📊 Output & Reports

Validator menghasilkan 3 jenis output:

### 1. **Real-time Console Output** (Streaming Progress)
```
🔍 Scanning for Python files in: .
📁 Found 13 Python file(s)

================================================================================
🔬 ANALYZING FILES
================================================================================

[1/13] Analyzing: ENGINEERING_MASTER.py
    🎯 Detected Role: SCRIPT (confidence: 70%)
    🟠 2 HIGH priority issue(s)
    📊 Maintainability: 40.0/100

[2/13] Analyzing: AI_CTE_ASSIST.py
    🎯 Detected Role: SCRIPT (confidence: 70%)
    ✅ No issues found
    📊 Maintainability: 61.0/100

[11/13] Analyzing: UNIVERSAL_CODE_VALIDATOR_V3.py
    🎯 Detected Role: FRAMEWORK (confidence: 100%)
    📊 Maintainability: 39.6/100

================================================================================
📊 ANALYSIS SUMMARY
================================================================================

📁 Project: .
📅 Timestamp: 2026-02-07T18:59:22
🆕 Validator Version: 3.0.0
📝 Files Analyzed: 13
📏 Total Lines: 14,968

🎯 Role Distribution:
   FRAMEWORK: 3 file(s) (23%)
   SCRIPT: 10 file(s) (77%)

🎯 Overall Score: 31.6/100 (Role-Normalized)
🏆 Grade: D - NEEDS IMPROVEMENT

🐛 Issues Found:
   Total: 322
   🔴 Critical: 2
   🟠 High: 18

📊 Metrics:
   Functions: 521
   Classes: 108
   Avg Complexity: 3.68
   Avg Maintainability: 42.7/100

🔒 Security: 11 issue(s)
⚡ Performance: 27 issue(s)
🔄 Complexity: 101 issue(s)

================================================================================
🎯 ROLE-SPECIFIC INSIGHTS
================================================================================

📄 MINI_AI_AGENT_V6.py
   Role: SCRIPT (confidence: 70%)
   Expected Complexity: LOW
   Actual Complexity: 44.0
   Verdict: ABOVE expected range
   Reasoning:
     • SCRIPT: Linear utility/helper code
     • Simple structure (45 functions, 4 classes)
     • LOC: 1281
   Issues (role-adjusted): 18

📄 UNIVERSAL_CODE_VALIDATOR_V3.py
   Role: FRAMEWORK (confidence: 100%)
   Expected Complexity: HIGH
   Actual Complexity: 21.0
   Verdict: WITHIN expected range ✅
   Reasoning:
     • FRAMEWORK: Meta-analyzer/orchestrator pattern detected
     • Multiple visitor/analyzer patterns detected (11)
     • Very high max complexity (21)
   Issues (role-adjusted): 69

================================================================================
🔴 TOP CRITICAL/HIGH ISSUES
================================================================================

🔴 CRITICAL Security Vulnerability
   📄 MINI_AI_AGENT_V5.py:631
   ❗ Using exec() can execute arbitrary code
   ⚖️  Role-adjusted weight: 0.8x
   💡 Refactor to avoid exec()

🟠 HIGH Anti-pattern
   📄 AI_PATTERN_ANALYZER.py:250
   ❗ Empty except block silently ignores errors
   💡 Log the error or handle it appropriately

================================================================================
💡 RECOMMENDATIONS
================================================================================

🔴 URGENT: Fix critical issues immediately!
🔒 Security: Address 11 security issue(s)

✅ Next Steps:
   1. Review the HTML report in your browser
   2. Check role classifications - are they accurate?
   3. Fix critical and high priority issues first
   4. Run the validator again to track improvements

================================================================================
✨ Analysis Complete!
================================================================================
```

### 2. **HTML Report** (Interactive Dashboard)
- 📊 Visual dashboard dengan role distribution chart
- 📄 Per-file role analysis dengan confidence score
- 🎨 Color-coded issue severity (Critical/High/Medium/Low)
- ⚖️ Role-adjusted weight indicators
- 💡 Detailed metrics & actionable suggestions
- 🖥️ Dapat dibuka di browser desktop atau Android

**File generated**: `code_analysis_YYYYMMDD_HHMMSS.html`

### 3. **JSON Report** (Machine-readable)
```json
{
  "project_path": ".",
  "timestamp": "2026-02-07T18:59:22",
  "validator_version": "3.0.0",
  "total_files": 13,
  "total_lines": 14968,
  "role_distribution": {
    "FRAMEWORK": 3,
    "SCRIPT": 10
  },
  "overall_score": 31.6,
  "critical_issues": 2,
  "high_issues": 18,
  "file_analyses": [...]
}
```

**File generated**: `code_analysis_YYYYMMDD_HHMMSS.json`
- ✅ Perfect untuk CI/CD integration
- ✅ Easy parsing untuk automated workflows
- ✅ Version control friendly

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
- Platform: **Linux, Windows, macOS, Android (Termux/Pydroid 3)**

### ✅ Tested On:
- ✅ Ubuntu 20.04+ / Debian / Fedora
- ✅ Windows 10/11
- ✅ macOS 11+ (Big Sur and later)
- ✅ Android 7+ with Termux
- ✅ Android 7+ with Pydroid 3

## 📱 Android-Specific Tips

### **Termux Setup**
```bash
# Install Python dan Git
pkg update && pkg upgrade
pkg install python git

# Clone dan run
git clone https://github.com/goinboxme/universal-code-validator.git
cd universal-code-validator
python UNIVERSAL_CODE_VALIDATOR_V3.py .
```

### **Pydroid 3 Setup**
1. Download `UNIVERSAL_CODE_VALIDATOR_V3.py` dari GitHub
2. Simpan di folder yang sama dengan kode Anda
3. Buka di Pydroid 3
4. Tap **Run** (▶️)
5. Input: ketik `.` untuk scan folder saat ini

### **Path Tips untuk Android**
```bash
# Current directory (recommended)
.

# Specific file in same folder
mycode.py

# Internal storage
/sdcard/projects/myapp.py

# Termux home
/data/data/com.termux/files/home/projects/

# Pydroid 3 directory
/storage/emulated/0/Pydroid/
```

### **Viewing HTML Reports on Android**
```bash
# Setelah analysis selesai:
# File: code_analysis_YYYYMMDD_HHMMSS.html

# Cara 1: File Manager
# Buka dengan Chrome/Firefox/browser apapun

# Cara 2: Termux (with termux-open)
pkg install termux-tools
termux-open code_analysis_*.html

# Cara 3: Share file HTML ke desktop via:
# - Google Drive / Dropbox
# - Email attachment
# - USB transfer
```

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

### 1. **Mobile Development on Android** ⭐
```bash
# Di Termux atau Pydroid 3
python UNIVERSAL_CODE_VALIDATOR_V3.py .

# Perfect untuk:
# - Learning Python on the go
# - Quick code quality checks
# - Coding practice validation
# - Portfolio project assessment
```

### 2. Pre-commit Hook (Desktop)
```bash
# .git/hooks/pre-commit
#!/bin/bash
python UNIVERSAL_CODE_VALIDATOR_V3.py . --json-only
if [ $? -ne 0 ]; then
    echo "Code quality check failed!"
    exit 1
fi
```

### 3. CI/CD Integration
```yaml
# .github/workflows/code-quality.yml
- name: Code Quality Check
  run: |
    python UNIVERSAL_CODE_VALIDATOR_V3.py . --json-only
```

### 4. Code Review Automation (Desktop/Android)
```bash
# Desktop: Review specific files
git diff --name-only main | grep '\.py$' | xargs python UNIVERSAL_CODE_VALIDATOR_V3.py

# Android: Quick check before committing
python UNIVERSAL_CODE_VALIDATOR_V3.py mychanged_file.py
```

### 5. Learning & Education
```bash
# Perfect untuk mahasiswa/pelajar yang coding di Android
# - Check homework assignments
# - Validate practice exercises
# - Learn best practices
# - Prepare for code reviews
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

- **Author**: [goinboxme]
- **Email**: inbox.globaltrade@gmail.com
- **GitHub**: [@goinboxme](https://github.com/goinboxme)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

## ❓ FAQ

### **Q: Bisa dijalankan di Android?**
A: Ya! 100% compatible dengan Termux dan Pydroid 3. Tidak perlu root atau dependencies eksternal.

### **Q: Apakah perlu install library tambahan?**
A: Tidak sama sekali. Pure Python standard library - langsung run!

### **Q: Apa bedanya dengan pylint/flake8?**
A: 
- ✅ Role-aware validation (unique feature!)
- ✅ Zero dependencies vs puluhan dependencies
- ✅ Cross-platform termasuk Android
- ✅ Context-intelligent scoring
- ✅ Interactive mode untuk mobile

### **Q: File HTML report tidak bisa dibuka di Android?**
A: Bisa! Gunakan file manager, pilih file HTML, buka dengan Chrome/Firefox. Atau gunakan `termux-open` di Termux.

### **Q: Kenapa script saya dapat score rendah?**
A: Check "Role Classification" - jika salah deteksi (misal: ENGINE detected as SCRIPT), complexity penalty jadi terlalu tinggi. Ini normal untuk code yang memang complex by design.

### **Q: Apa arti "role-adjusted weight"?**
A: Ini multiplier yang diterapkan ke severity issue berdasarkan role:
- SCRIPT: 1.0x (full penalty)
- ENGINE: 0.6-0.7x (reduced penalty)  
- FRAMEWORK: 0.3-0.5x (minimal penalty)

### **Q: Bisa analyze project dengan 1000+ files?**
A: Ya, tapi butuh waktu. Untuk project besar, consider analyze per module/package.

### **Q: Report JSON untuk apa?**
A: Untuk:
- CI/CD automation
- Trend tracking (compare JSON across commits)
- Custom dashboard integration
- Automated quality gates

### **Q: Confidence 70% vs 100% itu artinya?**
A: 
- 100% = Pasti (detected visitor pattern, high complexity)
- 70% = Probably (default untuk simple scripts)
- Lower confidence = might need manual review

---

**Made with ❤️ and Python - Runs Everywhere!**
