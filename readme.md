# Lily Data Logger Studio

Universal data logger software aiming to work with any kind of electronics measurement device.
Not only logging data but also controlling instruments (process automation).

## Releases

No releases yet, still work in progress.
Things to do for the first release:

* Add/edit/delete instruments
* Add/edit/delete process steps
* Add/delete measurements
* Edit configuration
* Save/load configurations
* Start/Stop data logger
* Export measurements to CVS
* Check instruments
* Add the following instruments:
  * TDS220 oscilloscope (or compatible TDS200, TDS1000 and TDS2000, they have the same interface)
  * NI USB-6009 (requires drivers from NI)
  * Protek 506 digital multimeter
  * Arduino Uno IO module (reading analog voltages, reading and writing digital IO, sketch for the Arduino Uno is included in this repo)
  * Add simulated instruments (for demo/testing the application):
    * multimeter giving some random values
    * temperature chamber
 
## Installation

Requirements for running the application:

* Python
* Upgrade pip: python -m pip install --upgrade pip
* pip install -r requirements.txt


## Instruments

Instruments are defined in JSON formatted files and can be exported from or imported in to the application.
This way anyone can create their own instrument files and use them in the application.

A JSON file can be created in a text editor.

Instrument file format:

```json
{
  "name": "my power supply",
  "interface": {
    "type": "serial",
    "baud_rate": 115200,
    "parity": "none",
    "data_bits": 8,
    "stop_bits": 1,
    "flow_control": "off",
    "time_out": 2
  },
  "channels": [
    {
      "name": "get voltage",
      "type": "input",
      "command": "U?\n",
      "response": "U={float}V\n"
    },
    {
      "name": "set voltage",
      "type": "output",
      "command": "U={float:2,3}V\n",
      "response": "OK\n"
    }
  ]
}
```

This JSON file describes a simple power supply instrument with 2 channels for reading and setting the voltage.

The name is obviously the name of the instrument, this usually is the manufacturer type number.

The interface section defines the interface type and the default values.
These values can be overridden in the application.

The channels sections described the channels.

The first channel is for reading out the voltage (get voltage).
The type is input and the command and expected response are defined.
The keyword `{float}` indicates we expect a floating point value there.
The application will try to match the actual response with this definition and returns the extracted value as a floating point.

The second channel is for setting the desired output voltage (set voltage). This can be used in process automation.
The command has a keyword `{float:2,3}` the desired value, will be converted to a string with a floating point representation.
The representation will have 2 digits before the decimal point and 3 digits behind the digital point.
For example if the desired value is 3.5V this will be sent as: `U=03.500V`.
There are a number of variations possible:

* `{float}`: a floating point with as many digits as required.
* `{float:,3}`: a floating point with as many digits as required before the decimal point and 3 digits behind the decimal point
* `{float:1-3,0-3}`: a floating point with 1 to 3 digits before the decimal point and 0 to 3 digits behind the decimal point.
* `{int}`: an integer with as many digits as required.
* `{int:3}`: an integer with three digits using leafing zeros if needed.
* `{str}`: a literal string value with undefined length.
* `{str:32}`: a literal string value with a length of 32 characters, spaces will be added at the end of the string to match the length.

2023 - LilyTronics (https://lilytronics.nl)
