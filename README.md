# 📱 Testowanie Mobilne – Projekt Semestralny (Automation Portfolio)

## 👨‍💻 Autor
Student: Szymon (TM-93850)

---

# 🚀 Opis projektu

Ten projekt przedstawia kompletny proces automatyzacji testów aplikacji mobilnych oraz API w środowisku Python + Appium + Docker + Allure.

Projekt został zbudowany krok po kroku w ramach laboratoriów i obejmuje pełny cykl:
od konfiguracji środowiska → przez testy → aż do generowania raportów i pipeline CI-like.

---

# 🧱 Blok 1 – Wprowadzenie do testowania mobilnego

W tym etapie zapoznałem się z podstawami testowania aplikacji mobilnych oraz architekturą Appium.
Poznałem rolę WebDrivera oraz sposób komunikacji z urządzeniami mobilnymi.

Technologie:
- Appium
- Android Emulator / Device
- Python

---

# ⚙️ Blok 2 – Środowisko testowe

Skonfigurowałem środowisko pracy oraz repozytorium GitHub.
Nauczyłem się pracy z terminalem oraz podstaw Git.

Technologie:
- Git / GitHub
- Python
- CLI

---

# 📦 Blok 3 – Docker i infrastruktura testowa

Uruchomiłem Appium Server w kontenerze Docker.
Poznałem podstawy Docker Compose i zarządzania kontenerami.

Technologie:
- Docker
- Docker Compose
- Appium Server

---

# 🧪 Blok 4 – Pierwsze testy automatyczne

Stworzyłem pierwsze testy automatyczne w Pythonie.
Poznałem strukturę testów oraz framework pytest.

Technologie:
- pytest
- Python
- Appium Client

---

# 🔗 Blok 5 – Testy API (Requests)

Rozszerzyłem testy o warstwę API.
Nauczyłem się wysyłania requestów oraz walidacji odpowiedzi JSON.

Technologie:
- requests
- REST API
- JSON validation

---

# 📊 Blok 6 – Raportowanie testów

Wprowadziłem system raportowania Allure.
Nauczyłem się dodawania kroków testowych (allure.step) oraz adnotacji.

Technologie:
- allure-pytest
- Allure Framework
- pytest

---

# 📸 Blok 7 – Zaawansowane raporty

Rozszerzyłem raporty o:
- załączniki (screenshots / JSON)
- story / feature
- metadane testów

Technologie:
- Allure attachments
- pytest hooks

---

# 🔄 Blok 8 – Integracja Appium + Test Framework

Połączyłem Appium z frameworkiem testowym.
Uruchamiałem testy end-to-end na uruchomionym serwerze Appium.

Technologie:
- Appium Python Client
- Selenium WebDriver API
- Docker Appium Server

---

# 🧪 Blok 9 – Infrastruktura testowa (Docker)

Zautomatyzowałem uruchamianie środowiska testowego przez Docker Compose.
Testy działały niezależnie od systemu operacyjnego.

Technologie:
- Docker Compose
- Appium containerization

---

# 🚀 Blok 10 – Pipeline CI (Allure + Automation)

Zbudowałem uniwersalny pipeline testowy:
- uruchamianie infrastruktury
- wykonywanie testów
- generowanie raportów Allure
- automatyczne sprzątanie środowiska

Efekt końcowy:
jedna komenda uruchamia cały proces testowy end-to-end.

Technologie:
- Python automation script
- pytest
- Allure Report (HTML)
- Docker Compose

---

# 🧠 Umiejętności zdobyte w projekcie

- Automatyzacja testów mobilnych (Appium)
- Tworzenie testów API
- Praca z Docker
- Budowa pipeline testowego
- Generowanie raportów Allure
- Organizacja projektu testowego
- CI/CD fundamentals

---

# 📌 Podsumowanie

Projekt przedstawia pełny cykl automatyzacji testów:
od konfiguracji środowiska aż po generowanie raportów i pipeline.

Jest to baza pod profesjonalne frameworki testowe stosowane w środowiskach produkcyjnych (QA Automation / DevOps).

---

# 🔗 Możliwe rozszerzenia

- integracja z Jenkins / GitHub Actions
- testy równoległe (pytest-xdist)
- testy na real device farm
- integracja z BrowserStack / SauceLabs