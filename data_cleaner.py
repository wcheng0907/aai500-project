import os
import random

DIRECTORY_PATH = "./data"
TMP_OUTPUT_FILENAME = "tmp_house_data.csv"
OUTPUT_FILENAME = "house_data.csv"
TRAINING = "training_data.csv"
TESTING = "testing_data.csv"

def validate_data_columns(data):
    for i in range(2, 12):
        if not data[i] or data[i] == "":
            return False

    return True

def shuffle_data(source_filename, destination_filename):
    source = DIRECTORY_PATH + "/" + source_filename
    with open(source, "r") as f:
        lines = f.readlines()

    random.shuffle(lines)

    destination = DIRECTORY_PATH + "/" + destination_filename
    with open(destination, "w") as f:
        f.write("PROPERTY TYPE,ADDRESS,CITY,ZIP OR POSTAL CODE,PRICE,BEDS,BATHS,LOCATION,SQUARE FEET\n")
        f.writelines(lines)

    # remove temporary file because we shuffle data and write to house_data.csv
    os.remove(source)

def parse_data(filenames, destination_filename, directory_path):
    destination = directory_path + "/" + destination_filename
    output_fp = open(destination, "w")

    for filename in filenames:
        if not filename.startswith("redfin_"):
            continue

        source_filename = directory_path + "/" + filename
        print("Parsing file: {}".format(filename))
        with open(source_filename, "r") as fp:
            line = fp.readline().strip()
            while line:
                data = line.split(",")
          
                # this is noise data, drop it off
                if len(data) < 27:
                    line = fp.readline().strip()

                    continue

                # remove header
                if data[0] == "SALE TYPE":
                    line = fp.readline().strip()

                    continue

                # remove the line if it has empty
                if not validate_data_columns(data):
                    line = fp.readline().strip()

                    continue

                # we are just interested in column 2 - 11
                output_fp.write(",".join(data[2:5] + data[6:12]) + "\n")
                line = fp.readline().strip()

    output_fp.close()

def read_data_filename():
    filenames = os.listdir(DIRECTORY_PATH)
    
    return filenames

def main():
    filenames = read_data_filename()
    parse_data(filenames, TMP_OUTPUT_FILENAME, DIRECTORY_PATH)
    shuffle_data(TMP_OUTPUT_FILENAME, OUTPUT_FILENAME)

if __name__ == "__main__":
    main()