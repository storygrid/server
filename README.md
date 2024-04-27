# server
Compiled executables available for both Mac and Windows can be found on the [releases page](https://github.com/storygrid/server/releases/).
## Setup
Install all required packages via `requirements.txt`.

## Running Flask App
Run `python storygrid.py` to start the flask app. It will automatically open the front end and generate the required folder to store audio files.

## Building the Executable

### Make sure you have pyinstaller installed
If not run: `pip3 install pyinstaller`.

### Build the Executable
Run the following command `pyinstaller --onefile --add-data "templates:templates" --add-data "static:static" storygrid.py`.

This will create a executable `dist/storygrid`.
