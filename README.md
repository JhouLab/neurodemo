Neuron Demonstration
====================

<div align="center"><img src="https://github.com/campagnola/neurodemo/blob/master/screenshot.png" width="800"></div>

Luke Campagnola & Paul Manis


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


Installation
------------

The easiest way to run this is via the standalone executables I already made (see bottom of this page). That requires no knowledge of Python or command line jargon.

Other ways to run from source code. All of these may require using the command line at least a little bit:

1. Using base Python:

   This is my personal preference due to ease and simplicity. Install Python from www.python.org, then open a command prompt, and install dependencies:

   > pip install numpy scipy PyQt6 pyqtgraph lmfit MetaArray

   Download the neurodemo source code from https://github.com/campagnola/neurodemo or https://github.com/JhouLab/neurodemo and click the "Download ZIP" button on the right side of the page. Unzip the file to directory that is easily accessible to you, then open a command prompt, cd to that directory, and type:

   > python -m neurodemo.py

   This should run the program.

2. Using Anaconda/miniconda:
    
    a. Python novices are often told to use Anaconda, but that is extreme overkill for this project, which only needs four of the 300+ packages that Anaconda comes bloated with. If you really want to go that route, download it here (http://www.anaconda.com), then install lmfit, pyqtgraph, and MetaArray, which Anaconda doesn't have by default:

    > conda install lmfit

    c. Then install pyqtgraph and MetaArray:

    > pip install pyqtgraph MetaArray

    d. Finally, download the neurodemo source by going to http://github.com/campagnola/neurodemo and clicking the "Download ZIP" button on the right side of the page. Unzip the file to a convenient directory, and run from there.

3. Create a single standalone executable file to distribute to others.

    - Git clone the repository. 
    - Create *and activate* a python virtual environment (venv) in the main repository directory and install all dependencies. Also, install pyinstaller:
    -     pip install pyinstaller
    - Install Pillow, which is needed because the splash image size (1015x653 pixels) is bigger than max (760x480)
    -     pip install Pillow
    - At the command line, cd to main repository directory, making sure the venv is active, then enter one of the following, based on whether you are on Windows or Mac:
    -     pyinstaller neurodemo_windows.spec
    -     pyinstaller neurodemo_mac.spec
    - This will create a subfolder "dist" containing a stand-alone executable that you can run by double-clicking. It will also create a subfolder "build" with intermediate files that you can generally ignore.
    - 
    - The Windows executable should take 4-5 seconds to launch, during which it shows a splash screen. The splash screen feature is not compatible with Mac. The Mac version also might take curiously long to launch (almost 30 seconds). Not sure why, but it seems fine after that.
    - I recommend converting the Mac executable to a dmg file using the Disk Utility app in MacOS. This preserves the executable permissions so that others can run it without having to run chmod. Go to "File", "New Image", "Image from folder", then choose either "read only" or "read/write". (There is also a compressed option, but it failed for me)


Running the Demo
----------------

You can launch the demo from the terminal by navigating to the location where you extracted the source code (eg, `cd Downloads\neurodemo\`) and then typing `python neurodemo.py`.

Windows: Open the folder where you extracted the neurodemo source code. Right click `demo.py` and select "Open with..". Navigate to the location where you installed anaconda or miniconda (you may need to click something like "browse" or "choose another application" depending on your version of windows). Select `python.exe`.

macOS: You can launch as above, or install the dmg file and just start the app. 



Link to standalone executables (Windows and Mac M1 versions):
----------------

Here is a folder containing several standalone executables:
https://www.dropbox.com/scl/fo/grh1ihu307gn4vfzljgnt/AJnmBrKSig-7XWAAWVYLoIs?rlkey=i366zvvfd3r5rwki1qh2t6vry&dl=0

Click the download link for the version you want (Windows or M1 Mac). You may see a dialog asking you to sign into Dropbox. At the bottom will be a link "continue with download only". Select that to bypass logging in.

The Mac version is a dmg file. Double click it, and it will mount a virtual disk containing a single executable file. Running it will be initially blocked because I have not paid $99/year to Apple to make this an officially sanctioned app. You have to enable it in the "Privacy and Security" settings. This will enable just this app, and does not leave you vulnerable to malicious software.
