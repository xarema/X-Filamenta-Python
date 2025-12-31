"""
---
Purpose: Automated security audit script for X-Filamenta-Python
Description: Runs security scanners and generates comprehensive security report

File: scripts/security_audit.py | Repository: X-Filamenta-Python
Created: 2025-12-30
Last modified: 2025-12-30

Distributed by: XAREMA | Coder: AleGabMar
App version: 0.1.0-Beta | File version: 1.0.0

License: AGPL-3.0-or-later
SPDX-License-Identifier: AGPL-3.0-or-later
Copyright (c) 2025 XAREMA. All rights reserved.

Metadata:
- Status: Stable
- Classification: Internal
---
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path


def run_command(command, description):
    """Run a command and capture output."""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*70}\n")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Command timed out after 5 minutes',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }


def check_tool_installed(tool_name, check_command):
    """Check if a security tool is installed."""
    try:
        subprocess.run(
            check_command,
            capture_output=True,
            timeout=10
        )
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def install_security_tools():
    """Install required security tools if not present."""
    tools = {
        'bandit': [sys.executable, '-m', 'pip', 'show', 'bandit'],
        'safety': [sys.executable, '-m', 'pip', 'show', 'safety'],
        'pip-audit': [sys.executable, '-m', 'pip', 'show', 'pip-audit']
    }

    missing_tools = []
    for tool, check_cmd in tools.items():
        if not check_tool_installed(tool, check_cmd):
            missing_tools.append(tool)

    if missing_tools:
        print(f"\n⚠️  Missing security tools: {', '.join(missing_tools)}")
        print("Installing required tools...")

        for tool in missing_tools:
            install_cmd = [sys.executable, '-m', 'pip', 'install', tool]
            result = run_command(install_cmd, f"Installing {tool}")
            if not result['success']:
                print(f"❌ Failed to install {tool}")
                return False

        print("✅ All security tools installed successfully")
    else:
        print("✅ All security tools are already installed")

    return True


def run_bandit_scan():
    """Run bandit security scanner on Python code."""
    bandit_cmd = [
        sys.executable, '-m', 'bandit',
        '-r', 'backend/',
        '-f', 'json',
        '-o', 'security_audit_bandit.json'
    ]

    result = run_command(bandit_cmd, "Bandit Security Scanner")

    # Bandit returns non-zero if it finds issues, which is expected
    # Read the JSON output
    try:
        with open('security_audit_bandit.json', 'r') as f:
            bandit_results = json.load(f)

        issues_count = len(bandit_results.get('results', []))
        print(f"\n📊 Bandit Results: {issues_count} potential issues found")

        if issues_count > 0:
            severity_counts = {}
            for issue in bandit_results.get('results', []):
                severity = issue.get('issue_severity', 'UNKNOWN')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            print("\nBy Severity:")
            for severity, count in sorted(severity_counts.items()):
                print(f"  {severity}: {count}")

        return bandit_results
    except FileNotFoundError:
        print("❌ Bandit output file not found")
        return None
    except json.JSONDecodeError:
        print("❌ Failed to parse Bandit output")
        return None


def run_safety_check():
    """Run safety checker for known vulnerabilities."""
    safety_cmd = [
        sys.executable, '-m', 'safety',
        'check',
        '--json'
    ]

    result = run_command(safety_cmd, "Safety Vulnerability Checker")

    try:
        if result['stdout']:
            safety_results = json.loads(result['stdout'])
            vuln_count = len(safety_results)
            print(f"\n📊 Safety Results: {vuln_count} known vulnerabilities found")

            if vuln_count > 0:
                for vuln in safety_results:
                    pkg = vuln.get('package', 'unknown')
                    installed = vuln.get('installed_version', 'unknown')
                    vuln_id = vuln.get('vulnerability_id', 'unknown')
                    print(f"\n⚠️  {pkg} {installed}")
                    print(f"   Vulnerability: {vuln_id}")

            return safety_results
        else:
            print("✅ No known vulnerabilities found")
            return []
    except json.JSONDecodeError:
        print("⚠️  Could not parse Safety output")
        print(result['stdout'])
        return None


def run_pip_audit():
    """Run pip-audit for comprehensive dependency scanning."""
    pip_audit_cmd = [
        sys.executable, '-m', 'pip_audit',
        '--format', 'json'
    ]

    result = run_command(pip_audit_cmd, "Pip-Audit Dependency Scanner")

    try:
        if result['stdout']:
            audit_results = json.loads(result['stdout'])
            dependencies = audit_results.get('dependencies', [])

            vulnerable = [d for d in dependencies if d.get('vulns')]
            print(f"\n📊 Pip-Audit Results: {len(vulnerable)} vulnerable packages")

            if vulnerable:
                for dep in vulnerable:
                    name = dep.get('name', 'unknown')
                    version = dep.get('version', 'unknown')
                    vulns = dep.get('vulns', [])
                    print(f"\n⚠️  {name} {version}")
                    print(f"   {len(vulns)} vulnerabilities")

            return audit_results
        else:
            print("✅ No vulnerabilities found")
            return {'dependencies': []}
    except json.JSONDecodeError:
        print("⚠️  Could not parse pip-audit output")
        return None


def manual_security_checks():
    """Perform manual security checks."""
    print("\n" + "="*70)
    print("Manual Security Checks")
    print("="*70 + "\n")

    checks = {
        'secrets_in_code': check_hardcoded_secrets(),
        'sql_injection': check_sql_injection_risks(),
        'xss_vulnerabilities': check_xss_risks(),
        'csrf_protection': check_csrf_protection(),
        'auth_security': check_authentication_security()
    }

    return checks


def check_hardcoded_secrets():
    """Check for hardcoded secrets in code."""
    print("Checking for hardcoded secrets...")

    # Common secret patterns
    patterns = [
        'password =',
        'api_key =',
        'secret_key =',
        'token =',
        'SECRET_KEY =',
        'API_KEY ='
    ]

    issues = []
    backend_path = Path('backend')

    for py_file in backend_path.rglob('*.py'):
        if 'tests' in str(py_file) or '__pycache__' in str(py_file):
            continue

        try:
            content = py_file.read_text()
            for pattern in patterns:
                if pattern in content:
                    # Check if it's a config from env or actual hardcoded value
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if pattern in line and 'environ' not in line and 'config' not in line.lower():
                            issues.append({
                                'file': str(py_file),
                                'line': i,
                                'pattern': pattern
                            })
        except Exception as e:
            continue

    if issues:
        print(f"⚠️  Found {len(issues)} potential hardcoded secrets")
        for issue in issues[:5]:  # Show first 5
            print(f"   {issue['file']}:{issue['line']} - {issue['pattern']}")
    else:
        print("✅ No hardcoded secrets detected")

    return {'passed': len(issues) == 0, 'issues': issues}


def check_sql_injection_risks():
    """Check for SQL injection vulnerabilities."""
    print("\nChecking for SQL injection risks...")

    risky_patterns = [
        'execute("',
        'execute(f"',
        '.format(',
        '% ',
    ]

    issues = []
    backend_path = Path('backend')

    for py_file in backend_path.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue

        try:
            content = py_file.read_text()
            if 'sql' in content.lower() or 'query' in content.lower():
                for pattern in risky_patterns:
                    if pattern in content:
                        issues.append({
                            'file': str(py_file),
                            'pattern': pattern,
                            'severity': 'MEDIUM'
                        })
        except Exception:
            continue

    if issues:
        print(f"⚠️  Found {len(issues)} potential SQL injection risks")
    else:
        print("✅ No obvious SQL injection risks detected")

    return {'passed': len(issues) == 0, 'issues': issues}


def check_xss_risks():
    """Check for XSS vulnerabilities."""
    print("\nChecking for XSS risks...")

    # Check if templates properly escape user input
    templates_path = Path('frontend/templates')
    issues = []

    if templates_path.exists():
        for html_file in templates_path.rglob('*.html'):
            try:
                content = html_file.read_text()
                # Look for potential unsafe rendering
                if '{{ ' in content and '| safe' in content:
                    issues.append({
                        'file': str(html_file),
                        'issue': 'Uses "| safe" filter - verify input is sanitized'
                    })
            except Exception:
                continue

    if issues:
        print(f"⚠️  Found {len(issues)} potential XSS risks (manual review needed)")
    else:
        print("✅ No obvious XSS risks detected")

    return {'passed': True, 'warnings': issues}  # Warnings, not failures


def check_csrf_protection():
    """Check if CSRF protection is implemented."""
    print("\nChecking CSRF protection...")

    # Check if Flask-WTF or similar CSRF protection is used
    config_file = Path('backend/src/config.py')
    csrf_enabled = False

    if config_file.exists():
        content = config_file.read_text()
        if 'CSRF' in content or 'csrf' in content:
            csrf_enabled = True

    if csrf_enabled:
        print("✅ CSRF protection appears to be configured")
    else:
        print("⚠️  CSRF protection not clearly configured")

    return {'passed': csrf_enabled}


def check_authentication_security():
    """Check authentication security practices."""
    print("\nChecking authentication security...")

    issues = []
    auth_file = Path('backend/src/routes/auth.py')

    if auth_file.exists():
        content = auth_file.read_text()

        # Check for password hashing
        if 'bcrypt' not in content and 'pbkdf2' not in content and 'set_password' not in content:
            issues.append("No clear password hashing mechanism found")

        # Check for rate limiting
        if 'limiter' not in content and 'rate_limit' not in content:
            issues.append("No rate limiting detected on auth routes")

    if issues:
        print(f"⚠️  Found {len(issues)} authentication security concerns")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("✅ Authentication security looks good")

    return {'passed': len(issues) == 0, 'issues': issues}


def generate_report(bandit_results, safety_results, pip_audit_results, manual_checks):
    """Generate comprehensive security audit report."""
    report_path = Path('Analysis_reports')
    report_path.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    report_file = report_path / f'{timestamp}_security_audit.md'

    with open(report_file, 'w') as f:
        f.write("---\n")
        f.write("Purpose: Comprehensive Security Audit Report\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("File: Analysis_reports/" + report_file.name + "\n")
        f.write("License: AGPL-3.0-or-later\n")
        f.write("---\n\n")

        f.write("# Security Audit Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")

        f.write("## Executive Summary\n\n")

        # Count total issues
        bandit_count = len(bandit_results.get('results', [])) if bandit_results else 0
        safety_count = len(safety_results) if safety_results else 0
        pip_audit_count = len([d for d in pip_audit_results.get('dependencies', []) if d.get('vulns')]) if pip_audit_results else 0

        f.write(f"- **Bandit Issues:** {bandit_count}\n")
        f.write(f"- **Known Vulnerabilities (Safety):** {safety_count}\n")
        f.write(f"- **Vulnerable Dependencies (Pip-Audit):** {pip_audit_count}\n\n")

        # Manual checks summary
        f.write("### Manual Security Checks\n\n")
        for check_name, result in manual_checks.items():
            status = "✅ PASS" if result.get('passed') else "⚠️  REVIEW NEEDED"
            f.write(f"- **{check_name.replace('_', ' ').title()}:** {status}\n")

        f.write("\n---\n\n")

        # Detailed results
        f.write("## Detailed Findings\n\n")

        # Bandit details
        if bandit_results:
            f.write("### Bandit Security Scanner\n\n")
            results = bandit_results.get('results', [])
            if results:
                for issue in results[:10]:  # Top 10
                    f.write(f"**{issue.get('issue_text')}**\n")
                    f.write(f"- Severity: {issue.get('issue_severity')}\n")
                    f.write(f"- Confidence: {issue.get('issue_confidence')}\n")
                    f.write(f"- File: {issue.get('filename')}:{issue.get('line_number')}\n\n")
            else:
                f.write("✅ No issues found\n\n")

        # Safety details
        if safety_results:
            f.write("### Known Vulnerabilities\n\n")
            if safety_results:
                for vuln in safety_results:
                    f.write(f"**{vuln.get('package')} {vuln.get('installed_version')}**\n")
                    f.write(f"- Vulnerability: {vuln.get('vulnerability_id')}\n")
                    f.write(f"- Fixed in: {vuln.get('fixed_version', 'N/A')}\n\n")
            else:
                f.write("✅ No known vulnerabilities\n\n")

        # Recommendations
        f.write("## Recommendations\n\n")
        f.write("1. Review and address all HIGH severity Bandit findings\n")
        f.write("2. Update vulnerable dependencies to patched versions\n")
        f.write("3. Implement missing security controls identified in manual checks\n")
        f.write("4. Schedule regular security audits (monthly recommended)\n")
        f.write("5. Keep dependencies up to date\n\n")

        f.write("---\n\n")
        f.write(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

    print(f"\n✅ Security audit report generated: {report_file}")
    return report_file


def main():
    """Main security audit execution."""
    print("\n" + "="*70)
    print("X-Filamenta-Python Security Audit")
    print("="*70 + "\n")

    # Step 1: Install tools
    if not install_security_tools():
        print("\n❌ Failed to install security tools. Exiting.")
        return 1

    # Step 2: Run automated scans
    print("\n" + "="*70)
    print("Running Automated Security Scans")
    print("="*70)

    bandit_results = run_bandit_scan()
    safety_results = run_safety_check()
    pip_audit_results = run_pip_audit()

    # Step 3: Manual checks
    manual_checks = manual_security_checks()

    # Step 4: Generate report
    report_file = generate_report(bandit_results, safety_results, pip_audit_results, manual_checks)

    print("\n" + "="*70)
    print("Security Audit Complete")
    print("="*70)
    print(f"\n📄 Full report: {report_file}")
    print("\n✅ Security audit completed successfully")

    return 0


if __name__ == '__main__':
    sys.exit(main())

