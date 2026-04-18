#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
81_manifest_scanner.py v1.1 - FIX dla namespace + XML
"""

import xml.etree.ElementTree as ET
import os
import sys
from pathlib import Path
import re
from datetime import datetime

class ManifestPermissionScanner:
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.risky_permissions = []
        self.debug_flags = []
        self.report = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_permissions': 0,
            'risky_permissions': [],
            'debug_flags': [],
            'risk_level': 'LOW',
            'all_permissions': []
        }
        
        # Baza niebezpiecznych uprawnień
        self.DANGEROUS_PERMISSIONS = {
            'android.permission.READ_SMS': {'risk': 'CRITICAL', 'desc': 'Odczyt SMS - phishing, 2FA bypass'},
            'android.permission.RECEIVE_SMS': {'risk': 'CRITICAL', 'desc': 'Odbiór SMS - przechwytywanie OTP'},
            'android.permission.WRITE_SMS': {'risk': 'CRITICAL', 'desc': 'Pisanie SMS - premium SMS fraud'},
            'android.permission.SEND_SMS': {'risk': 'CRITICAL', 'desc': 'Wysyłanie SMS - kosztowne ataki'},
            'android.permission.READ_CALL_LOG': {'risk': 'CRITICAL', 'desc': 'Dziennik połączeń - stalking'},
            'android.permission.WRITE_CALL_LOG': {'risk': 'CRITICAL', 'desc': 'Modyfikacja logów połączeń'},
            'android.permission.PROCESS_OUTGOING_CALLS': {'risk': 'CRITICAL', 'desc': 'Przechwytywanie połączeń wychodzących'},
            'android.permission.ACCESS_FINE_LOCATION': {'risk': 'CRITICAL', 'desc': 'Precyzyjna lokalizacja GPS'},
            'android.permission.ACCESS_COARSE_LOCATION': {'risk': 'HIGH', 'desc': 'Przybliżona lokalizacja sieciowa'},
            'android.permission.RECORD_AUDIO': {'risk': 'CRITICAL', 'desc': 'Nagrywanie audio - podsłuch'},
            'android.permission.CAMERA': {'risk': 'CRITICAL', 'desc': 'Dostęp do kamery - szpiegowanie'},
            'android.permission.READ_CONTACTS': {'risk': 'HIGH', 'desc': 'Kontakty - spam, phishing'},
            'android.permission.WRITE_CONTACTS': {'risk': 'HIGH', 'desc': 'Modyfikacja kontaktów'},
            'android.permission.GET_ACCOUNTS': {'risk': 'HIGH', 'desc': 'Lista kont użytkownika'},
            'android.permission.READ_PHONE_STATE': {'risk': 'HIGH', 'desc': 'IMEI, numer telefonu'},
            'android.permission.CALL_PHONE': {'risk': 'HIGH', 'desc': 'Wybieranie połączeń bez UI'},
            'android.permission.USE_FINGERPRINT': {'risk': 'HIGH', 'desc': 'Biometria - fingerprint spoofing'},
            'android.permission.USE_BIOMETRIC': {'risk': 'HIGH', 'desc': 'Biometria ogólna'},
            'android.permission.INSTALL_PACKAGES': {'risk': 'CRITICAL', 'desc': 'Instalacja APK bez zgody'},
            'android.permission.DELETE_PACKAGES': {'risk': 'CRITICAL', 'desc': 'Usuwanie aplikacji'}
        }
    
    def scan_manifest(self):
        """Główna funkcja skanowania z FIX namespace"""
        print("🔍 Rozpoczynam audyt AndroidManifest.xml...")
        print(f"📁 Ścieżka: {self.manifest_path}")
        
        if not os.path.exists(self.manifest_path):
            print(f"❌ BŁĄD: Plik {self.manifest_path} nie istnieje!")
            sys.exit(1)
        
        try:
            # FIX: Usuwanie namespace dla prostego parsowania
            tree = ET.parse(self.manifest_path)
            root = tree.getroot()
            
            # Czyszczenie namespace
            for elem in root.iter():
                if '}' in elem.tag:
                    elem.tag = elem.tag.split('}', 1)[1]
            
            print("✅ XML sparsowany pomyślnie (namespace fixed)")
            
            # Skanowanie uprawnień
            self._scan_permissions(root)
            
            # Skanowanie flag debugowania
            self._scan_debug_flags(root)
            
            # Generowanie raportu
            self._generate_report()
            
            print("✅ Audyt zakończony pomyślnie!")
            print(f"⚠️  Znaleziono {len(self.report['risky_permissions'])} niebezpiecznych uprawnień")
            
            return True
            
        except ET.ParseError as e:
            print(f"❌ BŁĄD parsowania XML: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Nieoczekiwany błąd: {e}")
            sys.exit(1)
    
    def _scan_permissions(self, root):
        """Skanowanie z FIX namespace"""
        permissions = root.findall('.//uses-permission')
        self.report['total_permissions'] = len(permissions)
        
        print(f"\n📋 Znaleziono {len(permissions)} wszystkich uprawnień:")
        
        for i, perm in enumerate(permissions):
            # FIX: Poprawne czytanie android:name
            perm_name = perm.get('{http://schemas.android.com/apk/res/android}name') or \
                       perm.get('android:name') or \
                       perm.get('name') or \
                       f"UNKNOWN_{i}"
            
            self.report['all_permissions'].append(perm_name)
            
            print(f"  📄 {perm_name}")
            
            # Sprawdzanie czy niebezpieczne
            if perm_name in self.DANGEROUS_PERMISSIONS:
                risk_info = self.DANGEROUS_PERMISSIONS[perm_name]
                risky_perm = {
                    'name': perm_name,
                    'risk': risk_info['risk'],
                    'description': risk_info['desc']
                }
                self.risky_permissions.append(risky_perm)
                self.report['risky_permissions'].append(risky_perm)
                
                marker = "🔴" if risk_info['risk'] == 'CRITICAL' else "🟡"
                print(f"    {marker} NIEBEZPIECZNE ({risk_info['risk']}) - {risk_info['desc']}")
    
    def _scan_debug_flags(self, root):
        """Skanowanie flag debugowania z FIX namespace"""
        app_element = root.find('.//application')
        if app_element is not None:
            # Debuggable - sprawdzenie obu namespace
            debuggable = (app_element.get('{http://schemas.android.com/apk/res/android}debuggable') or 
                         app_element.get('android:debuggable') or 
                         app_element.get('debuggable'))
            
            if debuggable == 'true':
                self.debug_flags.append('android:debuggable="true"')
                self.report['debug_flags'].append({
                    'flag': 'android:debuggable',
                    'value': 'true',
                    'risk': 'CRITICAL'
                })
                print("\n🔴 KRYTYCZNY: android:debuggable=\"true\"!")
            
            # Backup
            allow_backup = (app_element.get('{http://schemas.android.com/apk/res/android}allowBackup') or 
                           app_element.get('android:allowBackup') or 
                           app_element.get('allowBackup'))
            
            if allow_backup == 'true':
                self.debug_flags.append('android:allowBackup="true"')
                self.report['debug_flags'].append({
                    'flag': 'android:allowBackup',
                    'value': 'true',
                    'risk': 'HIGH'
                })
                print("🟡 WYSOKIE RYZYKO: android:allowBackup=\"true\"")
    
    def _generate_report(self):
        """Generowanie raportu ryzyka"""
        critical_count = sum(1 for p in self.report['risky_permissions'] if p['risk'] == 'CRITICAL')
        
        if critical_count > 0:
            self.report['risk_level'] = 'CRITICAL'
        elif len(self.report['risky_permissions']) > 3:
            self.report['risk_level'] = 'HIGH'
        elif len(self.report['risky_permissions']) > 0:
            self.report['risk_level'] = 'MEDIUM'
    
    def save_xml_report(self, output_path):
        """ZAPIS XML - POPRAWIONA WERSJA"""
        # Używamy ET do prostego XML
        root = ET.Element('RiskyPermissionsReport')
        
        # Metadata
        meta = ET.SubElement(root, 'metadata')
        ET.SubElement(meta, 'scan_date').text = self.report['scan_date']
        ET.SubElement(meta, 'total_permissions').text = str(self.report['total_permissions'])
        ET.SubElement(meta, 'risk_level').text = self.report['risk_level']
        ET.SubElement(meta, 'all_permissions_count').text = str(len(self.report['all_permissions']))
        
        # Risky permissions
        risky_section = ET.SubElement(root, 'risky_permissions')
        for perm in self.report['risky_permissions']:
            perm_elem = ET.SubElement(risky_section, 'permission')
            perm_elem.set('name', perm['name'])
            perm_elem.set('risk', perm['risk'])
            desc = ET.SubElement(perm_elem, 'description')
            desc.text = perm['description']
        
        # Debug flags
        if self.report['debug_flags']:
            debug_section = ET.SubElement(root, 'debug_flags')
            for flag in self.report['debug_flags']:
                flag_elem = ET.SubElement(debug_section, 'flag')
                flag_elem.set('name', flag['flag'])
                flag_elem.set('value', flag['value'])
                flag_elem.set('risk', flag['risk'])
        
        # Pretty print i zapis
        rough_string = ET.tostring(root, 'unicode')
        reparsed = ET.fromstring(rough_string)
        tree = ET.ElementTree(reparsed)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ Raport XML zapisany: {output_path}")
    
    def print_summary(self):
        """Wydruk podsumowania"""
        print("\n" + "="*70)
        print("📊 PODSUMOWANIE AUDYTU UPRAWNIEŃ")
        print("="*70)
        print(f"📅 Data: {self.report['scan_date']}")
        print(f"📊 Razem uprawnień: {self.report['total_permissions']}")
        print(f"🔴 Krytyczne: {sum(1 for p in self.report['risky_permissions'] if p['risk'] == 'CRITICAL')}")
        print(f"🟡 Wysokie: {sum(1 for p in self.report['risky_permissions'] if p['risk'] == 'HIGH')}")
        print(f"⚠️  Poziom ryzyka: **{self.report['risk_level']}**")
        
        if self.report['risky_permissions']:
            print("\n📋 Niebezpieczne uprawnienia:")
            for perm in self.report['risky_permissions']:
                print(f"   {perm['name']} ({perm['risk']})")
        print("="*70)

def main():
    base_path = r"C:\TM-93850\Artefakt02\decompiled_apk"
    manifest_path = os.path.join(base_path, "AndroidManifest.xml")
    
    if not os.path.exists(base_path):
        print(f"❌ BŁĄD: Folder {base_path} nie istnieje!")
        print("💡 Uruchom dekompilację APK z Bloku 2")
        sys.exit(1)
    
    scanner = ManifestPermissionScanner(manifest_path)
    
    success = scanner.scan_manifest()
    if not success:
        sys.exit(1)
    
    output_dir = os.getcwd()
    xml_report = os.path.join(output_dir, "RiskyPermission.xml")
    scanner.save_xml_report(xml_report)
    
    scanner.print_summary()
    
    print(f"\n🎉 SUKCES! Pliki wygenerowane:")
    print(f"   📄 RiskyPermission.xml ✓")
    print(f"   📋 Sprawdź 81_permissions_report.md")

if __name__ == "__main__":
    main()