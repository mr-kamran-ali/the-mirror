# The Mirror Project
**Detection of Implicit Racial Bias using EEG Data**

- [The Mirror](#the-mirror-project)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
    - [Running Locally](#running-locally)
  - [Built With](#built-with)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

* [Python](https://www.python.org/)
  

### Installing

Clone or download the repository to your local machine.
Then run `conda create --name the-mirror python=3.8` to create a conda environment called "the-mirror" with the correct python version. The run `conda activate the-mirror`. Since the requirements.txt is pip-syntaxed, run `pip install -r requirements.txt` after.

### Running Locally

Local app only records EEG data using OpenBCI hardware. For the test we used [Psytoolkit Online IAT Racism](https://www.psytoolkit.org/c/3.3.2/survey?s=DfJfv) online cognitive-psychological experiment. Psytoolkit can also be used offline by just opening `iat_race.html` file in any modern browser. 

**IMPORTANT: at the end of the experiment closing the running python code is important to save the final data from OpenBCI board. Pressing "q" will quit the program and save the data as well in the same directory. Closing the code in terminal will also save the data into the file**

*To run local app:*

**On MAC:**
* python main.py --board-id 2 --serial-port /dev/cu.usbserial-DM02587F

**On Windows:**
* python main.py --board-id 2 --serial-port COM3

**NOTE: Please verify the port names in your local PC**


## Built With

* [Python](https://python.org/) - Python Web Framework
* [Psytoolkit](www.psytoolkit.org/) - Psytoolkit for running cognitive-psychological experiments and surveys
* [OpenBCI](https://shop.openbci.com/collections/frontpage/products/cyton-daisy-biosensing-boards-16-channel?variant=38959256526) OpenBCI cyton and daisy boards


## Authors

* **Siddhant Gadamsetti** - *Developer* - [MSc Digital Health, Hasso Plattner Institute Potsdam, Germany](Siddhant.Gadamsetti@student.hpi.uni-potsdam.de)
* **Florian Hermes** - *Developer* - [MSc Digital Health, Hasso Plattner Institute Potsdam, Germany](Florian.Hermes@student.hpi.uni-potsdam.de)
* **Kamran Ali** - *Developer* - [MSc Digital Health, Hasso Plattner Institute Potsdam, Germany](kamran-ali.com)

## License

* *No Copyright from us on code contained in main.py*
* *For Copyrights of libraries and tools used in the app please visit respective library documents, library list is included in requirements.txt*
* *For psytoolkit.org please visit [Their Website](www.psytoolkit.org)*

