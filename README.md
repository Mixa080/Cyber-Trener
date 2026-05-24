# 🏋️ Digital Twin Trainer (Cyber Trener)

**Digital Twin Trainer** to innowacyjna aplikacja wspierająca trening siłowy, wykorzystująca wizję komputerową do analizy poprawności wykonywanych ćwiczeń w czasie rzeczywistym. System pełni rolę „cyfrowego bliźniaka” trenera, pomagając użytkownikom ćwiczyć efektywniej i bezpieczniej.

## 👥 Autorzy Projektu
* **Maksym Sas** (258495)
* **Yurii Pokora** (258650)
* **Mykhailo Shkurupii** (258496)

## 🚀 Główne Funkcjonalności
Aplikacja automatyzuje proces treningowy, od planowania po szczegółową analitykę postępów.

* **Analiza techniki w czasie rzeczywistym:** Wykorzystanie kamery do śledzenia kąta w stawach, zakresu ruchu oraz tempa.
* **Interaktywny Feedback:** Głosowe i wizualne komunikaty korygujące technikę podczas serii (np. „Zwolnij fazę ekscentryczną”).
* **Zarządzanie Planem Treningowym:** Możliwość przeglądania kalendarza, edycji planów oraz automatyczne sugestie kolejnych sesji.
* **Dashboard Statystyk:** Wizualizacja postępów, wykresy siły i porównania tygodniowe na podstawie danych historycznych.

## 🗄️ Baza Danych (Data Storage)
System wykorzystuje relacyjną bazę danych MSSQL do trwałego przechowywania i zarządzania informacjami:
* **Użytkownicy:** Profile, parametry fizyczne oraz cele treningowe.
* **Plany Treningowe:** Predefiniowane i spersonalizowane zestawy ćwiczeń wraz z harmonogramem.
* **Historia Sesji:** Szczegółowy zapis każdego treningu (liczba powtórzeń, czas trwania, wykryte błędy).
* **Analityka Postępów:** Przechowywanie danych historycznych niezbędnych do generowania wykresów progresji.

## 📋 Przykład: Podnoszenie hantli na biceps
Projekt szczegółowo analizuje technikę podnoszenia hantli na biceps w celu maksymalizacji zaangażowania mięśni dwugłowych ramienia i przedramion.

### Poprawna Technika:
1. **Pozycja początkowa:** Ciało wyprostowane, stopy na szerokość bioder, ramiona wzdłuż ciała.
2. **Faza podnoszenia:** Zginanie rąk w łokciach przy zachowaniu ich bliskości do tułowia.
3. **Faza opuszczania:** Powolny, kontrolowany ruch do pełnego wyprostu rąk.

### Analizowane błędy:
* **Bujanie ciałem:** Wykorzystywanie pędu tułowia do podniesienia ciężaru.
* **Ruch ramion do przodu:** Przesuwanie łokci zamiast ich stabilizacji.
* **Zbyt szybkie opuszczanie:** Brak kontroli w fazie ekscentrycznej.
* **Niepełny zakres ruchu:** Brak pełnego wyprostu rąk w dolnej fazie.

## ⚙️ Logika Systemu (Workflow)
Zgodnie z modelem działania, proces treningowy przebiega następująco:

1. **Logowanie:** Autoryzacja i dostęp do spersonalizowanego pulpitu (Dashboard) z danymi z bazy.
2. **Przygotowanie:** Otwarcie planu dnia pobranego z bazy danych i ewentualna jego edycja.
3. **Sesja:** Aktywacja kamery → Wykonanie serii → Analiza ruchu przez program → Otrzymanie feedbacku.
4. **Podsumowanie:** Automatyczny zapis wyników (powtórzenia, jakość techniki) do **Bazy Danych** i aktualizacja statystyk.

## 🛠 Architektura
System obsługi treningu angażuje cztery główne filary:

* **Użytkownik (ćwiczący):** Wykonuje trening i monitoruje statystyki.
* **Trener:** Zarządza planami treningowymi dostępnymi w systemie.
* **Program (AI Engine):** Odpowiada za techniczną analizę sesji (Vision) i interfejs użytkownika.
* **Baza Danych:** Serce systemu przechowujące historię, plany i dane użytkowników.
