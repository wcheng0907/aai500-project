import os
import random

DIRECTORY_PATH = "./data"
TMP_OUTPUT_FILENAME = "tmp_house_data.csv"
OUTPUT_FILENAME = "house_data.csv"
TRAINING = "training_data.csv"
TESTING = "testing_data.csv"

def split_training_testing(source_filename):
    source = DIRECTORY_PATH + "/" + source_filename
    with open(source, "r") as f:
        lines = f.readlines()

    data_count = len(lines)
    training_data_count = round(data_count * 0.8)

    # we slipt data to 80% training data and 20% testing data
    # write training data
    training_file = DIRECTORY_PATH + "/" + TRAINING
    with open(training_file, "w") as f:
        for i in range(training_data_count):
            f.write(lines[i])

    # write testing data
    testing_file = DIRECTORY_PATH + "/" + TESTING
    with open(testing_file, "w") as f:
        for i in range(training_data_count + 1, data_count):
            f.write(lines[i])


def shuffle_data(source_filename, destination_filename):
    source = DIRECTORY_PATH + "/" + source_filename
    with open(source, "r") as f:
        lines = f.readlines()

    random.shuffle(lines)

    destination = DIRECTORY_PATH + "/" + destination_filename
    with open(destination, "w") as f:
        f.writelines(lines)

    # remove temporary file because we shuffle data and write to house_data.csv
    os.remove(source)

def parse_data(filenames, destination_filename, directory_path):
    destination = directory_path + "/" + destination_filename
    output_fp = open(destination, "w")

    for filename in filenames:
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

                # we are just interested in column 2 - 13
                output_fp.write(",".join(data[2:14]) + "\n")
                line = fp.readline().strip()

    output_fp.close()

def read_data_filename():
    filenames = os.listdir(DIRECTORY_PATH)
    
    return filenames

def main():
    filenames = read_data_filename()
    parse_data(filenames, TMP_OUTPUT_FILENAME, DIRECTORY_PATH)
    shuffle_data(TMP_OUTPUT_FILENAME, OUTPUT_FILENAME)
    split_training_testing(OUTPUT_FILENAME)

if __name__ == "__main__":
    main()