# 64_audit_report.md - Raport z Audytu

## 1. Analiza Spójności

Po przeanalizowaniu logów z testu w **Zadaniu 6.3** oraz mapy selektorów wygenerowanej w **Artefakcie 5**, zauważono, że wszystkie użyte identyfikatory (takie jak `ADD`, `title`, `LOGIN_FIELD`) są zgodne z mapą selektorów.

- **ID 'ADD'**: Zgodne z mapą selektorów – `button_add`.
- **ID 'title'**: Zgodne z mapą selektorów – `label_title`.
- **ID 'LOGIN_FIELD'**: Zgodne z mapą selektorów – `edit_text_username`.

Dzięki tej spójności, testy są stabilne, ponieważ nie występują niezgodności między identyfikatorami używanymi w testach a tymi, które są zdefiniowane w aplikacji.

---

## 2. Ocena Modularności

Jeśli deweloper zmieniłby ID przycisku `ADD` na `PLUS_BTN`, zmiana ta wpłynęłaby na kilka plików w projekcie:

- **MainPage.py**: Klasa reprezentująca ekran główny zawierałaby metodę, która używa `ADD`. Trzeba by było edytować tę metodę, aby korzystała z nowego selektora (`PLUS_BTN`).
- **BasePage.py**: Jeśli używamy klasy bazowej `BasePage`, zmiana ID wymagałaby aktualizacji mapy selektorów w pliku `53_selectors.json`. Jednak dzięki centralizacji mapy selektorów, zmiana ta musiałaby być dokonana tylko w jednym miejscu.

Zmiana w jednym selektorze wymaga edytowania jednego pliku JSON oraz potencjalnie jednej metody w klasie Page, co znacznie upraszcza utrzymanie kodu i minimalizuje ryzyko wprowadzenia błędów w innych częściach aplikacji.

---

## 3. Wnioski Optymalizacyjne

Jedną z rzeczy, którą można by dodać do klasy **BasePage**, aby ułatwić pracę testerom, jest implementacja **Explicit Wait** dla elementów UI. 

Obecnie, jeśli element nie jest od razu dostępny (np. z powodu opóźnienia ładowania strony), test może nie powieść się z powodu braku elementu w momencie interakcji. Dodanie metody, która czeka na załadowanie elementu przed interakcją (np. `wait_for_element(self, element)`), pozwoliłoby na zwiększenie stabilności testów.

Przykład implementacji:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wait_for_element(self, element_id, timeout=10):
    """
    Czeka na załadowanie elementu w UI przed próbą interakcji z nim.
    """
    WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located((By.ID, self.find_id(element_id)))
    )

---

### **Kroki do zapisania pliku**:

1. **Zapisz plik**:
   Zapisz utworzony plik jako **64_audit_report.md** w odpowiednim folderze.

2. **Użyj odpowiednich edytorów**:
   Jeśli chcesz edytować plik w przyszłości, możesz otworzyć go w dowolnym edytorze tekstu, który obsługuje Markdown (np. **Visual Studio Code**, **Notepad++**, **Typora**).

3. **Sprawdzenie**:
   Możesz załadować plik do **GitHub**, aby sprawdzić, jak renderuje się Markdown, lub po prostu otworzyć go w edytorze.

---

### **Podsumowanie**:

Plik **64_audit_report.md** powinien zawierać analizę spójności, ocenę modularności oraz wnioski optymalizacyjne, które pomogą poprawić jakość kodu i zapewnią stabilność testów. W ten sposób dokumentujesz swój proces audytu i przekazujesz cenne informacje dotyczące jakości architektury testowej w projekcie.