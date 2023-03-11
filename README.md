<h1 align="center"> Tolio - Offline Portfolio Tracker </h1>
<p align="center"><img
  src="/src/assets/icons/tolio_icon.png"
  alt="Alt text"
  title="Tolio"
  style="display: inline-block; margin: 0 auto; max-width: 300px"></p>


![GitHub](https://img.shields.io/github/license/jozhw/tolio) ![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/jozhw/tolio?include_prereleases) ![GitHub all releases](https://img.shields.io/github/downloads/jozhw/tolio/total?logo=Github) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jozhw/tolio) ![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/jozhw/tolio/v0.2.3) ![Scrutinizer code quality (GitHub/Bitbucket)](https://img.shields.io/scrutinizer/quality/g/jozhw/tolio) [![Downloads](https://static.pepy.tech/personalized-badge/tolio?period=total&units=international_system&left_color=black&right_color=orange&left_text=PyPI%20Downloads)](https://pepy.tech/project/tolio)


```
VERSION 0.2.3

Languages: Python 3.10.9 | Rust 1.66.0

Tailored Dependency: tolio==0.2.3
  - Linux: Python 3.8.0 > supported version >= 3.7.1 support only
  - MacOS: supported version >= Python 3.10.0

Supports: MacOS and Linux

```

### How to Run - MacOS(Python 3.10.0+) or Linux(3.8.0 > >= 3.7.1)
---
Create a virtual environment and make sure you are in the tolio directory in the terminal and run the following commands in the terminal.

```
# Clone the repository
git clone https://github.com/jozhw/tolio.git

# install tolio from pypi
pip install tolio

# use this command if the above does not work
pip install --upgrade tolio

# Run only if it is your first time running the application
./install_dependencies.sh

# To run the program
./run.sh

```

### How to Run - Unsupported Python Versions & Windows
---
Must download the rust programing language along with cargo, rust's package manager. You also need to make sure that maturin is installed.

Note: This application has not been tested on windows. There may be instances where some of the functionalities may fail. Please let me know if this is the case for windows users.

```
# Install rust with cargo for macos or linux and configure the path
export PATH="$HOME/.cargo/envbin:$PATH" ; curl https://sh.rustup.rs -sSf | sh -s -- -y ; source "$HOME/.cargo/env"

# Install rust and cargo for windows
https://forge.rust-lang.org/infra/other-installation-methods.html

# Install maturin
pip install maturin

# Install from requirements.txt
pip install -r requirements.txt

# run the program
./run.sh

```

### Appearance
---
With the help of using <a href="https://github.com/TomSchimansky/CustomTkinter">customtkinter</a> and some personal hacking, Tolio can sync with the operating system's appearance setting. To use this feature, on the appearance mode setting for the application, select "System".


https://user-images.githubusercontent.com/112655410/222914413-a3dbf50e-550f-45b8-a88f-5a557488b88f.mp4


### Details
---
* The data stored (portfolio.db) or exported (transactions_data.csv) will be in the tolio repository.

* This application supports stock splits, fractional shares, and the recording of long securities.

* More details comming soon!

