import datetime
import json
import sys
import csv
import os

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT_MS = "%Y-%m-%dT%H:%M:%S.%f%z"

def parse_single_file(in_file: str, out_file: str, append: bool=False):
    print(f'Loading file {in_file}')

    # Parses json data
    json_data = None

    with open(in_file, encoding="utf8") as json_file:
        json_data = json.load(json_file)

    if json_data is None:
        print(f'{in_file} is either an empty file or does\'t exist!')
        return

    # Checks if the out file already has the field names as a header
    has_header = False

    if os.path.exists(out_file):
        with open(out_file, encoding="utf8") as csv_file:
            reader = csv.DictReader(csv_file)

            has_header == reader.fieldnames != None

    # Writes data to the out file
    with open(out_file, 'a' if append else 'w', encoding="utf8") as csv_file:
        fieldnames = ["lon", "lat", "from_date", "to_date", "location"]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if not has_header:
            writer.writeheader()

        for places in json_data["timelineObjects"]:
            try:
                place_visit = places["placeVisit"]
            
                lon = place_visit["location"]["longitudeE7"]
                lon = lon / 10000000

                lat = place_visit["location"]["latitudeE7"]
                lat = lat / 10000000

                from_date_raw = place_visit["duration"]["startTimestamp"]
                used_format = DATE_FORMAT_MS if from_date_raw[19] == "." else DATE_FORMAT
                from_date = datetime.datetime.strptime(from_date_raw, used_format)

                to_date_raw = place_visit["duration"]["endTimestamp"]
                used_format = DATE_FORMAT_MS if to_date_raw[19] == "." else DATE_FORMAT
                to_date = datetime.datetime.strptime(to_date_raw, used_format)

                location = place_visit["location"]["name"]
                
                writer.writerow({"lon": lon, "lat": lat, "from_date": from_date,
                        "to_date": to_date, "location": location})
            except KeyError:
                continue
        
        print(f'Finished writting from {in_file} locations to file ${out_file}')

def parse_folder(in_folder, out_file):
    files = __get_files__(in_folder)

    for file in files:
        if file.lower().endswith(".json"):
            parse_single_file(file, out_file, True)

def __get_files__(path):
    files = []

    for root, dirs, files_in_dir in os.walk(path):
        for file in files_in_dir:
            files.append(os.path.join(root,file))
    
    return files

def check_input(args):
    append = False
    folder = False

    in_path = out_file = ""

    for i in range(len(args)):
        arg = args[i]

        if arg == "-a": append = True
        elif arg == "-f": folder = True
        elif arg == "-in":
            if i + 1 < len(args):
                in_path = args[i + 1]
        elif arg == "-out":
            if i + 1 < len(args):
                out_file = args[i + 1]
    
    if not folder:
        if not in_path.lower().endswith(".json"): in_path = in_path + ".json"
    if not out_file.lower().endswith(".csv"): out_file = out_file + ".csv"

    if not os.path.exists(in_path):
        if not folder:
            raise IOError(f'File {in_path} does not exist!')

    if not folder and os.path.isdir(in_path):
        raise IOError(f'The given input, {in_path}, is a folder!')
    
    if folder and not os.path.isdir(in_path):
        raise IOError(f'The given input, {in_path}, is not a folder!')
    
    return append, folder, in_path, out_file

if __name__ == "__main__":
    append, folder, in_path, out_file = check_input(sys.argv)

    print(f'Parsing goole location history data from {"folder" if folder else "file"} ./{in_path} to file {out_file}')
    
    if not folder: parse_single_file(in_path, out_file, append)
    else:          parse_folder     (in_path, out_file)