# test_101_allure_init.py

import pytest
import allure

@allure.feature("10.1: Inicjalizacja Allure")
class TestAllureInit:

    @allure.story("Test pozytywny – powinien przejść")
    def test_pass_example(self):
        with allure.step("Krok 1: Sprawdzenie wartości prawdziwej"):
            assert True
        with allure.step("Krok 2: Dodatkowe sprawdzenie"):
            assert 1 + 1 == 2

    @allure.story("Test negatywny – powinien nie przejść")
    def test_fail_example(self):
        with allure.step("Krok 1: Sprawdzenie wartości fałszywej"):
            assert False, "Celowe niepowodzenie testu"
        with allure.step("Krok 2: Ten krok nie zostanie wykonany"):
            assert True