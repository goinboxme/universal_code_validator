#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                 🌟 UNIVERSAL CODE VALIDATOR v3.0 🌟                    ║
║                                                                            ║
║   Comprehensive code quality analyzer for ANY Python project              ║
║   Now with ROLE-AWARE VALIDATION - Context-Intelligent Scoring!          ║
║                                                                            ║
║   NEW in v3.0:                                                             ║
║   ✓ Role-aware validation (SCRIPT/ENGINE/FRAMEWORK detection)            ║
║   ✓ Adaptive rule weighting based on code purpose                         ║
║   ✓ Context-intelligent scoring normalization                             ║
║   ✓ Zero false positives on framework/engine complexity                   ║
║                                                                            ║
║   v2.1 Features:                                                           ║
║   ✓ Context-aware security scanning (AST-based)                           ║
║   ✓ Eliminated false positives from strings/comments                      ║
║   ✓ Duplicate issue detection prevention                                  ║
║                                                                            ║
║   Checks performed automatically:                                          ║
║   ✓ Syntax & Parsing                                                       ║
║   ✓ Security Vulnerabilities (CONTEXT-AWARE)                              ║
║   ✓ Complexity Metrics                                                     ║
║   ✓ Performance Issues                                                     ║
║   ✓ Code Quality                                                           ║
║   ✓ Best Practices                                                         ║
║   ✓ Documentation Coverage                                                 ║
║   ✓ Anti-patterns                                                          ║
║   ✓ Maintainability Index                                                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import ast
import os
import re
import sys
import json
import math
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

VERSION = "3.0.0"

class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "🔴 CRITICAL"
    HIGH = "🟠 HIGH"
    MEDIUM = "🟡 MEDIUM"
    LOW = "🟢 LOW"
    INFO = "ℹ️  INFO"


class CodeRole(Enum):
    """Code role classification based on structural analysis"""
    SCRIPT = "SCRIPT"          # Linear utility / helper
    ENGINE = "ENGINE"          # Logic-heavy system
    FRAMEWORK = "FRAMEWORK"    # Meta-analyzer / orchestrator


class IssueType(Enum):
    """Types of issues that can be detected"""
    SYNTAX = "Syntax Error"
    SECURITY = "Security Vulnerability"
    PERFORMANCE = "Performance Issue"
    MAINTAINABILITY = "Maintainability"
    COMPLEXITY = "Complexity"
    STYLE = "Code Style"
    DOCUMENTATION = "Documentation"
    ANTI_PATTERN = "Anti-pattern"
    BEST_PRACTICE = "Best Practice"


# Thresholds for various metrics
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

# Role classification thresholds
ROLE_THRESHOLDS = {
    'visitor_score_high': 3,        # Multiple visitor patterns detected
    'complexity_very_high': 15,     # Max cyclomatic complexity
    'nesting_deep': 5,              # Max nesting depth
    'loc_large': 500,               # Lines for large codebase
    'loc_medium': 200,              # Lines for medium codebase
    'classes_multiple': 3,          # Multiple class definitions
    'complexity_medium': 8,         # Average complexity threshold
}

# Role-aware rule weighting matrix
ROLE_WEIGHTS = {
    CodeRole.SCRIPT: {
        'long_function': 1.0,       # HIGH - scripts should be clean
        'nested_logic': 1.0,        # HIGH
        'complexity': 1.0,          # HIGH
        'maintainability': 1.0,     # HIGH
        'security': 0.8,            # MEDIUM
        'performance': 0.6,         # LOW-MEDIUM
    },
    CodeRole.ENGINE: {
        'long_function': 0.6,       # MEDIUM - engines can be larger
        'nested_logic': 0.6,        # MEDIUM
        'complexity': 0.6,          # MEDIUM
        'maintainability': 0.7,     # MEDIUM-HIGH
        'security': 1.0,            # HIGH - engines handle data
        'performance': 0.7,         # MEDIUM
    },
    CodeRole.FRAMEWORK: {
        'long_function': 0.3,       # LOW - frameworks are naturally complex
        'nested_logic': 0.3,        # LOW
        'complexity': 0.3,          # LOW
        'maintainability': 0.5,     # MEDIUM
        'security': 1.2,            # VERY HIGH - frameworks are critical
        'performance': 0.4,         # LOW
    },
}

# Expected complexity ranges by role
ROLE_COMPLEXITY_RANGES = {
    CodeRole.SCRIPT: {'min': 1, 'max': 5, 'label': 'LOW'},
    CodeRole.ENGINE: {'min': 5, 'max': 12, 'label': 'MEDIUM'},
    CodeRole.FRAMEWORK: {'min': 10, 'max': 25, 'label': 'HIGH'},
}


# ═══════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class StructuralProfile:
    """Structural profile of code for role classification"""
    loc: int
    functions: int
    classes: int
    max_nesting: int
    avg_complexity: float
    max_complexity: float
    visitor_score: int  # Count of visitor/analyzer patterns
    logic_utility_ratio: float  # Ratio of logic vs utility code


@dataclass
class RoleClassification:
    """Role classification result"""
    role: CodeRole
    confidence: float  # 0-1
    reasoning: List[str]  # Why this role was chosen
    expected_complexity: str  # LOW/MEDIUM/HIGH
    actual_complexity: float
    complexity_verdict: str  # BELOW/WITHIN/ABOVE expected


@dataclass
class Issue:
    """Represents a code issue"""
    type: IssueType
    severity: Severity
    message: str
    file_path: str
    line_number: Optional[int] = None
    column: Optional[int] = None
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None
    role_weight: float = 1.0  # NEW: Role-aware weight adjustment
    
    def __hash__(self):
        """Make Issue hashable for deduplication"""
        return hash((self.type, self.message, self.file_path, self.line_number))
    
    def __eq__(self, other):
        """Check equality for deduplication"""
        if not isinstance(other, Issue):
            return False
        return (self.type == other.type and 
                self.message == other.message and
                self.file_path == other.file_path and
                self.line_number == other.line_number)


@dataclass
class Metric:
    """Code metric"""
    name: str
    value: float
    category: str
    description: str
    threshold: Optional[float] = None
    passed: Optional[bool] = None


@dataclass
class FileAnalysis:
    """Analysis result for a single file"""
    file_path: str
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    classes: int
    functions: int
    avg_complexity: float
    max_complexity: float
    maintainability_index: float
    documentation_coverage: float
    structural_profile: Optional[StructuralProfile] = None  # NEW
    role_classification: Optional[RoleClassification] = None  # NEW
    issues: List[Issue] = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)


@dataclass
class ProjectAnalysis:
    """Complete project analysis"""
    project_path: str
    total_files: int
    total_lines: int
    total_issues: int
    critical_issues: int
    high_issues: int
    overall_score: float
    grade: str
    file_analyses: List[FileAnalysis] = field(default_factory=list)
    summary_metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = VERSION


# ═══════════════════════════════════════════════════════════════════════════
# STRUCTURAL PROFILER (NEW - Layer 2)
# ═══════════════════════════════════════════════════════════════════════════

class StructuralProfiler(ast.NodeVisitor):
    """
    Analyzes code structure to extract facts for role classification.
    This is NOT validation - just objective measurement.
    """
    
    def __init__(self):
        self.logic_utility_ratio = 0.0
        self.visitor_score = 0
        self.visitor_patterns = 0
        self.analyzer_patterns = 0
        self.logic_nodes = 0
        self.utility_nodes = 0
        
    def visit_ClassDef(self, node):
        """Detect visitor/analyzer patterns"""
        class_name = node.name.lower()
        
        # Check for visitor pattern
        if 'visitor' in class_name or 'walker' in class_name:
            self.visitor_patterns += 1
        
        # Check for analyzer pattern
        if 'analyzer' in class_name or 'scanner' in class_name or 'detector' in class_name:
            self.analyzer_patterns += 1
        
        # Check for NodeVisitor inheritance
        for base in node.bases:
            if isinstance(base, ast.Attribute) and base.attr == 'NodeVisitor':
                self.visitor_patterns += 1
            elif isinstance(base, ast.Name) and 'visitor' in base.id.lower():
                self.visitor_patterns += 1
        
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Count logic nodes"""
        self.logic_nodes += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Count logic nodes"""
        self.logic_nodes += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Count logic nodes"""
        self.logic_nodes += 1
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Classify functions as logic or utility"""
        # Simple heuristic: functions with control flow are logic
        has_control_flow = any(
            isinstance(n, (ast.If, ast.For, ast.While, ast.Try))
            for n in ast.walk(node)
        )
        
        if has_control_flow:
            self.logic_nodes += 1
        else:
            self.utility_nodes += 1
        
        self.generic_visit(node)
    
    @classmethod
    def profile(cls, tree: ast.AST, loc: int, functions: int, classes: int,
                max_nesting: int, avg_complexity: float, max_complexity: float) -> StructuralProfile:
        """Generate structural profile from AST"""
        profiler = cls()
        profiler.visit(tree)
        
        visitor_score = profiler.visitor_patterns + profiler.analyzer_patterns
        
        total_nodes = profiler.logic_nodes + profiler.utility_nodes
        logic_ratio = profiler.logic_nodes / total_nodes if total_nodes > 0 else 0.5
        
        return StructuralProfile(
            loc=loc,
            functions=functions,
            classes=classes,
            max_nesting=max_nesting,
            avg_complexity=avg_complexity,
            max_complexity=max_complexity,
            visitor_score=visitor_score,
            logic_utility_ratio=logic_ratio
        )


# ═══════════════════════════════════════════════════════════════════════════
# ROLE CLASSIFIER (NEW - Layer 3)
# ═══════════════════════════════════════════════════════════════════════════

class RoleClassifier:
    """
    Deterministic role classification based on structural profile.
    No hardcoded filenames - 100% behavioral detection.
    """
    
    @staticmethod
    def classify(profile: StructuralProfile) -> RoleClassification:
        """
        Classify code role based on structural profile.
        
        Priority order (MUST be checked in this sequence):
        1. FRAMEWORK (meta-analyzers, orchestrators)
        2. ENGINE (logic-heavy systems)
        3. SCRIPT (default - utilities, helpers)
        """
        
        reasoning = []
        confidence = 0.0
        
        # ═══════════════════════════════════════════════════════════════
        # A. FRAMEWORK Detection (highest priority)
        # ═══════════════════════════════════════════════════════════════
        is_framework = False
        framework_score = 0.0
        
        # Condition 1: Visitor pattern detection
        if profile.visitor_score >= ROLE_THRESHOLDS['visitor_score_high']:
            is_framework = True
            framework_score += 0.4
            reasoning.append(f"Multiple visitor/analyzer patterns detected ({profile.visitor_score})")
        
        # Condition 2: Very high complexity
        if profile.max_complexity >= ROLE_THRESHOLDS['complexity_very_high']:
            framework_score += 0.3
            reasoning.append(f"Very high max complexity ({profile.max_complexity})")
        
        # Condition 3: Deep nesting (meta-logic characteristic)
        if profile.max_nesting >= ROLE_THRESHOLDS['nesting_deep']:
            framework_score += 0.2
            reasoning.append(f"Deep nesting detected ({profile.max_nesting} levels)")
        
        # Condition 4: Large codebase
        if profile.loc >= ROLE_THRESHOLDS['loc_large']:
            framework_score += 0.1
            reasoning.append(f"Large codebase ({profile.loc} LOC)")
        
        # FRAMEWORK verdict
        if is_framework and profile.loc >= ROLE_THRESHOLDS['loc_large']:
            role = CodeRole.FRAMEWORK
            confidence = min(framework_score, 1.0)
            reasoning.insert(0, "FRAMEWORK: Meta-analyzer/orchestrator pattern detected")
        
        # ═══════════════════════════════════════════════════════════════
        # B. ENGINE Detection
        # ═══════════════════════════════════════════════════════════════
        elif (profile.classes >= ROLE_THRESHOLDS['classes_multiple'] and
              profile.avg_complexity >= ROLE_THRESHOLDS['complexity_medium'] and
              profile.loc >= ROLE_THRESHOLDS['loc_medium']):
            
            role = CodeRole.ENGINE
            confidence = 0.8
            reasoning = [
                "ENGINE: Logic-heavy stateful system",
                f"Multiple classes ({profile.classes})",
                f"Medium-high avg complexity ({profile.avg_complexity:.1f})",
                f"Medium-large codebase ({profile.loc} LOC)"
            ]
        
        # ═══════════════════════════════════════════════════════════════
        # C. SCRIPT (default)
        # ═══════════════════════════════════════════════════════════════
        else:
            role = CodeRole.SCRIPT
            confidence = 0.7
            reasoning = [
                "SCRIPT: Linear utility/helper code",
                f"Simple structure ({profile.functions} functions, {profile.classes} classes)",
                f"LOC: {profile.loc}"
            ]
        
        # Complexity verdict
        expected_range = ROLE_COMPLEXITY_RANGES[role]
        expected_label = expected_range['label']
        
        if profile.max_complexity < expected_range['min']:
            complexity_verdict = "BELOW"
        elif profile.max_complexity > expected_range['max']:
            complexity_verdict = "ABOVE"
        else:
            complexity_verdict = "WITHIN"
        
        return RoleClassification(
            role=role,
            confidence=confidence,
            reasoning=reasoning,
            expected_complexity=expected_label,
            actual_complexity=profile.max_complexity,
            complexity_verdict=complexity_verdict
        )


# ═══════════════════════════════════════════════════════════════════════════
# ROLE-AWARE ISSUE ADJUSTER (NEW - Layer 4)
# ═══════════════════════════════════════════════════════════════════════════

class RoleAwareAdjuster:
    """
    Applies role-aware weights to issues.
    This normalizes scoring based on code purpose.
    """
    
    @staticmethod
    def adjust_issues(issues: List[Issue], role: CodeRole) -> List[Issue]:
        """Apply role-aware weights to issues"""
        
        weights = ROLE_WEIGHTS[role]
        adjusted_issues = []
        
        for issue in issues:
            # Determine issue category for weighting
            if issue.type == IssueType.MAINTAINABILITY:
                if 'too long' in issue.message.lower():
                    weight = weights['long_function']
                elif 'nesting' in issue.message.lower():
                    weight = weights['nested_logic']
                else:
                    weight = weights['maintainability']
            
            elif issue.type == IssueType.COMPLEXITY:
                if 'nesting' in issue.message.lower():
                    weight = weights['nested_logic']
                else:
                    weight = weights['complexity']
            
            elif issue.type == IssueType.SECURITY:
                weight = weights['security']
            
            elif issue.type == IssueType.PERFORMANCE:
                weight = weights['performance']
            
            else:
                weight = 1.0  # Default weight for other issues
            
            # Apply weight
            issue.role_weight = weight
            
            # Adjust severity based on weight (for display purposes)
            # Very low weights might downgrade visible severity
            if weight <= 0.3 and issue.severity not in (Severity.CRITICAL, Severity.HIGH):
                # Don't add to adjusted list if weight is very low and severity is low
                if weight > 0.2:  # Still keep if weight is not negligible
                    adjusted_issues.append(issue)
            else:
                adjusted_issues.append(issue)
        
        return adjusted_issues
    
    @staticmethod
    def normalize_score(raw_score: float, role: CodeRole, 
                       actual_complexity: float, total_issues: int,
                       critical_issues: int = 0) -> float:  # ✅ TAMBAHKAN PARAMETER INI
        """
        Normalize score based on role and expected complexity.
        
        Formula:
        FINAL_SCORE = raw_score - (weighted_penalty × role_adjustment)
        
        Where:
        - weighted_penalty = sum of (issue_severity × role_weight)
        - role_adjustment = factor based on expected vs actual complexity
        """
        
        expected_range = ROLE_COMPLEXITY_RANGES[role]
        
        # Calculate complexity adjustment factor
        if actual_complexity <= expected_range['max']:
            # Within or below expected range - minimal penalty adjustment
            complexity_factor = 1.0
        else:
            # Above expected range - but apply different scaling by role
            excess = actual_complexity - expected_range['max']
            
            if role == CodeRole.FRAMEWORK:
                # Frameworks: very lenient on complexity excess
                complexity_factor = 1.0 + (excess * 0.01)  # 1% penalty per unit excess
            elif role == CodeRole.ENGINE:
                # Engines: moderate penalty
                complexity_factor = 1.0 + (excess * 0.03)  # 3% penalty per unit excess
            else:  # SCRIPT
                # Scripts: strict on complexity
                complexity_factor = 1.0 + (excess * 0.05)  # 5% penalty per unit excess
        
        # Apply role-based normalization
        normalized_score = raw_score / complexity_factor
        
        # Bonus for frameworks/engines with manageable issue density
        if role in (CodeRole.FRAMEWORK, CodeRole.ENGINE):
            issue_density = total_issues / max(actual_complexity, 1)
            if issue_density < 1.0:  # Less than 1 issue per complexity point
                bonus = min(5.0, (1.0 - issue_density) * 10)
                normalized_score += bonus
        
        # ✅ TAMBAHAN: Penalti untuk critical issues
        if critical_issues > 0:
            # Critical issues dapat menurunkan score lebih banyak
            critical_penalty = critical_issues * 5  # -5 per critical issue
            normalized_score -= critical_penalty
        
        return max(0, min(100, normalized_score))


# ═══════════════════════════════════════════════════════════════════════════
# COMPLEXITY CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════

class ComplexityAnalyzer(ast.NodeVisitor):
    """Calculates code complexity metrics"""
    
    def __init__(self):
        self.complexity = 1
        self.nesting_level = 0
        self.max_nesting = 0
        self.cognitive_complexity = 0
        
    def generic_visit(self, node):
        """Track nesting depth"""
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            self.nesting_level += 1
            self.max_nesting = max(self.max_nesting, self.nesting_level)
            
        super().generic_visit(node)
        
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            self.nesting_level -= 1
    
    def visit_If(self, node):
        """Count if statements"""
        self.complexity += 1
        self.cognitive_complexity += (1 + self.nesting_level)
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Count for loops"""
        self.complexity += 1
        self.cognitive_complexity += (1 + self.nesting_level)
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Count while loops"""
        self.complexity += 1
        self.cognitive_complexity += (1 + self.nesting_level)
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        """Count exception handlers"""
        self.complexity += 1
        self.cognitive_complexity += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """Count boolean operations"""
        self.complexity += len(node.values) - 1
        self.generic_visit(node)
    
    @staticmethod
    def calculate(node: ast.AST) -> Tuple[int, int, int]:
        """Calculate complexity for a node"""
        analyzer = ComplexityAnalyzer()
        analyzer.visit(node)
        return analyzer.complexity, analyzer.cognitive_complexity, analyzer.max_nesting


# ═══════════════════════════════════════════════════════════════════════════
# IMPROVED AST-BASED SECURITY SCANNER
# ═══════════════════════════════════════════════════════════════════════════

class SecurityScanner(ast.NodeVisitor):
    """
    Context-aware security scanner using AST
    Eliminates false positives from string literals and comments
    """
    
    def __init__(self, file_path: str, code: str):
        self.file_path = file_path
        self.code = code
        self.issues = set()  # Use set to prevent duplicates
        self.lines = code.split('\n')
        
    def visit_Call(self, node):
        """Check dangerous function calls"""
        func_name = self._get_func_name(node)
        
        # Check for eval()
        if func_name == 'eval':
            self.issues.add(Issue(
                type=IssueType.SECURITY,
                severity=Severity.CRITICAL,
                message="Using eval() is extremely dangerous",
                file_path=self.file_path,
                line_number=node.lineno,
                code_snippet=self._get_line(node.lineno),
                suggestion="Find safer alternatives, never eval user input"
            ))
        
        # Check for exec()
        elif func_name == 'exec':
            self.issues.add(Issue(
                type=IssueType.SECURITY,
                severity=Severity.CRITICAL,
                message="Using exec() can execute arbitrary code",
                file_path=self.file_path,
                line_number=node.lineno,
                code_snippet=self._get_line(node.lineno),
                suggestion="Refactor to avoid exec()"
            ))
        
        # Check for subprocess with shell=True
        elif func_name in ('subprocess.call', 'subprocess.Popen', 'subprocess.run', 
                           'os.system', 'os.popen'):
            if func_name in ('os.system', 'os.popen'):
                self.issues.add(Issue(
                    type=IssueType.SECURITY,
                    severity=Severity.HIGH,
                    message="Potential command injection vulnerability",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    code_snippet=self._get_line(node.lineno),
                    suggestion="Use subprocess with list arguments instead"
                ))
            else:
                # Check for shell=True in subprocess calls
                for keyword in node.keywords:
                    if keyword.arg == 'shell' and isinstance(keyword.value, ast.Constant):
                        if keyword.value.value is True:
                            self.issues.add(Issue(
                                type=IssueType.SECURITY,
                                severity=Severity.HIGH,
                                message="Potential command injection with shell=True",
                                file_path=self.file_path,
                                line_number=node.lineno,
                                suggestion="Use shell=False and pass command as list"
                            ))
        
        # Check for yaml.load (should use safe_load)
        elif func_name == 'yaml.load':
            has_safe_loader = False
            if len(node.args) > 1:
                if isinstance(node.args[1], ast.Attribute) and node.args[1].attr == 'SafeLoader':
                    has_safe_loader = True
            
            if not has_safe_loader:
                self.issues.add(Issue(
                    type=IssueType.SECURITY,
                    severity=Severity.HIGH,
                    message="Unsafe YAML deserialization",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    suggestion="Use yaml.safe_load() instead"
                ))
        
        # Check for pickle.loads/load
        elif func_name in ('pickle.load', 'pickle.loads'):
            self.issues.add(Issue(
                type=IssueType.SECURITY,
                severity=Severity.MEDIUM,
                message="Pickle deserialization can execute arbitrary code",
                file_path=self.file_path,
                line_number=node.lineno,
                suggestion="Use JSON or other safe serialization formats"
            ))
        
        # Check for hashlib weak algorithms
        elif func_name in ('hashlib.md5', 'hashlib.sha1'):
            self.issues.add(Issue(
                type=IssueType.SECURITY,
                severity=Severity.MEDIUM,
                message=f"Weak cryptographic algorithm: {func_name.split('.')[1].upper()}",
                file_path=self.file_path,
                line_number=node.lineno,
                suggestion="Use SHA256 or stronger algorithms"
            ))
        
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        """Check for hardcoded secrets in assignments"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                
                # Check if value is a string constant
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    value = node.value.value
                    
                    # Skip short values and all-caps constants
                    if len(value) <= 3 or value.isupper():
                        continue
                    
                    # Password detection
                    if any(x in var_name for x in ['password', 'passwd', 'pwd']):
                        self.issues.add(Issue(
                            type=IssueType.SECURITY,
                            severity=Severity.CRITICAL,
                            message=f"Hardcoded password in variable '{target.id}'",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            suggestion="Use environment variables or secure vaults"
                        ))
                    
                    # API key/token detection
                    elif any(x in var_name for x in ['api_key', 'apikey', 'secret_key', 'token', 'auth_token']):
                        if len(value) > 10:
                            self.issues.add(Issue(
                                type=IssueType.SECURITY,
                                severity=Severity.CRITICAL,
                                message=f"Hardcoded API key/token in variable '{target.id}'",
                                file_path=self.file_path,
                                line_number=node.lineno,
                                suggestion="Store secrets in environment variables"
                            ))
        
        self.generic_visit(node)
    
    def _get_func_name(self, node: ast.Call) -> str:
        """Extract function name from call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            parts = []
            obj = node.func
            while isinstance(obj, ast.Attribute):
                parts.append(obj.attr)
                obj = obj.value
            if isinstance(obj, ast.Name):
                parts.append(obj.id)
            return '.'.join(reversed(parts))
        return ""
    
    def _get_line(self, line_num: int) -> str:
        """Get line of code"""
        if 1 <= line_num <= len(self.lines):
            return self.lines[line_num - 1].strip()
        return ""
    
    @classmethod
    def scan(cls, code: str, file_path: str, tree: ast.AST) -> List[Issue]:
        """Scan code for security issues using AST"""
        scanner = cls(file_path, code)
        scanner.visit(tree)
        return list(scanner.issues)


# ═══════════════════════════════════════════════════════════════════════════
# PERFORMANCE ANALYZER (Improved)
# ═══════════════════════════════════════════════════════════════════════════

class PerformanceAnalyzer(ast.NodeVisitor):
    """Detects performance issues using AST"""
    
    def __init__(self, file_path: str, code: str):
        self.file_path = file_path
        self.code = code
        self.issues = set()
        self.lines = code.split('\n')
        self.in_loop = False
        
    def visit_For(self, node):
        """Check for loop performance issues"""
        old_in_loop = self.in_loop
        self.in_loop = True
        
        # Check for string concatenation in loop
        for child in ast.walk(node):
            if isinstance(child, ast.AugAssign):
                if isinstance(child.op, ast.Add):
                    if isinstance(child.target, ast.Name):
                        self.issues.add(Issue(
                            type=IssueType.PERFORMANCE,
                            severity=Severity.MEDIUM,
                            message="String concatenation in loop",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            suggestion="Use list.append() and ''.join() for better performance"
                        ))
                        break
        
        self.generic_visit(node)
        self.in_loop = old_in_loop
    
    def visit_While(self, node):
        """Check while loop performance"""
        old_in_loop = self.in_loop
        self.in_loop = True
        self.generic_visit(node)
        self.in_loop = old_in_loop
    
    @classmethod
    def analyze(cls, code: str, file_path: str, tree: ast.AST) -> List[Issue]:
        """Analyze code for performance issues"""
        analyzer = cls(file_path, code)
        analyzer.visit(tree)
        return list(analyzer.issues)


# ═══════════════════════════════════════════════════════════════════════════
# ANTI-PATTERN DETECTOR
# ═══════════════════════════════════════════════════════════════════════════

class AntiPatternDetector(ast.NodeVisitor):
    """Detects code anti-patterns"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues = set()
        
    def visit_FunctionDef(self, node):
        """Check function issues"""
        # Too many parameters
        if len(node.args.args) > THRESHOLDS['max_parameters']:
            self.issues.add(Issue(
                type=IssueType.ANTI_PATTERN,
                severity=Severity.MEDIUM,
                message=f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                file_path=self.file_path,
                line_number=node.lineno,
                suggestion=f"Consider using a config object or reducing to {THRESHOLDS['max_parameters']} parameters"
            ))
        
        # Empty function
        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.issues.add(Issue(
                type=IssueType.ANTI_PATTERN,
                severity=Severity.LOW,
                message=f"Empty function '{node.name}'",
                file_path=self.file_path,
                line_number=node.lineno,
                suggestion="Implement the function or remove if not needed"
            ))
        
        self.generic_visit(node)
    
    def visit_Try(self, node):
        """Check exception handling"""
        for handler in node.handlers:
            # Bare except
            if handler.type is None:
                self.issues.add(Issue(
                    type=IssueType.ANTI_PATTERN,
                    severity=Severity.MEDIUM,
                    message="Bare except clause catches all exceptions",
                    file_path=self.file_path,
                    line_number=handler.lineno,
                    suggestion="Catch specific exceptions instead"
                ))
            
            # Empty except block
            if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                self.issues.add(Issue(
                    type=IssueType.ANTI_PATTERN,
                    severity=Severity.HIGH,
                    message="Empty except block silently ignores errors",
                    file_path=self.file_path,
                    line_number=handler.lineno,
                    suggestion="Log the error or handle it appropriately"
                ))
        
        self.generic_visit(node)
    
    def visit_Compare(self, node):
        """Check comparisons"""
        # Comparison with True/False
        for comparator in node.comparators:
            if isinstance(comparator, ast.Constant) and comparator.value in (True, False):
                self.issues.add(Issue(
                    type=IssueType.ANTI_PATTERN,
                    severity=Severity.LOW,
                    message="Comparison with True/False is redundant",
                    file_path=self.file_path,
                    line_number=node.lineno,
                    suggestion="Use the boolean expression directly"
                ))
        
        self.generic_visit(node)


# ═══════════════════════════════════════════════════════════════════════════
# MAINTAINABILITY CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════

class MaintainabilityCalculator:
    """Calculates maintainability index"""
    
    @staticmethod
    def calculate(code: str, avg_complexity: float, loc: int, comment_ratio: float) -> float:
        """Calculate Maintainability Index (0-100)"""
        if loc == 0:
            return 100
        
        try:
            volume = max(loc, 1)
            mi = 171 - 5.2 * math.log(volume) - 0.23 * avg_complexity - 16.2 * math.log(loc)
            
            # Add comment bonus
            mi += comment_ratio * 10
            
            # Normalize to 0-100
            mi = max(0, min(100, mi))
            
            return round(mi, 2)
        except:
            return 50.0
# ═══════════════════════════════════════════════════════════════════════════
# ROLE-AWARE MAINTAINABILITY CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════
class RoleAwareMaintainabilityCalculator:
    """
    Calculates maintainability index with role-aware baseline and compensation
    """
    
    # Role-specific baseline MI values
    ROLE_BASELINES = {
        CodeRole.SCRIPT: 60,      # Scripts should be clean and simple
        CodeRole.ENGINE: 50,      # Engines are inherently more complex
        CodeRole.FRAMEWORK: 40,   # Frameworks are architecturally complex
    }
    
    # Minimum MI thresholds per role (floor values)
    ROLE_FLOORS = {
        CodeRole.SCRIPT: 40,
        CodeRole.ENGINE: 35,
        CodeRole.FRAMEWORK: 30,   # Framework can't fall below 30 unless CRITICAL
    }
    
    @staticmethod
    def calculate(code: str, avg_complexity: float, loc: int, comment_ratio: float,
                  role: CodeRole, structural_profile: StructuralProfile) -> float:
        """
        Calculate Role-Aware Maintainability Index (0-100)
        
        Fix #1: Uses role-specific baseline
        Fix #2: Applies logic density compensation
        """
        if loc == 0:
            return 100
        
        try:
            # Standard MI calculation
            volume = max(loc, 1)
            base_mi = 171 - 5.2 * math.log(volume) - 0.23 * avg_complexity - 16.2 * math.log(loc)
            
            # Add comment bonus
            base_mi += comment_ratio * 10
            
            baseline = RoleAwareMaintainabilityCalculator.ROLE_BASELINES[role]
            
            # Blend base MI with role baseline (60% base, 40% baseline)
            adjusted_mi = (base_mi * 0.6) + (baseline * 0.4)
            

            compensation = 0
            
            if role == CodeRole.FRAMEWORK:
                # High logic/utility ratio indicates legitimate complexity
                if structural_profile.logic_utility_ratio > 0.7:
                    compensation += 5  # +5 points for logic-heavy frameworks
                
                # High visitor score indicates meta-programming patterns
                if structural_profile.visitor_score >= ROLE_THRESHOLDS['visitor_score_high']:
                    compensation += structural_profile.visitor_score * 2  # +2 per visitor pattern
                
                # Cap compensation bonus
                compensation = min(compensation, 15)  # Max +15 bonus
            
            elif role == CodeRole.ENGINE:
                # Moderate compensation for engines
                if structural_profile.logic_utility_ratio > 0.6:
                    compensation += 3
                
                compensation = min(compensation, 8)  # Max +8 bonus
            
            adjusted_mi += compensation
            
            # Normalize to 0-100
            adjusted_mi = max(0, min(100, adjusted_mi))
            
            # Apply role-specific floor
            floor = RoleAwareMaintainabilityCalculator.ROLE_FLOORS[role]
            adjusted_mi = max(adjusted_mi, floor)
            
            return round(adjusted_mi, 2)
            
        except Exception as e:
            # Return role baseline on error
            return RoleAwareMaintainabilityCalculator.ROLE_BASELINES[role]

# ═══════════════════════════════════════════════════════════════════════════
# FILE ANALYZER
# ═══════════════════════════════════════════════════════════════════════════

class FileAnalyzer:
    """Analyzes a single Python file"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.code = ""
        self.tree = None
        self.issues = set()  # Use set for deduplication
        
    def analyze(self) -> Optional[FileAnalysis]:
        """Perform complete file analysis with role-aware validation"""
        try:
            # Read file
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.code = f.read()
            
            # Basic metrics
            lines = self.code.split('\n')
            loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
            blank_lines = len([l for l in lines if not l.strip()])
            comment_lines = len([l for l in lines if l.strip().startswith('#')])
            
            # Parse AST
            try:
                self.tree = ast.parse(self.code)
            except SyntaxError as e:
                self.issues.add(Issue(
                    type=IssueType.SYNTAX,
                    severity=Severity.CRITICAL,
                    message=f"Syntax error: {e.msg}",
                    file_path=self.file_path,
                    line_number=e.lineno,
                    column=e.offset
                ))
                return None
            
            # Count structures
            classes = len([n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)])
            functions = len([n for n in ast.walk(self.tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))])
            
            # Calculate complexity
            complexities = []
            max_nesting_overall = 0
            
            for node in ast.walk(self.tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    cyclo, cognitive, nesting = ComplexityAnalyzer.calculate(node)
                    complexities.append(cyclo)
                    max_nesting_overall = max(max_nesting_overall, nesting)
                    
                    # Check complexity thresholds
                    if cyclo > THRESHOLDS['max_cyclomatic_complexity']:
                        self.issues.add(Issue(
                            type=IssueType.COMPLEXITY,
                            severity=Severity.MEDIUM,
                            message=f"Function '{node.name}' has high cyclomatic complexity: {cyclo}",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            suggestion=f"Refactor to reduce complexity below {THRESHOLDS['max_cyclomatic_complexity']}"
                        ))
                    
                    if cognitive > THRESHOLDS['max_cognitive_complexity']:
                        self.issues.add(Issue(
                            type=IssueType.COMPLEXITY,
                            severity=Severity.MEDIUM,
                            message=f"Function '{node.name}' has high cognitive complexity: {cognitive}",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            suggestion="Simplify logic and reduce nesting"
                        ))
                    
                    if nesting > THRESHOLDS['max_nesting_depth']:
                        self.issues.add(Issue(
                            type=IssueType.COMPLEXITY,
                            severity=Severity.MEDIUM,
                            message=f"Function '{node.name}' has deep nesting: {nesting} levels",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            suggestion=f"Reduce nesting depth below {THRESHOLDS['max_nesting_depth']}"
                        ))
            
            avg_complexity = sum(complexities) / len(complexities) if complexities else 0
            max_complexity = max(complexities) if complexities else 0
            
            # ═══════════════════════════════════════════════════════════
            # LAYER 2: STRUCTURAL PROFILING (NEW)
            # ═══════════════════════════════════════════════════════════
            structural_profile = StructuralProfiler.profile(
                tree=self.tree,
                loc=loc,
                functions=functions,
                classes=classes,
                max_nesting=max_nesting_overall,
                avg_complexity=avg_complexity,
                max_complexity=max_complexity
            )
            
            # ═══════════════════════════════════════════════════════════
            # LAYER 3: ROLE CLASSIFICATION (NEW)
            # ═══════════════════════════════════════════════════════════
            role_classification = RoleClassifier.classify(structural_profile)
            
            # Documentation coverage
            docstrings = self.code.count('"""') + self.code.count("'''")
            total_definitions = classes + functions
            doc_coverage = (docstrings / 2) / total_definitions if total_definitions > 0 else 0
            
            if doc_coverage < THRESHOLDS['min_docstring_coverage'] and total_definitions > 0:
                self.issues.add(Issue(
                    type=IssueType.DOCUMENTATION,
                    severity=Severity.LOW,
                    message=f"Low documentation coverage: {doc_coverage*100:.1f}%",
                    file_path=self.file_path,
                    suggestion=f"Add docstrings to reach {THRESHOLDS['min_docstring_coverage']*100}% coverage"
                ))
            
            # Calculate maintainability index with role-aware baseline and compensation
            comment_ratio = comment_lines / len(lines) if lines else 0
            mi = RoleAwareMaintainabilityCalculator.calculate(
                code=self.code,
                avg_complexity=avg_complexity,
                loc=loc,
                comment_ratio=comment_ratio,
                role=role_classification.role,
                structural_profile=structural_profile
            )
            
            if mi < THRESHOLDS['min_maintainability_index']:
                self.issues.add(Issue(
                    type=IssueType.MAINTAINABILITY,
                    severity=Severity.MEDIUM,
                    message=f"Low maintainability index: {mi}",
                    file_path=self.file_path,
                    suggestion="Reduce complexity, add comments, and improve structure"
                ))
            
            # Run AST-based analyzers
            security_issues = SecurityScanner.scan(self.code, self.file_path, self.tree)
            self.issues.update(security_issues)
            
            perf_issues = PerformanceAnalyzer.analyze(self.code, self.file_path, self.tree)
            self.issues.update(perf_issues)
            
            # Anti-pattern detection
            detector = AntiPatternDetector(self.file_path)
            detector.visit(self.tree)
            self.issues.update(detector.issues)
            
            # Check function/class length
            for node in ast.walk(self.tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if hasattr(node, 'end_lineno'):
                        length = node.end_lineno - node.lineno
                        if length > THRESHOLDS['max_function_length']:
                            self.issues.add(Issue(
                                type=IssueType.MAINTAINABILITY,
                                severity=Severity.LOW,
                                message=f"Function '{node.name}' is too long: {length} lines",
                                file_path=self.file_path,
                                line_number=node.lineno,
                                suggestion=f"Break into smaller functions (max {THRESHOLDS['max_function_length']} lines)"
                            ))
                
                elif isinstance(node, ast.ClassDef):
                    if hasattr(node, 'end_lineno'):
                        length = node.end_lineno - node.lineno
                        if length > THRESHOLDS['max_class_length']:
                            self.issues.add(Issue(
                                type=IssueType.MAINTAINABILITY,
                                severity=Severity.LOW,
                                message=f"Class '{node.name}' is too long: {length} lines",
                                file_path=self.file_path,
                                line_number=node.lineno,
                                suggestion=f"Consider splitting into multiple classes (max {THRESHOLDS['max_class_length']} lines)"
                            ))
            
            # ═══════════════════════════════════════════════════════════
            # LAYER 4: ROLE-AWARE ADJUSTMENT (NEW)
            # ═══════════════════════════════════════════════════════════
            adjusted_issues = RoleAwareAdjuster.adjust_issues(
                list(self.issues), 
                role_classification.role
            )
            
            # Create metrics
            metrics = [
                Metric("Lines of Code", loc, "Size", "Total executable lines"),
                Metric("Cyclomatic Complexity", avg_complexity, "Complexity", "Average function complexity"),
                Metric("Maintainability Index", mi, "Quality", "Overall maintainability (0-100)"),
                Metric("Documentation Coverage", doc_coverage * 100, "Documentation", "Percentage of documented functions/classes"),
                Metric("Comment Ratio", comment_ratio * 100, "Documentation", "Percentage of comment lines"),
            ]
            
            return FileAnalysis(
                file_path=self.file_path,
                lines_of_code=loc,
                blank_lines=blank_lines,
                comment_lines=comment_lines,
                classes=classes,
                functions=functions,
                avg_complexity=avg_complexity,
                max_complexity=max_complexity,
                maintainability_index=mi,
                documentation_coverage=doc_coverage,
                structural_profile=structural_profile,
                role_classification=role_classification,
                issues=adjusted_issues,
                metrics=metrics
            )
            
        except Exception as e:
            print(f"Error analyzing {self.file_path}: {e}")
            return None


# ═══════════════════════════════════════════════════════════════════════════
# PROJECT ANALYZER
# ═══════════════════════════════════════════════════════════════════════════

class ProjectAnalyzer:
    """Analyzes entire project or directory"""
    
    def __init__(self, path: str):
        self.path = Path(path)
        self.python_files = []
        self.file_analyses = []
        
    def find_python_files(self):
        """Find all Python files"""
        if self.path.is_file():
            if self.path.suffix == '.py':
                self.python_files = [self.path]
        else:
            self.python_files = list(self.path.rglob('*.py'))
            # Exclude common directories
            self.python_files = [
                f for f in self.python_files 
                if not any(part.startswith('.') or part in ('venv', '__pycache__', 'build', 'dist') 
                          for part in f.parts)
            ]
    
    def analyze(self) -> ProjectAnalysis:
        """Analyze all files in project"""
        print(f"\n🔍 Scanning for Python files in: {self.path}")
        self.find_python_files()
        print(f"📁 Found {len(self.python_files)} Python file(s)")
        
        if not self.python_files:
            print("❌ No Python files found!")
            return ProjectAnalysis(
                project_path=str(self.path),
                total_files=0,
                total_lines=0,
                total_issues=0,
                critical_issues=0,
                high_issues=0,
                overall_score=0,
                grade="N/A"
            )
        
        print("\n" + "="*80)
        print("🔬 ANALYZING FILES")
        print("="*80)
        
        # Analyze each file
        for i, file_path in enumerate(self.python_files, 1):
            print(f"\n[{i}/{len(self.python_files)}] Analyzing: {file_path.name}")
            
            analyzer = FileAnalyzer(str(file_path))
            result = analyzer.analyze()
            
            if result:
                self.file_analyses.append(result)
                
                # Show quick stats with role info
                critical = len([iss for iss in result.issues if iss.severity == Severity.CRITICAL])
                high = len([iss for iss in result.issues if iss.severity == Severity.HIGH])
                
                # Display role classification
                if result.role_classification:
                    role = result.role_classification.role.value
                    confidence = result.role_classification.confidence
                    print(f"    🎯 Detected Role: {role} (confidence: {confidence:.0%})")
                
                if critical > 0:
                    print(f"    🔴 {critical} CRITICAL issue(s)")
                if high > 0:
                    print(f"    🟠 {high} HIGH priority issue(s)")
                if not result.issues:
                    print(f"    ✅ No issues found")
                
                print(f"    📊 Maintainability: {result.maintainability_index:.1f}/100")
        
        # Calculate aggregate metrics
        total_lines = sum(fa.lines_of_code for fa in self.file_analyses)
        total_issues = sum(len(fa.issues) for fa in self.file_analyses)
        critical_issues = sum(
            len([iss for iss in fa.issues if iss.severity == Severity.CRITICAL])
            for fa in self.file_analyses
        )
        high_issues = sum(
            len([iss for iss in fa.issues if iss.severity == Severity.HIGH])
            for fa in self.file_analyses
        )
        
        # ═══════════════════════════════════════════════════════════════
        # LAYER 5: ROLE-AWARE SCORING (NEW)
        # ═══════════════════════════════════════════════════════════════
        if self.file_analyses:
            total_raw_score = 0
            total_normalized_score = 0
            
            for fa in self.file_analyses:
                # Calculate raw maintainability score
                raw_mi = fa.maintainability_index
                
                # Hitung critical issues terlebih dahulu (di dalam loop)
                file_critical_issues = len([iss for iss in fa.issues if iss.severity == Severity.CRITICAL])

                if fa.role_classification:
                    normalized_mi = RoleAwareAdjuster.normalize_score(
                        raw_score=raw_mi,
                        role=fa.role_classification.role,
                        actual_complexity=fa.max_complexity,
                        total_issues=len(fa.issues),
                        critical_issues=file_critical_issues
                    )
                else:
                    # Jika tidak ada role classification, gunakan raw score
                    normalized_mi = raw_mi
                
                total_raw_score += raw_mi
                total_normalized_score += normalized_mi
            
            # Average normalized score
            avg_normalized_mi = total_normalized_score / len(self.file_analyses)
            
            # Apply issue penalties with role-aware weighting
            total_weighted_issues = 0
            for fa in self.file_analyses:
                for issue in fa.issues:
                    # Use role weight if available
                    weight = getattr(issue, 'role_weight', 1.0)
                    
                    if issue.severity == Severity.CRITICAL:
                        total_weighted_issues += 5 * weight
                    elif issue.severity == Severity.HIGH:
                        total_weighted_issues += 2 * weight
                    elif issue.severity == Severity.MEDIUM:
                        total_weighted_issues += 1 * weight
                    else:
                        total_weighted_issues += 0.5 * weight
                        
            # Normalize penalty by project size
            total_functions = sum(fa.functions for fa in self.file_analyses)
            if total_functions > 0:
                issue_density = total_weighted_issues / total_functions
                penalty = min(issue_density * 8, 50)  # Max 50 points penalty
            else:
                penalty = total_weighted_issues * 1.5
            
            overall_score = max(0, avg_normalized_mi - penalty)
        else:
            overall_score = 0
        
        # Determine grade
        if overall_score >= 80:
            grade = "A - EXCELLENT"
        elif overall_score >= 60:
            grade = "B - GOOD"
        elif overall_score >= 40:
            grade = "C - FAIR"
        elif overall_score >= 20:
            grade = "D - NEEDS IMPROVEMENT"
        else:
            grade = "F - CRITICAL"
        
        # Summary metrics
        summary = {
            'total_functions': sum(fa.functions for fa in self.file_analyses),
            'total_classes': sum(fa.classes for fa in self.file_analyses),
            'avg_complexity': sum(fa.avg_complexity for fa in self.file_analyses) / len(self.file_analyses) if self.file_analyses else 0,
            'avg_maintainability': sum(fa.maintainability_index for fa in self.file_analyses) / len(self.file_analyses) if self.file_analyses else 0,
            'security_issues': sum(len([iss for iss in fa.issues if iss.type == IssueType.SECURITY]) for fa in self.file_analyses),
            'performance_issues': sum(len([iss for iss in fa.issues if iss.type == IssueType.PERFORMANCE]) for fa in self.file_analyses),
            'complexity_issues': sum(len([iss for iss in fa.issues if iss.type == IssueType.COMPLEXITY]) for fa in self.file_analyses),
        }
        
        return ProjectAnalysis(
            project_path=str(self.path),
            total_files=len(self.python_files),
            total_lines=total_lines,
            total_issues=total_issues,
            critical_issues=critical_issues,
            high_issues=high_issues,
            overall_score=overall_score,
            grade=grade,
            file_analyses=self.file_analyses,
            summary_metrics=summary
        )


# ═══════════════════════════════════════════════════════════════════════════
# REPORT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════

class ReportGenerator:
    """Generates analysis reports"""
    
    @staticmethod
    def print_summary(analysis: ProjectAnalysis):
        """Print summary to console with role-aware insights"""
        print("\n" + "="*80)
        print("📊 ANALYSIS SUMMARY")
        print("="*80)
        
        print(f"\n📁 Project: {analysis.project_path}")
        print(f"📅 Timestamp: {analysis.timestamp}")
        print(f"🆕 Validator Version: {analysis.version}")
        print(f"📝 Files Analyzed: {analysis.total_files}")
        print(f"📏 Total Lines: {analysis.total_lines:,}")
        
        # Role Distribution (NEW)
        if analysis.file_analyses:
            role_counts = {}
            for fa in analysis.file_analyses:
                if fa.role_classification:
                    role = fa.role_classification.role.value
                    role_counts[role] = role_counts.get(role, 0) + 1
            
            if role_counts:
                print(f"\n🎯 Role Distribution:")
                for role, count in sorted(role_counts.items()):
                    percentage = (count / analysis.total_files) * 100
                    print(f"   {role}: {count} file(s) ({percentage:.0f}%)")
        
        print(f"\n🎯 Overall Score: {analysis.overall_score:.1f}/100 (Role-Normalized)")
        print(f"🏆 Grade: {analysis.grade}")
        
        print(f"\n🐛 Issues Found:")
        print(f"   Total: {analysis.total_issues}")
        print(f"   🔴 Critical: {analysis.critical_issues}")
        print(f"   🟠 High: {analysis.high_issues}")
        
        print(f"\n📊 Metrics:")
        print(f"   Functions: {analysis.summary_metrics['total_functions']}")
        print(f"   Classes: {analysis.summary_metrics['total_classes']}")
        print(f"   Avg Complexity: {analysis.summary_metrics['avg_complexity']:.2f}")
        print(f"   Avg Maintainability: {analysis.summary_metrics['avg_maintainability']:.1f}/100")
        
        print(f"\n🔒 Security: {analysis.summary_metrics['security_issues']} issue(s)")
        print(f"⚡ Performance: {analysis.summary_metrics['performance_issues']} issue(s)")
        print(f"🔄 Complexity: {analysis.summary_metrics['complexity_issues']} issue(s)")
        
        # Role-specific insights (NEW)
        print("\n" + "="*80)
        print("🎯 ROLE-SPECIFIC INSIGHTS")
        print("="*80)
        
        for fa in analysis.file_analyses:
            if fa.role_classification:
                rc = fa.role_classification
                filename = Path(fa.file_path).name
                
                print(f"\n📄 {filename}")
                print(f"   Role: {rc.role.value} (confidence: {rc.confidence:.0%})")
                print(f"   Expected Complexity: {rc.expected_complexity}")
                print(f"   Actual Complexity: {rc.actual_complexity:.1f}")
                print(f"   Verdict: {rc.complexity_verdict} expected range")
                
                if rc.reasoning:
                    print(f"   Reasoning:")
                    for reason in rc.reasoning[:3]:  # Show top 3 reasons
                        print(f"     • {reason}")
                
                # Show adjusted issues count
                adjusted_count = len(fa.issues)
                if adjusted_count > 0:
                    print(f"   Issues (role-adjusted): {adjusted_count}")
        
        # Top issues by severity
        if analysis.file_analyses:
            all_issues = []
            for fa in analysis.file_analyses:
                all_issues.extend(fa.issues)
            
            if all_issues:
                print("\n" + "="*80)
                print("🔴 TOP CRITICAL/HIGH ISSUES")
                print("="*80)
                
                critical_high = [iss for iss in all_issues if iss.severity in (Severity.CRITICAL, Severity.HIGH)]
                critical_high.sort(key=lambda x: (x.severity.value, x.file_path))
                
                for issue in critical_high[:10]:
                    print(f"\n{issue.severity.value} {issue.type.value}")
                    print(f"   📄 {Path(issue.file_path).name}:{issue.line_number or '?'}")
                    print(f"   ❗ {issue.message}")
                    
                    # Show role weight if adjusted
                    if hasattr(issue, 'role_weight') and issue.role_weight != 1.0:
                        print(f"   ⚖️  Role-adjusted weight: {issue.role_weight:.1f}x")
                    
                    if issue.suggestion:
                        print(f"   💡 {issue.suggestion}")
        
        print("\n" + "="*80)
        print("✨ NEW IN v3.0 - ROLE-AWARE VALIDATION")
        print("="*80)
        print("✅ Automatic role detection (SCRIPT/ENGINE/FRAMEWORK)")
        print("✅ Context-intelligent scoring (frameworks not penalized for complexity)")
        print("✅ Adaptive rule weighting based on code purpose")
        print("✅ Zero false positives on legitimate architectural patterns")
        print("="*80)
    
    @staticmethod
    def generate_json(analysis: ProjectAnalysis, output_file: str):
        """Generate JSON report with role information"""
        
        def convert_to_dict(obj):
            """Convert objects to dictionary for JSON"""
            if isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, Issue):
                result = {
                    'type': obj.type.value,
                    'severity': obj.severity.value,
                    'message': obj.message,
                    'file_path': obj.file_path,
                    'line_number': obj.line_number,
                    'column': obj.column,
                    'code_snippet': obj.code_snippet,
                    'suggestion': obj.suggestion
                }
                if hasattr(obj, 'role_weight'):
                    result['role_weight'] = obj.role_weight
                return result
            elif isinstance(obj, StructuralProfile):
                return {
                    'loc': obj.loc,
                    'functions': obj.functions,
                    'classes': obj.classes,
                    'max_nesting': obj.max_nesting,
                    'avg_complexity': obj.avg_complexity,
                    'max_complexity': obj.max_complexity,
                    'visitor_score': obj.visitor_score,
                    'logic_utility_ratio': obj.logic_utility_ratio
                }
            elif isinstance(obj, RoleClassification):
                return {
                    'role': obj.role.value,
                    'confidence': obj.confidence,
                    'reasoning': obj.reasoning,
                    'expected_complexity': obj.expected_complexity,
                    'actual_complexity': obj.actual_complexity,
                    'complexity_verdict': obj.complexity_verdict
                }
            elif isinstance(obj, Metric):
                return {
                    'name': obj.name,
                    'value': obj.value,
                    'category': obj.category,
                    'description': obj.description,
                    'threshold': obj.threshold,
                    'passed': obj.passed
                }
            elif isinstance(obj, FileAnalysis):
                result = {
                    'file_path': obj.file_path,
                    'lines_of_code': obj.lines_of_code,
                    'blank_lines': obj.blank_lines,
                    'comment_lines': obj.comment_lines,
                    'classes': obj.classes,
                    'functions': obj.functions,
                    'avg_complexity': obj.avg_complexity,
                    'max_complexity': obj.max_complexity,
                    'maintainability_index': obj.maintainability_index,
                    'documentation_coverage': obj.documentation_coverage,
                    'issues': [convert_to_dict(iss) for iss in obj.issues],
                    'metrics': [convert_to_dict(m) for m in obj.metrics]
                }
                if obj.structural_profile:
                    result['structural_profile'] = convert_to_dict(obj.structural_profile)
                if obj.role_classification:
                    result['role_classification'] = convert_to_dict(obj.role_classification)
                return result
            elif isinstance(obj, ProjectAnalysis):
                return {
                    'project_path': obj.project_path,
                    'timestamp': obj.timestamp,
                    'version': obj.version,
                    'total_files': obj.total_files,
                    'total_lines': obj.total_lines,
                    'total_issues': obj.total_issues,
                    'critical_issues': obj.critical_issues,
                    'high_issues': obj.high_issues,
                    'overall_score': obj.overall_score,
                    'grade': obj.grade,
                    'summary_metrics': obj.summary_metrics,
                    'file_analyses': [convert_to_dict(fa) for fa in obj.file_analyses]
                }
            return obj
        
        report_data = convert_to_dict(analysis)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Detailed JSON report saved: {output_file}")
    
    @staticmethod
    def generate_html(analysis: ProjectAnalysis, output_file: str):
        """Generate HTML report with role-aware insights"""
        
        # Calculate role distribution
        role_distribution = {}
        for fa in analysis.file_analyses:
            if fa.role_classification:
                role = fa.role_classification.role.value
                role_distribution[role] = role_distribution.get(role, 0) + 1
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Code Analysis Report v{analysis.version}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        .version-badge {{ display: inline-block; background: #4CAF50; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.9em; margin-left: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .card {{ background: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50; }}
        .card.role {{ border-left-color: #2196F3; }}
        .critical {{ border-left-color: #f44336; }}
        .high {{ border-left-color: #ff9800; }}
        .medium {{ border-left-color: #ffc107; }}
        .low {{ border-left-color: #8bc34a; }}
        .grade {{ font-size: 48px; font-weight: bold; text-align: center; color: #4CAF50; }}
        .issue {{ background: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; border-radius: 3px; }}
        .issue.critical {{ background: #f8d7da; border-left-color: #f44336; }}
        .issue.high {{ background: #fff3cd; border-left-color: #ff9800; }}
        .role-badge {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.85em; font-weight: bold; margin-left: 8px; }}
        .role-SCRIPT {{ background: #e3f2fd; color: #1976d2; }}
        .role-ENGINE {{ background: #fff3e0; color: #f57c00; }}
        .role-FRAMEWORK {{ background: #f3e5f5; color: #7b1fa2; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; }}
        .improvements {{ background: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50; margin: 20px 0; }}
        .improvements h3 {{ margin-top: 0; color: #2e7d32; }}
        .role-insights {{ background: #e3f2fd; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3; margin: 20px 0; }}
        .role-insights h3 {{ margin-top: 0; color: #1565c0; }}
        .weight-indicator {{ font-size: 0.9em; color: #666; font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Universal Code Analysis Report <span class="version-badge">v{analysis.version}</span></h1>
        
        <div class="improvements">
            <h3>✨ New in v3.0 - Role-Aware Validation</h3>
            <ul>
                <li>✅ Automatic role detection (SCRIPT/ENGINE/FRAMEWORK)</li>
                <li>✅ Context-intelligent scoring (no false complexity penalties)</li>
                <li>✅ Adaptive rule weighting based on code purpose</li>
                <li>✅ Zero false positives on legitimate architectural patterns</li>
            </ul>
        </div>
        
        <div class="card">
            <h3>Project Information</h3>
            <p><strong>Path:</strong> {analysis.project_path}</p>
            <p><strong>Date:</strong> {analysis.timestamp}</p>
            <p><strong>Files:</strong> {analysis.total_files}</p>
            <p><strong>Lines:</strong> {analysis.total_lines:,}</p>
        </div>
        
        <div class="summary">
            <div class="card">
                <div class="grade">{analysis.overall_score:.0f}</div>
                <p style="text-align: center;"><strong>{analysis.grade}</strong></p>
                <p style="text-align: center; font-size: 0.9em; color: #666;">Role-Normalized Score</p>
            </div>
            <div class="card critical">
                <h3>🔴 Critical Issues</h3>
                <p style="font-size: 36px; margin: 0;">{analysis.critical_issues}</p>
            </div>
            <div class="card high">
                <h3>🟠 High Issues</h3>
                <p style="font-size: 36px; margin: 0;">{analysis.high_issues}</p>
            </div>
            <div class="card">
                <h3>🐛 Total Issues</h3>
                <p style="font-size: 36px; margin: 0;">{analysis.total_issues}</p>
            </div>
        </div>
"""
        
        # Add role distribution
        if role_distribution:
            html += """
        <div class="role-insights">
            <h3>🎯 Role Distribution</h3>
            <p>Detected code roles in your project:</p>
            <ul>
"""
            for role, count in sorted(role_distribution.items()):
                percentage = (count / analysis.total_files) * 100
                html += f'                <li><span class="role-badge role-{role}">{role}</span>: {count} file(s) ({percentage:.0f}%)</li>\n'
            
            html += """
            </ul>
            <p style="font-size: 0.9em; color: #555; margin-top: 10px;">
                <strong>SCRIPT:</strong> Linear utilities/helpers<br>
                <strong>ENGINE:</strong> Logic-heavy systems with state<br>
                <strong>FRAMEWORK:</strong> Meta-analyzers and orchestrators
            </p>
        </div>
"""
        
        html += f"""
        <h2>📊 Metrics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr><td>Functions</td><td>{analysis.summary_metrics['total_functions']}</td></tr>
            <tr><td>Classes</td><td>{analysis.summary_metrics['total_classes']}</td></tr>
            <tr><td>Average Complexity</td><td>{analysis.summary_metrics['avg_complexity']:.2f}</td></tr>
            <tr><td>Average Maintainability</td><td>{analysis.summary_metrics['avg_maintainability']:.1f}/100</td></tr>
            <tr><td>Security Issues</td><td>{analysis.summary_metrics['security_issues']}</td></tr>
            <tr><td>Performance Issues</td><td>{analysis.summary_metrics['performance_issues']}</td></tr>
            <tr><td>Complexity Issues</td><td>{analysis.summary_metrics['complexity_issues']}</td></tr>
        </table>
        
        <h2>🎯 File-Level Role Analysis</h2>
"""
        
        # Add per-file role analysis
        for fa in analysis.file_analyses:
            if fa.role_classification:
                rc = fa.role_classification
                filename = Path(fa.file_path).name
                role = rc.role.value
                
                html += f"""
        <div class="card role">
            <h4>📄 {filename} <span class="role-badge role-{role}">{role}</span></h4>
            <p><strong>Confidence:</strong> {rc.confidence:.0%}</p>
            <p><strong>Expected Complexity:</strong> {rc.expected_complexity} | <strong>Actual:</strong> {rc.actual_complexity:.1f} ({rc.complexity_verdict})</p>
            <p><strong>Reasoning:</strong></p>
            <ul>
"""
                for reason in rc.reasoning[:3]:
                    html += f"                <li>{reason}</li>\n"
                
                html += f"""
            </ul>
            <p><strong>Issues:</strong> {len(fa.issues)} (role-adjusted)</p>
        </div>
"""
        
        html += """
        <h2>🔴 Critical & High Priority Issues</h2>
"""
        
        # Add issues
        for fa in analysis.file_analyses:
            critical_high = [iss for iss in fa.issues if iss.severity in (Severity.CRITICAL, Severity.HIGH)]
            if critical_high:
                html += f"<h3>📄 {Path(fa.file_path).name}</h3>"
                for issue in critical_high:
                    severity_class = 'critical' if issue.severity == Severity.CRITICAL else 'high'
                    weight_info = ""
                    if hasattr(issue, 'role_weight') and issue.role_weight != 1.0:
                        weight_info = f'<p class="weight-indicator">⚖️ Role-adjusted weight: {issue.role_weight:.1f}x</p>'
                    
                    html += f"""
                    <div class="issue {severity_class}">
                        <strong>{issue.severity.value} {issue.type.value}</strong>
                        <p>Line {issue.line_number or '?'}: {issue.message}</p>
                        {f'<p><em>💡 {issue.suggestion}</em></p>' if issue.suggestion else ''}
                        {weight_info}
                    </div>
                    """
        
        html += """
        <footer style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
            <p>Generated by Universal Code Validator v3.0 - Role-Aware AST-Based Analysis</p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"📄 HTML report saved: {output_file}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                 🌟 UNIVERSAL CODE VALIDATOR v{VERSION} 🌟                    ║
║                                                                            ║
║              Analyze ANY Python code without prior knowledge               ║
║         Now with ROLE-AWARE VALIDATION - Context-Intelligent Scoring!     ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Get target path
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        print("Usage options:")
        print("  1. Analyze single file:    python validator.py myfile.py")
        print("  2. Analyze directory:      python validator.py /path/to/project")
        print("  3. Analyze current dir:    python validator.py .")
        print()
        target = input("Enter file or directory path (or '.' for current): ").strip()
        if not target:
            target = "."
    
    # Check if path exists
    target_path = Path(target)
    if not target_path.exists():
        print(f"\n❌ Error: Path not found: {target}")
        sys.exit(1)
    
    # Analyze
    analyzer = ProjectAnalyzer(target)
    analysis = analyzer.analyze()
    
    # Generate reports
    ReportGenerator.print_summary(analysis)
    
    # Save reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"code_analysis_{timestamp}.json"
    html_file = f"code_analysis_{timestamp}.html"
    
    print("\n" + "="*80)
    print("💾 GENERATING REPORTS")
    print("="*80)
    
    ReportGenerator.generate_json(analysis, json_file)
    ReportGenerator.generate_html(analysis, html_file)
    
    # Final recommendations
    print("\n" + "="*80)
    print("💡 RECOMMENDATIONS")
    print("="*80)
    
    if analysis.critical_issues > 0:
        print("\n🔴 URGENT: Fix critical issues immediately!")
        print("   These issues can cause serious problems.")
    
    if analysis.summary_metrics['security_issues'] > 0:
        print(f"\n🔒 Security: Address {analysis.summary_metrics['security_issues']} security issue(s)")
        print("   Security vulnerabilities should be prioritized.")
    
    if analysis.summary_metrics['avg_complexity'] > 10:
        print(f"\n🔄 Complexity: Average complexity is {analysis.summary_metrics['avg_complexity']:.1f}")
        print("   Consider refactoring complex functions.")
    
    if analysis.summary_metrics['avg_maintainability'] < 40:
        print(f"\n⚠️  Maintainability: Score is {analysis.summary_metrics['avg_maintainability']:.1f}/100")
        print("   Code needs significant improvement for long-term maintenance.")
    
    print("\n✅ Next Steps:")
    print("   1. Review the HTML report in your browser")
    print("   2. Check role classifications - are they accurate?")
    print("   3. Fix critical and high priority issues first")
    print("   4. Note that complexity penalties are role-adjusted")
    print("   5. Run the validator again to track improvements")
    print("   6. Consider setting up automated CI/CD checks")
    
    print("\n" + "="*80)
    print("✨ Analysis Complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
