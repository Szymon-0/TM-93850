#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
84_security_scorer.py v1.2 - FIXED UnicodeError
TM-93850 Block 8.4 - Risk Classification
"""

import xml.etree.ElementTree as ET
import json
import os
import sys
from datetime import datetime

class SecurityScorer:
    def __init__(self):
        self.max_score = 100.0
        self.score = self.max_score
        self.deductions = []
        
        self.permissions_file = "RiskyPermission.xml"
        self.vulns_file = "83_vulnerabilities.json"
        
        self.WEIGHTS = {
            "CRITICAL_permission": -40,
            "HIGH_permission": -20,
            "debuggable_true": -30,
            "allowBackup_true": -15,
            "CRITICAL_cve": -25,
            "HIGH_cve": -15,
            "MEDIUM_cve": -8,
            "multiple_issues": -10
        }
    
    def audit_permissions(self):
        """Analiza RiskyPermission.xml"""
        print("🔍 [8.1] Analiza RiskyPermission.xml...")
        
        if not os.path.exists(self.permissions_file):
            print(f"   ⚪ Plik {self.permissions_file} nie istnieje")
            return
        
        try:
            tree = ET.parse(self.permissions_file)
            root = tree.getroot()
            
            critical_perms = root.findall(".//permission[@risk='CRITICAL']")
            for perm in critical_perms:
                self.score += self.WEIGHTS["CRITICAL_permission"]
                self.deductions.append(f"🔴 {perm.get('name')} (-40)")
            
            high_perms = root.findall(".//permission[@risk='HIGH']")
            for perm in high_perms:
                self.score += self.WEIGHTS["HIGH_permission"]
                self.deductions.append(f"🟠 {perm.get('name')} (-20)")
            
            debug_flags = root.findall(".//flag[@name='android:debuggable']")
            if debug_flags:
                self.score += self.WEIGHTS["debuggable_true"]
                self.deductions.append("🔴 android:debuggable=true (-30)")
            
            print(f"   📊 {len(critical_perms)} Critical, {len(high_perms)} High")
            
        except Exception as e:
            print(f"   ⚠️  Błąd XML: {e}")
    
    def audit_vulnerabilities(self):
        """Analiza 83_vulnerabilities.json"""
        print("🔍 [8.3] Analiza CVE vulnerabilities...")
        
        if not os.path.exists(self.vulns_file):
            print(f"   ⚪ Plik {self.vulns_file} nie istnieje")
            return
        
        try:
            with open(self.vulns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            vulns = data.get('vulnerabilities', [])
            
            critical_cve = [v for v in vulns if v['severity'] == 'CRITICAL']
            for cve in critical_cve:
                self.score += self.WEIGHTS["CRITICAL_cve"]
                self.deductions.append(f"🔴 {cve['cve']} (-25)")
            
            high_cve = [v for v in vulns if v['severity'] == 'HIGH']
            for cve in high_cve:
                self.score += self.WEIGHTS["HIGH_cve"]
                self.deductions.append(f"🟠 {cve['cve']} (-15)")
            
            medium_cve = [v for v in vulns if v['severity'] == 'MEDIUM']
            for cve in medium_cve:
                self.score += self.WEIGHTS["MEDIUM_cve"]
                self.deductions.append(f"🟡 {cve['cve']} (-8)")
            
            print(f"   📊 {len(critical_cve)} Critical, {len(high_cve)} High, {len(medium_cve)} Medium")
            
        except Exception as e:
            print(f"   ⚠️  Błąd JSON: {e}")
    
    def calculate_risk_level(self):
        """Klasyfikacja ryzyka"""
        if self.score >= 90:
            return "🟢 LOW"
        elif self.score >= 70:
            return "🟡 MEDIUM"
        elif self.score >= 40:
            return "🟠 HIGH"
        else:
            return "🔴 CRITICAL"
    
    def generate_report(self):
        """Generowanie raportu - FIXED UTF-8"""
        risk_level = self.calculate_risk_level()
        
        with open("84_risk_score.txt", "w", encoding='utf-8') as f:
            f.write("ANDROID SECURITY SCORE REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"FINAL SCORE: {self.score:.1f} / 100\n")
            f.write(f"RISK LEVEL: {risk_level}\n\n")
            f.write("DEDUCTION BREAKDOWN:\n")
            f.write("-" * 30 + "\n")
            for deduction in self.deductions:
                f.write(f"• {deduction}\n")
            f.write("\nRECOMMENDATION:\n")
            if self.score < 40:
                f.write("🚫 CRITICAL - DO NOT DEPLOY!\n")
            else:
                f.write("⚠️  Review required\n")
        
        print(f"\n✅ 84_risk_score.txt ZAPISANY")
    
    def run_audit(self):
        """Główny audyt"""
        print("🔍 8.4 SECURITY SCORER")
        print("Integracja 8.1 + 8.3")
        print("=" * 50)
        
        self.audit_permissions()
        self.audit_vulnerabilities()
        
        self.score = max(0, self.score)
        risk_level = self.calculate_risk_level()
        
        print("\n" + "="*50)
        print("🎯 FINAL SCORE")
        print("="*50)
        print(f"📊 SCORE: **{self.score:.1f}/100**")
        print(f"🎨 {risk_level}")
        
        if self.deductions:
            print("\n📉 Top Deductions:")
            for d in self.deductions[:5]:
                print(f"   {d}")
        
        self.generate_report()
        print("\n🎉 8.4 ZALICZONE!")

def main():
    scorer = SecurityScorer()
    scorer.run_audit()

if __name__ == "__main__":
    main()