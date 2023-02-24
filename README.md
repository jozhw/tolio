<h1 align="center"> Tolio - Offline Portfolio Tracker </h1>

<p align="center"><img
  src="/src/assets/icons/tolio_icon.png"
  alt="Alt text"
  title="Tolio"
  style="display: inline-block; margin: 0 auto; max-width: 300px"></p>


![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/jozhw/tolio?include_prereleases) ![GitHub all releases](https://img.shields.io/github/downloads/jozhw/tolio/total?logo=Github) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jozhw/tolio) ![GitHub commits since latest release (by date including pre-releases)](https://img.shields.io/github/commits-since/jozhw/tolio/v0.1.1) ![GitHub](https://img.shields.io/github/license/jozhw/tolio) 



```
VERSION 0.2.0 
Python 3.10.8 | Rust 1.66.0 
```

### How to Run
Create a virtual environment and make sure you are in the tolio directory in the terminal and run the following commands in the terminal.

```
# Clone the repository

git clone https://github.com/jozhw/tolio.git

# Download the .whl file from Tolio releases and in the env

pip install <ADD FILENAME>.whl
- if the above does not work, it is most likely because the package has been previously installed
- if this is the case do the following
pip install --upgrade --force-reinstall {ADD FILENAME}.whl

# Run only if it is your first time running the application

 ./install_dependencies.sh  
 
# To run the program

 ./run.sh  

```

### Details

* The data that you enter into the application will be stored locally on your device in the portfolio.db file in the src directory. 

* This application supports stock splits, fractional shares, and the recording of long securities.

* Documentation will be coming for the official version.
