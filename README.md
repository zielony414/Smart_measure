# Smart Measure - System Automatyzacji Pomiarów DC/DC

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/UI-PyQt5-green?style=for-the-badge&logo=qt" />
</p>

## O Projekcie

Projekt **Smart Measure** został zrealizowany w ramach kolaboracji pomiędzy **Politechniką Rzeszowską** a firmą **Bury Sp. z o.o.** Celem systemu jest pełna automatyzacja procesu wyznaczania sprawności przetworników DC/DC w warunkach laboratoryjnych.

System eliminuje błędy ludzkie oraz znacząco skraca czas testów poprzez bezpośrednią komunikację z aparaturą pomiarową, zbieranie danych w czasie rzeczywistym oraz generowanie ustrukturyzowanych raportów analitycznych.

## Kluczowe Funkcjonalności

- **Automatyzacja Cyklu Pomiarowego:** Skrypt steruje nastawami zasilaczy i obciążeń zgodnie ze zdefiniowanym scenariuszem testowym.
- **Obsługa Aparatury Laboratoryjnej:** Integracja z multimetrami, zasilaczami i obciążeniami elektronicznymi renomowanych marek.
- **Generowanie Raportów:** Automatyczny eksport wyników do arkuszy Excel na podstawie przygotowanych szablonów (`Template.xlsx`).
- **Interfejs Graficzny (GUI):** Intuicyjny panel operatora zbudowany w oparciu o bibliotekę PyQt5.
- **Tryb Symulacji:** Możliwość testowania logiki oprogramowania bez fizycznego podłączenia urządzeń.

## Obsługiwany Sprzęt

System posiada zaimplementowane sterowniki dla następujących urządzeń:
- **Multimetry:** FLUKE 8808A, FLUKE 8846A.
- **Zasilacze:** TTI CPX400DP.
- **Obciążenia elektroniczne:** BK Precision 8601.
- **Komory klimatyczne:** CTS T6550 (obsługa warunków środowiskowych).

## Technologia

- **Język:** Python
- **Biblioteki:**
  - `PyQt5` – interfejs użytkownika.
  - `Pandas` & `NumPy` – przetwarzanie i analiza danych.
  - `OpenPyXL` – manipulacja plikami Excel.
  - `PySerial` – komunikacja z urządzeniami przez porty COM/RS232.

## Struktura Projektu

- `main.py` – Główny punkt wejścia aplikacji.
- `BurySmartMeasure.py` – Logika interfejsu graficznego.
- `data.py` – Moduł odpowiedzialny za logikę pomiarową i przetwarzanie danych.
- `symulacja/` – Środowisko do testowania systemu offline.
- `drivers/` – (Pliki takie jak `FLUKE8808A.py` itp.) dedykowane klasy do obsługi konkretnych urządzeń
