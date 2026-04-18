#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
82_secrets_finder.py - Skaner wycieków danych (Hardcoded Secrets)
TM-93850 Block 8.2 - Android Security Audit
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

class SecretsFinder:
    def __init__(self):
        self.base_path = r"C:\TM-93850\Artefakt02\decompiled_apk"
        self.strings_path = os.path.join(self.base_path, "res", "values", "strings.xml")
        self.output_file = "82_secrets_found.txt"
        self.findings = []
        
        # Wzorce do wyszukiwania SECRETS (High Precision)
        self.SECRETS_PATTERNS = {
            'API_KEYS': [
                r'api[_-]?key["\']?\s*[=:]\s*["\']?([a-zA-Z0-9]{20,})',
                r'key["\']?\s*[=:]\s*["\']?([a-zA-Z0-9]{16,40})',
                r'AIza[0-9A-Za-z_-]{35}',
                r'AKIA[0-9A-Z]{16}',
            ],
            'URL_IP': [
                r'(?:http[s]?://|//)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\$\\$,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
                r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})',
            ],
            'PASSWORDS': [
                r'(?:password|pass|pwd)["\']?\s*[=:]\s*["\']?([^"\']{4,})',
                r'(?:secret|token)["\']?\s*[=:]\s*["\']?([a-zA-Z0-9]{10,})',
            ],
            'DATABASE': [
                r'(?:db_|database_)["\']?\s*[=:]\s*["\']?([a-zA-Z0-9:/._-]+)',
                r'mongodb://[^"\s]+',
                r'postgres://[^"\s]+',
            ],
            'FIREBASE': [
                r'project_id["\']?\s*:\s*["\']?([a-z0-9-]{6,})',
                r'firebase[_-]?config',
            ]
        }
    
    def scan_strings_xml(self):
        """Skanowanie głównego pliku strings.xml"""
        print("🔍 Skanowanie strings.xml...")
        
        if not os.path.exists(self.strings_path):
            print(f"❌ Plik nie istnieje: {self.strings_path}")
            print("💡 Sprawdź czy APK został zdekompilowany w Bloku 2")
            return False
        
        try:
            with open(self.strings_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            print(f"✅ Znaleziono strings.xml ({len(content)} bajtów)")
            
            # Skanowanie wszystkich wzorców
            self._scan_patterns(content, "strings.xml")
            return True
            
        except Exception as e:
            print(f"❌ Błąd odczytu pliku: {e}")
            return False
    
    def _scan_patterns(self, content, filename):
        """Skanowanie wzorców w treści"""
        line_num = 1
        for line in content.split('\n'):
            for category, patterns in self.SECRETS_PATTERNS.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        secret = match.group(1) if match.groups() else match.group(0)
                        if len(secret) > 5:  # Filtr krótkich false positives
                            finding = {
                                'category': category,
                                'secret': secret[:50] + '...' if len(secret) > 50 else secret,
                                'line': line_num,
                                'filename': filename,
                                'context': line.strip()[:100]
                            }
                            self.findings.append(finding)
                            print(f"🟡 [{category}] Linia {line_num}: {finding['secret']}")
            line_num += 1
    
    def scan_all_files(self):
        """Skanowanie WSZYSTKICH plików tekstowych (bonus)"""
        print("\n🔍 Skanowanie wszystkich plików tekstowych...")
        scanned = 0
        
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(('.xml', '.java', '.smali', '.txt', '.json', '.properties')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            self._scan_patterns(content, os.path.relpath(filepath, self.base_path))
                            scanned += 1
                    except:
                        continue
        
        print(f"✅ Przeskanowano {scanned} plików")
    
    def save_report(self):
        """Zapis wyników do 82_secrets_found.txt"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(f"SECRETS SCAN REPORT\n")
            f.write(f"Generated: {timestamp}\n")
            f.write(f"Base path: {self.base_path}\n")
            f.write(f"Total findings: {len(self.findings)}\n")
            f.write("="*60 + "\n\n")
            
            if not self.findings:
                f.write("✅ NO SECRETS FOUND - APPLICATION SECURE\n")
            else:
                for i, finding in enumerate(self.findings, 1):
                    f.write(f"{i}. [{finding['category'].upper()}]\n")
                    f.write(f"   File: {finding['filename']} (line {finding['line']})\n")
                    f.write(f"   Secret: {finding['secret']}\n")
                    f.write(f"   Context: {finding['context']}\n")
                    f.write("-" * 40 + "\n")
        
        print(f"\n✅ Raport zapisany: {self.output_file}")
    
    def print_summary(self):
        """Podsumowanie w terminalu"""
        print("\n" + "="*50)
        print("📊 PODSUMOWANIE SKANU SECRETS")
        print("="*50)
        print(f"📁 Strings.xml: {'✅ ZNALEZIONO' if self.findings else '🟢 CZYSTE'}")
        print(f"🔍 Znalezisk: {len(self.findings)}")
        print(f"📄 Raport: 82_secrets_found.txt")
        print("="*50)

def main():
    print("🔍 8.2 SECRETS FINDER - Hardcoded Secrets Scanner")
    print("="*50)
    
    scanner = SecretsFinder()
    
    # Główny skan strings.xml
    if scanner.scan_strings_xml():
        # Bonus: skan wszystkich plików
        scanner.scan_all_files()
        
        # Zapis raportu
        scanner.save_report()
        scanner.print_summary()
        print("\n🎉 ZADANIE 8.2 CZĘŚĆ 1 UKOŃCZONE!")
        print("📋 Sprawdź: 82_secrets_found.txt")
    else:
        print("❌ BŁĄD - sprawdź ścieżkę do dekompilacji")
        sys.exit(1)

if __name__ == "__main__":
    main()