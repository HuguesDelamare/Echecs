## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Installation](#installation)
* [Contributor](#contributor)


## General info
<p>The project is an offline chess tournament app, this app will be a replacement of the old one because of lots of problems due to net issues.The purpose of this is to correct this problem so the organizer of the chess tournament can have access to the datas and can send the result to the website even if the website is offline.</p>
	


## Technologies
Project is created with:
* Python version: 3.9
* Flake8 : 3.8.4
* Tinydb : 4.4.0


## Installation
* Make sure you have Python 3.7+ installed. (I developed it with Python 3.9).
* Installing pip will be needed to install packages. (pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org)
* Some Python modules are required which are contained in requirements.txt and will be installed below.

<h3>Installing the requirements</h3>

<h4>Python</h4>
To make sure Python is installed on windows :
 
    python --version

On Linux, Python 3.x users may need to use: 
    
    python3 --version

If you get a "Python is not defined" message, you'll need to download it at [The python site](https://www.python.org/downloads/)
<h4>How to install PIP</h4>
on Windows :

1. Download the [get-pip.py installer](https://bootstrap.pypa.io/get-pip.py) Either way, right-click on the link and select Save As... and save it to any safe location, such as your Downloads folder. 

2. Open the Command Prompt and navigate to the get-pip.py file

3. Run the following command: `python get-pip.py`

on Mac :

    sudo easy_install pip

on Linux (Advanced Package Tool (Python 3.x)) :

    sudo apt-get install python3-pip

<h4>Installing Git</h4>
You can go the official GitHub [website](https://git-scm.com/downloads) to intall it.
    

<h3>Installing the project</h3>
Open your terminal (CMD).

Choose the destination where you want to put folder that will contain the project:

    > cd YourFolderPath

Once you've picked a path for your folder we can create that folder:

	> mkdir FolderName

Now, we can clone the project in our folder by using the github https method (don't forget to be in the folder you just created):

	> git clone https://github.com/HuguesDelamare/Echecs.git

Enter now in the project we just downloaded 

    > cd Echecs

Installing the python environement in this folder:

  	> py -m venv YourEnvironementName

After installing the environement:

	> YourEnvName\Scripts\activate

We can now install all the libraries necessary for the project:

	> py -m pip install -r requirements.txt

The environement is functional we can now start the project:

	> py main.py

The project should start and you'll see infos of the script progression in your terminal.	
Here is a command line to create a html flake8 report.Don't forget to exclude your environement(env or venv) folder to avoid extra errors messages.
	
	> flake8 --format=html --htmldir=flake-report --exclude= "your path to the env folder in project"
	
## Contributor
  This application has been developped by [myself](https://github.com/HuguesDelamare).
  A big thank you to my mentor Alexandre Iwanesko  for helping me during the project.

