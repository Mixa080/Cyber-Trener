

# 🏋️ Digital Twin Trainer (Cyber Trener)

[cite_start]**Digital Twin Trainer** to innowacyjna aplikacja wspierająca trening siłowy, wykorzystująca wizję komputerową do analizy poprawności wykonywanych ćwiczeń w czasie rzeczywistym[cite: 1, 2]. [cite_start]System pełni rolę „cyfrowego bliźniaka” trenera, pomagając użytkownikom ćwiczyć efektywniej i bezpieczniej[cite: 6, 8].

## 👥 Autorzy Projektu
* [cite_start]**Maksym Sas** (258495) [cite: 45]
* [cite_start]**Yurii Pokora** (258650) [cite: 46]
* [cite_start]**Mykhailo Shkurupii** (258496) [cite: 47]


## 🚀 Główne Funkcjonalności
[cite_start]Aplikacja automatyzuje proces treningowy, od planowania po szczegółową analitykę postępów[cite: 13, 23].

* [cite_start]**Analiza techniki w czasie rzeczywistym:** Wykorzystanie kamery do śledzenia kąta w stawach, zakresu ruchu oraz tempa[cite: 7, 33].
* [cite_start]**Interaktywny Feedback:** Głosowe i wizualne komunikaty korygujące technikę podczas serii (np. „Zwolnij fazę ekscentryczną”)[cite: 8, 34].
* [cite_start]**Zarządzanie Planem Treningowym:** Możliwość przeglądania kalendarza, edycji planów oraz automatyczne sugestie kolejnych sesji[cite: 5, 21, 38].
* [cite_start]**Dashboard Statystyk:** Wizualizacja postępów, wykresy siły i porównania tygodniowe[cite: 10, 27].



## 📋 Przykład: Podnoszenie hantli na biceps
[cite_start]Projekt szczegółowo analizuje technikę podnoszenia hantli na biceps w celu maksymalizacji zaangażowania mięśni dwugłowych ramienia i przedramion[cite: 43, 49, 50, 51].

### [cite_start]Poprawna Technika[cite: 54]:
1.  [cite_start]**Pozycja początkowa:** Ciało wyprostowane, stopy na szerokość bioder, ramiona wzdłuż ciała[cite: 55, 56, 57, 58].
2.  [cite_start]**Faza podnoszenia:** Zginanie rąk w łokciach przy zachowaniu ich bliskości do tułowia[cite: 60, 61, 63].
3.  [cite_start]**Faza opuszczania:** Powolny, kontrolowany ruch do pełnego wyprostu rąk[cite: 64, 65, 66, 67].

### [cite_start]Analizowane błędy[cite: 70, 75]:
* [cite_start]**Bujanie ciałem:** Wykorzystywanie pędu tułowia do podniesienia ciężaru[cite: 79, 80].
* [cite_start]**Ruch ramion do przodu:** Przesuwanie łokci zamiast ich stabilizacji[cite: 76, 77].
* [cite_start]**Zbyt szybkie opuszczanie:** Brak kontroli w fazie ekscentrycznej[cite: 82, 83].
* [cite_start]**Niepełny zakres ruchu:** Brak pełnego wyprostu rąk w dolnej fazie[cite: 85, 86].



## ⚙️ Logika Systemu (Workflow)
[cite_start]Zgodnie z diagramem aktywności[cite: 40], proces treningowy przebiega następująco:
1.  [cite_start]**Logowanie:** Dostęp do spersonalizowanego pulpitu[cite: 26, 27].
2.  [cite_start]**Przygotowanie:** Otwarcie planu dnia i ewentualna jego edycja[cite: 28, 29].
3.  [cite_start]**Sesja:** Aktywacja kamery $\rightarrow$ Wykonanie serii $\rightarrow$ Analiza ruchu $\rightarrow$ Otrzymanie feedbacku[cite: 31, 32, 33, 34].
4.  [cite_start]**Podsumowanie:** Zapis wyników (powtórzenia, jakość) i aktualizacja statystyk[cite: 37, 38].


## 🛠 Architektura
[cite_start]System obsługi treningu angażuje trzech głównych aktorów[cite: 1, 13]:
* [cite_start]**Użytkownik (ćwiczący):** Wykonuje trening i monitoruje statystyki[cite: 19].
* [cite_start]**Trener:** Zarządza planami treningowymi[cite: 22].
* [cite_start]**Program:** Odpowiada za techniczną analizę sesji w czasie rzeczywistym[cite: 18].
