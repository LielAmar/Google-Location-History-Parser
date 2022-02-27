# Google Location History Parser

[![License](https://img.shields.io/badge/License-MIT-%23ff7057?style=flat)](https://github.com/LielAmar/2FA/blob/master/LICENSE)
[![Discord](https://img.shields.io/discord/416652224505184276?color=%235865F2&label=Join%20Our%20Discord)](https://discord.gg/NzgBrqR)
<br>

## Information
Google Location History Parser is a python script used to parse json data downloaded through Google Takeout, into a .csv file which can be used to import data into Google Maps.

## Features
* Parse a single .json file
* Parse an entire folder and its sub-folders containing .json files
* Append to an existing file or create a new file

## Using Google Location History Parser
Simply clone the repository using `git clone https://github.com/LielAmar/Google-Location-History-Parser` and run the `parser.py` file.
```cmd
python3 parser.py <-a> <-f> -in [in-folder/in-file] -out [out-file]
```

## Command Line Arguments

* `-f`   whether the input path is a directory or file
* `-a`   whether the script should append data to an existing out file
* `-in`  input path
* `-out` output path

## Examples

```cmd
python3 parser.py -a -f -in locations -out out.csv
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
