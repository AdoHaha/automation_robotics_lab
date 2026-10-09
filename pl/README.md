# Automatyka i robotyka — laboratoria po polsku

Notatniki prowadzą od podstaw Pythona do modelowania i analizy decyzji produkcyjnych. Zawierają objaśnienia, skomentowany kod, docstringi funkcji, ilustracje, wykresy, eksperymenty interaktywne oraz zadania do samodzielnego wykonania.

| Laboratorium | Temat | Google Colab |
|---|---|---|
| [0](lab_auto_0.ipynb) | Podstawy Pythona: dane, pętle, funkcje, tabele, wykresy i pierwszy suwak | [Otwórz](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/pl/lab_auto_0.ipynb) |
| [1](lab_auto_1.ipynb) | Asortyment produkcji i przydział zasobów: PuLP, obszar dopuszczalny i analiza ograniczeń | [Otwórz](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/pl/lab_auto_1.ipynb) |
| [2](lab_auto_2.ipynb) | Dobór mieszanki: bilans masy, jakość, koszt i analiza wrażliwości | [Otwórz](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/pl/lab_auto_2.ipynb) |
| [3](lab_auto_3.ipynb) | Problem transportowy, przepływy w sieci i problem rozkroju | [Otwórz](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/pl/lab_auto_3.ipynb) |
| [4](lab_auto_4.ipynb) | Harmonogramowanie typu job-shop i wykresy Gantta | [Otwórz](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/pl/lab_auto_4.ipynb) |
| [5](lab_auto_5.ipynb) | Sieci projektu: CPM, PERT, zapasy czasu i skracanie czynności | [Otwórz](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/pl/lab_auto_5.ipynb) |
| [6](lab_auto_6.ipynb) | Prognozy cen i ryzyka awarii jako wejścia do modeli produkcyjnych | [Otwórz](https://colab.research.google.com/github/AdoHaha/automation_robotics_lab/blob/master/pl/lab_auto_6.ipynb) |

## Jak pracować w Colab

Otwórz wybrany notatnik, zapisz własną kopię na Dysku i wykonuj komórki po kolei, zaczynając od konfiguracji. Pierwsza instalacja bibliotek wymaga internetu. Aby wypróbować lokalnie zmieniony plik przed opublikowaniem go w repozytorium, użyj **Plik → Prześlij notatnik** w Colab i wybierz plik `.ipynb` z tego folderu.

W laboratoriach 0–3 najpierw przewiduj wynik, następnie uruchamiaj kod, zmieniaj założenia i wyjaśniaj różnice. Uczysz się także tworzyć własne wykresy i łączyć suwaki z funkcjami. Gdy widżet się nie wyświetla, skorzystaj z pokazanego obok bezpośredniego wywołania funkcji z wybranymi parametrami. Zadania oznaczone „DO ZROBIENIA” rozwijają działający kod początkowy.

Laboratoria 0–5 mają dane ćwiczeniowe w kodzie. Laboratorium 6 pobiera brakujące pliki ze wspólnego folderu `data/` w repozytorium. Domyślnie używa dostarczonej historii cen, zgodnej z datami przykładowych zamówień. Eksperyment z bieżącymi cenami FRED opisano w notatniku: po przełączeniu na dane aktualne trzeba ustawić terminy zamówień późniejsze od użytej historii.

## Praca lokalna

Z głównego folderu repozytorium zainstaluj biblioteki i uruchom Jupyter:

```bash
python -m pip install -r requirements.txt
python -m pip install jupyter
jupyter notebook
```

Otwórz notatnik z folderu `pl/`. Laboratorium 6 odnajduje dane również w `../data/`. Przed sprawdzeniem całego rozwiązania uruchom ponownie kernel i wykonaj wszystkie komórki po kolei.

## Słownictwo używane w kodzie i wynikach

Polska terminologia nawiązuje do wcześniejszych [materiałów MISP](https://github.com/AdoHaha/misp), zwłaszcza pojęć zmiennej decyzyjnej, funkcji celu, ograniczenia i rozwiązania dopuszczalnego. Nazwy funkcji, argumentów, kluczy danych i statusów solvera są zachowane w kodzie; ich znaczenie wyjaśniają notatniki.

| Nazwa angielska | Znaczenie |
|---|---|
| decision variable | zmienna decyzyjna |
| objective | funkcja celu |
| constraint | ograniczenie |
| feasible solution | rozwiązanie dopuszczalne |
| slack | luz ograniczenia; dla zasobu: niewykorzystana ilość |
| surplus | nadwyżka ponad wymagane minimum |
| binding constraint | ograniczenie aktywne — spełnione jako równość |
| shadow price / dual price | cena dualna (cena cienia); lokalna zmiana wartości celu przy zmianie prawej strony |
| reduced cost | koszt zredukowany |
| cutting stock / cutting pattern | problem rozkroju / wzorzec rozkroju |
| makespan | czas zakończenia wszystkich zadań |
| critical path / project slack | ścieżka krytyczna / zapas czasu czynności |
| crashing | skracanie czasu trwania czynności, zwykle za dodatkowy koszt |
| `Optimal` / `Infeasible` | znaleziono optimum / model nie ma rozwiązania dopuszczalnego |

Luz, nadwyżkę, ceny dualne i koszty zredukowane interpretuj zgodnie z rodzajem ograniczenia i modelem. W szczególności ceny dualne z modelu ciągłego nie opisują automatycznie zmian w modelu całkowitoliczbowym. Każdy eksperyment kończ sprawdzeniem statusu, ograniczeń i jednostek oraz porównaniem z rozwiązaniem bazowym.

Zapisane wyniki polskich notatników są wyczyszczone, aby studenci uzyskali je podczas własnego uruchomienia.
