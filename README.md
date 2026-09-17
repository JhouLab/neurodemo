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


Requirements
------------

* Python 3.10 or higher
* NumPy, SciPy
* PyQt5 or 6
* PyQtGraph
* lmfit
* MetaArray


Installation
------------

### Most users: download the app

If you just want to run the demo, download the prebuilt app for your platform from the
[Releases page](https://github.com/JhouLab/neurodemo/releases) — no Python installation required.

* **Windows**: download the `.exe` and double-click it to run. Will show a splash screen before opening.
* **macOS**: download the `.dmg`, open it, and drag the app to Applications. No splash screen appears, and may take up to 30 seconds to open. The app is not signed with an Apple developer certificate, so the first launch will be blocked; go to System Settings > Privacy & Security and allow it there. This only allows this one app and does not otherwise weaken your Mac's security.

### Running from source (intermediate users)

If you want to run from source instead (e.g. to modify the code), first clone the repository.

Using the command line:

```
git clone https://github.com/JhouLab/neurodemo.git
cd neurodemo
```

Or using [GitHub Desktop](https://desktop.github.com/): click "Add" > "Clone repository",
select `JhouLab/neurodemo` (or paste `https://github.com/JhouLab/neurodemo.git` under the URL
tab), choose a local path, and click "Clone".

**Option A: Plain Python (venv)**

Windows: double-click `Create_Env.bat` once to set up the environment, then double-click
`Run_this.bat` any time to launch the program.

macOS: double-click `Create_Env.command` once to set up the environment, then double-click
`Run_this.command` any time to launch the program. (The first time, macOS may require you to
right-click the file and choose "Open" to bypass the unidentified-developer warning.)

Both scripts check that your Python is 3.10 or higher (installing from
[python.org](https://www.python.org/downloads/) first if needed) and create a local virtual
environment (`neurodemo_venv`) so the installed packages don't affect the rest of your system.

If you'd rather do this manually from the command line instead of using the scripts:

All commands below must be run from inside the `neurodemo` directory:

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

**Option B: Anaconda / Miniconda**

```
conda create -n neurodemo python>=3.10
conda activate neurodemo
pip install -r requirements.txt
python neurodemo.py
```

Once installed, you can launch the demo by re-activating the environment
(`conda activate neurodemo` or the `activate` step above) and running `python neurodemo.py`.

### Building a standalone executable (maintainers)

**Windows `.exe`:** create and activate a virtual environment as above, install the
dependencies plus `pyinstaller` and `Pillow` (needed to resize the splash image from
1015x653 down to the 760x480 max), then run:

```
pip install pyinstaller Pillow
pyinstaller neurodemo_windows.spec
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
and [create-dmg](https://github.com/create-dmg/create-dmg) (`brew install create-dmg`), then:

```
pyinstaller neurodemo_mac.spec
mkdir -p dist/dmg
cp -r dist/neurodemo.app dist/dmg/
create-dmg --volname neurodemo --volicon icon.icns \
  --app-drop-link 250 100 dist/neurodemo.dmg dist/dmg/
```

First launch on macOS can take up to ~30 seconds (no splash screen is shown).
