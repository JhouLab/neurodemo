Neuron Demonstration
====================

<div align="center"><img src="https://github.com/campagnola/neurodemo/blob/master/screenshot.png" width="800"></div>

Luke Campagnola & Paul Manis


This is an educational simulation of a simple neuron.

* Hodgkin & Huxley channels
* Lewis & Gerstner (2002) cortical channels
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

The easiest way to run this is via the standalone executables I have already made (see bottom of this page).

Other ways to install:

1. Using Anaconda/miniconda:
    
    a. Experienced Python users can install the requirements listed above, then download the neurodemo code and run `neurodemo.py`. For everybody else, I recommend installing the [Anaconda Python distribution] (http://continuum.io/downloads). Download and run the installation package for your platform. To keep the size down, you can instead install [miniconda] (http://conda.pydata.org/miniconda.html). When you run the installer, _take note of the location it is installing to_.

    b. If you installed miniconda, then it is necessary to manually install numpy, scipy, and pyqt6 (if you installed Anaconda, then these packages are already installed and you can skip this step, except for lmfit). This can be done from a terminal:

    ```
    > conda install numpy scipy pyqt pyqtgraph lmfit
    ```

    c. Install pyqtgraph (this is required regardless of which python distribution you installed):

    ```
    > pip install pyqtgraph
    ```

    d. Download the [neurodemo source code] (https://github.com/campagnola/neurodemo/archive/master.zip). You can find this by going to http://github.com/campagnola/neurodemo and clicking the "Download ZIP" button on the right side of the page. Unzip the file and you are ready to begin!

2. To get the latest version that runs with Python 3.10 and PyQt6 you can follow these steps, depending on your system. Note that these all create and use Python virtual environments rather than conda/mminiconda environments.
    
    a. Windows
    -  Git clone the repository.
    - In the main directory, under the windows cmd terminal, run win_install.bat.
    - Create a shortcut on the desktop to the file win_start_demo.bat, and set the "window" to minimized. 
        Clicking on the shortcut should start the program. 
    
    b. macOS
    - Git clone the repository.
    - In the main directory, using a zsh or bash terminal, run ./make_local_env.sh. This should create the environment, install all the required packages, and leave you with the environment activated. 
    -  type "python demo.py" to run the program. 
    - To make an installable file (dmg), run the shell script that is appropriate for the processor: make_M1_dmg.sh or make_x86_64_dmg.sh. The resulting dmg file will be in the folder dist/demo_(architecture).dmg. You can then install the app as you would with any other dmg file.  

3. Create a single standalone executable file to distribute to others.

    - Git clone the repository. 
    - Create *and activate* a python virtual environment (venv) in the main repository directory and install all dependencies. Also, install pyinstaller:
    -     pip install pyinstaller
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
