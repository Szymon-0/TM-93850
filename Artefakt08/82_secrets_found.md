# Raport analizy hardcoded secrets


## Top 3 Zagrożenia

W tej sekcji przedstawiam trzy przykłady hardcoded secrets, które moim zdaniem stanowią poważne zagrożenie dla bezpieczeństwa aplikacji. Są to dane, które mogą zostać łatwo wykorzystane przez hakera.

1. **Hasła w pliku `strings.xml`**
   - **Sekret**: `Password:`
   - **Plik**: `strings.xml` (linia 177)
   - **Opis**: Wartość `"Password:"` w pliku `strings.xml` może wskazywać na przechowywanie haseł użytkowników w aplikacji. Jeśli hasła są twardo zapisane w plikach zasobów, to stanowi to poważne zagrożenie, ponieważ takie dane mogą zostać wydobyte podczas dekompilacji aplikacji.
   
2. **Przykład adresu e-mail w twardym kodzie**
   - **Sekret**: `foobar@example.com`
   - **Plik**: `strings.xml` (linia 561)
   - **Opis**: Adres e-mail `foobar@example.com` zapisany w pliku `strings.xml` może stanowić dane kontaktowe, które mogą zostać użyte przez hakera do wysyłania phishingowych wiadomości e-mail. Potencjalnie może to również wskazywać na brak odpowiedniego zabezpieczenia danych użytkowników w aplikacji.

3. **Adres URL w twardym kodzie**
   - **Sekret**: `http://www.google.com`
   - **Plik**: `strings.xml` (linia 561)
   - **Opis**: Zawartość adresu URL `http://www.google.com` w aplikacji nie wydaje się mieć związku z rzeczywistym działaniem aplikacji. Tego typu dane mogą zostać użyte do ataków typu man-in-the-middle (MITM), jeśli aplikacja nie wykorzystuje odpowiednich zabezpieczeń w postaci HTTPS lub jeśli URL jest nieprawidłowo zaimplementowany.

## Top 3 False Positives

W tej sekcji przedstawiam trzy przykłady, które zostały oznaczone jako "groźne" przez skrypt, ale po dalszej analizie okazuje się, że są to elementy interfejsu użytkownika lub standardowe linki, które nie stanowią rzeczywistego zagrożenia.

1. **Instrukcja dotycząca hasła**
   - **Sekret**: `Please enter your password:`
   - **Plik**: `strings.xml` (linia 236)
   - **Opis**: Jest to standardowy tekst w aplikacjach mobilnych, który jest wyświetlany w oknie dialogowym, gdy użytkownik jest proszony o podanie hasła. Wartość ta jest częścią interfejsu użytkownika i nie stanowi zagrożenia, chyba że występuje w kontekście przechowywania samego hasła.

2. **Adres URL z domyślnym linkiem**
   - **Sekret**: `http://www.example.com/lala/foobar@example.com`
   - **Plik**: `strings.xml` (linia 561)
   - **Opis**: Jest to przykładowy adres URL, który często pojawia się w kodzie lub w dokumentacji, by pokazać, jak działa linkowanie danych w aplikacji. Nie jest to prawdziwy adres URL, tylko przykład, więc nie stanowi rzeczywistego zagrożenia.

3. **Wartość w linku do Google**
   - **Sekret**: `https://www.google.com`
   - **Plik**: `strings.xml` (linia 561)
   - **Opis**: Podobnie jak w przypadku poprzedniego URL-a, adres `https://www.google.com` może zostać uznany za przykład lub domyślny link. Jako popularny link do Google, nie stanowi on zagrożenia, jeśli jest używany zgodnie z przeznaczeniem.

## Podsumowanie

Analiza hardcoded secrets w aplikacji wykazała, że chociaż większość znalezionych elementów jest wynikiem typowych praktyk programistycznych (np. przykładowe adresy URL, teksty w interfejsie), to wciąż zidentyfikowano poważne ryzyko związane z przechowywaniem haseł lub adresów e-mail w plikach zasobów aplikacji. Takie dane mogą stanowić punkt wyjścia dla ataków, takich jak phishing czy wykorzystanie starych, nieaktualnych danych.

Zalecenia obejmują:
- Unikanie twardego kodowania wrażliwych danych w plikach zasobów.
- Przeglądanie i aktualizowanie linków oraz tekstów, aby upewnić się, że nie zawierają wrażliwych informacji.

**Data analizy**: 18/04/2026  
