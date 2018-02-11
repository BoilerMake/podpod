# PodPod Communication

## Project Status
Project is now deprecated.

## Info
This script is used to communicate with the BoilerMake Backend, and allows for ID barcodes to be scanned and then recorded on the API server. We used a Raspberry Pi to process the scanner input.

### Prerequisites and Installation
* You must have the [BoilerMake Backend](https://github.com/BoilerMake/backend) installed
    * Setup the backend and generate a `PODPOD_KEY`
* [Install Python 3](https://www.python.org/)
* [Install Requests](http://docs.python-requests.org/en/master/)
* Copy `config.sample.ini` to `config.ini` and fill in your details. Make sure that your API url does **not** have a trailing slash

Make sure that your Raspberry Pi is connected to the internet, and has a USB Barcode Scanner plugged in. Then, execute `sudo python task.py`

If you want to run this on a desktop or laptop, run the script with the `--stdin` option.

Use `--help` to view all options.
