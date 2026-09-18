Neuron Demonstration
====================

<div align="center"><img src="https://github.com/campagnola/neurodemo/blob/master/screenshot.png" width="800"></div>

This is a fork from the project by Luke Campagnola & Paul Manis (with a few bug fixes by Tom Jhou to the sequence plotter)


This is an educational simulation of a simple neuron.

* Hodgkin & Huxley channels
* Ersier et al. 1999 // Jolivet, Lewis & Gerstner (2004) cortical channels
* Destexhe 1993 Ih channel
* Current/voltage clamp electrode with access resistance
* Diagram of cell membrane with circuit schematic
* Realtime simulation and plotting of voltages, currents, open probabilities, gating parameters, etc.
* Analysis tool for generating I/V curves and similar analyses.
* Pure python simulation; relatively easy to add new channels

<div align="center"><img src="https://github.com/campagnola/neurodemo/blob/master/analysis_screenshot.png" width="500"></div>

Installation
------------

### Most users: download the app

If you just want to run the demo, download the prebuilt app for your platform from the
[Releases page](https://github.com/JhouLab/neurodemo/releases) — no Python installation required.

* **Windows**: download the `.exe` and double-click it to run. Will show a splash screen before opening.
* **macOS**: download the `.dmg`, open it, and drag the app to Applications. The app is not signed with an Apple developer certificate, so the first launch will be blocked; go to System Settings > Privacy & Security, scroll down and allow it there. This only allows this one app and does not otherwise weaken your Mac's security. 

### Advanced users: run from source

Requires Python 3.10 or higher, along with libraries in requirements.txt.

First clone the repository.

Using the command line:

```
git clone https://github.com/JhouLab/neurodemo.git
cd neurodemo
```

Or using [GitHub Desktop](https://desktop.github.com/): click "Add" > "Clone repository",
select `JhouLab/neurodemo` (or paste `https://github.com/JhouLab/neurodemo.git` under the URL
tab), choose a local path, and click "Clone".

**Option A: Plain Python, via scripts (venv)**

Windows: double-click `Create_env_windows.bat` once to set up the environment, then double-click
`Run_this_windows.bat` any time to launch the program.

macOS: double-click `Create_env_mac.command` once to set up the environment, then double-click
`Run_this_mac.command` any time to launch the program. (The first time, macOS may require you to
right-click the file and choose "Open" to bypass the unidentified-developer warning.)

Both scripts check if your Python is 3.10 or higher (installing from
[python.org](https://www.python.org/downloads/) first if needed) and create a local virtual
environment (`neurodemo_venv`) so the installed packages don't affect the rest of your system.

**Option B: Manually via command line**

If you'd rather do this manually instead of via scripts.

Type these commands from the `neurodemo` directory to install requirements and run:

Windows (cmd or PowerShell):

```
py -3 -m venv neurodemo_venv
neurodemo_venv\Scripts\activate
pip install -r requirements.txt
python neurodemo.py
```

macOS / Linux:

```
python3 -m venv neurodemo_venv
source neurodemo_venv/bin/activate
pip install -r requirements.txt
python neurodemo.py
```

**Option C: Anaconda / Miniconda**

```
conda create -n neurodemo python>=3.10
conda activate neurodemo
pip install -r requirements.txt
python neurodemo.py
```

Once installed, options B and C are launched by first re-activating the environment
(`conda activate neurodemo` or the `*/activate` commands above) and running `python neurodemo.py`.

### Maintainers: Build a standalone executable

**Windows `.exe`:** the [Build Windows app](.github/workflows/build-windows.yml) GitHub Actions
workflow builds it automatically. Trigger it from the "Actions" tab on GitHub ("Build Windows
app" > "Run workflow"), or by pushing a tag like `v1.2.0` (which also attaches the built `.exe`
to the corresponding GitHub Release). The finished `.exe` can be downloaded from the workflow
run's "Artifacts" section, or from the release link above.

If you'd rather build manually: create and activate a virtual environment as above,
install the dependencies plus `pyinstaller` and `Pillow` (needed to resize the splash image
from 1015x653 down to the 760x480 max), then run this from the repo root (so that the output
`dist/`/`build/` folders land there rather than inside `resources/`):

```
pip install pyinstaller Pillow
pyinstaller resources/neurodemo_windows.spec
```

This creates a `dist/` folder containing the standalone executable, and a `build/` folder of
intermediate files that can be ignored. The executable shows a splash screen for a few seconds
on launch.

**macOS `.dmg`:** the [Build macOS app](.github/workflows/build-mac.yml) GitHub Actions
workflow builds both Intel and Apple Silicon `.dmg` files automatically — no Mac required.
Trigger it from the "Actions" tab on GitHub ("Build macOS app" > "Run workflow"), or by pushing
a tag like `v1.2.0` (which also attaches the built `.dmg` files to the corresponding GitHub
Release). The finished `.dmg` files can be downloaded from the workflow run's "Artifacts"
section, or from the release.

If you'd rather build manually on a Mac instead: install the dependencies plus `pyinstaller`
and [create-dmg](https://github.com/create-dmg/create-dmg) (`brew install create-dmg`), then
run this from the repo root (same reason as above):

```
pyinstaller resources/neurodemo_mac.spec
mkdir -p dist/dmg
cp -r dist/neurodemo.app dist/dmg/
create-dmg --volname neurodemo --volicon resources/icon.icns \
  --app-drop-link 250 100 dist/neurodemo.dmg dist/dmg/
```

