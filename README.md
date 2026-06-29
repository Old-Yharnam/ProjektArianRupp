# ProjektArianRupp

Kurze Übersicht zum lokalen Bauen und Ausführen.

## Make-Targets

Die Make-Targets befinden sich in `PythonBackendFrontend/Makefile`:

- `make install`
  - Erstellt eine virtuelle Umgebung (`.venv`)
  - Aktualisiert `pip`
  - Installiert Abhängigkeiten aus `requirements.txt`
- `make run`
  - Startet das Python-Projekt mit `app.py` aus der virtuellen Umgebung
- `make clean`
  - Entfernt die virtuelle Umgebung (`.venv`)

## Projekt lokal bauen

### 1) PythonBackendFrontend

In den Ordner wechseln und Targets ausführen:

```powershell
cd PythonBackendFrontend
make install
make run
```

Optional aufräumen:

```powershell
make clean
```

### 2) ESPCodeC / AnaeherungsSensor (ESP-IDF)

Der ESP-Teil ist ein ESP-IDF-Projekt und wird mit `idf.py` gebaut.

```powershell
cd ESPCodeC/AnaeherungsSensor
idf.py build
```

Nützliche zusätzliche Build-Targets sind im `CMakeLists.txt` definiert:

- `idf_fullclean` -> führt `idf.py fullclean` aus
- `idf_build` -> führt `idf.py build` aus
- `idf_flash` -> führt `idf.py flash` aus
- `idf_clean_build_flash` -> führt `fullclean`, `build`, `flash` nacheinander aus

Beispiel (über CMake-Target):

```powershell
cmake --build . --target idf_build
```
