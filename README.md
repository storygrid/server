# server
## Setup
Install all required packages via `requirements.txt`.

## Running Flask App
Under `server/Backend` run command `flask --app main run` to start the Flask App.

## Building the Executable

### Make sure you have pyinstaller installed
If not run: `pip3 install pyinstaller`

### Build the Executable
`pyinstaller --onefile --add-data "templates:templates" --add-data "static:static" storygrid.py`
