import os
import tarfile
import requests


def downloadData(dataset_directory="./input/"):
    """
    Downloads Berkley segmentation dataset and extracts it
    :param dataset_directory: Path where dataset has to be stored
    :return: None
    """

    urls = ["http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/BSR/BSR_bsds500.tgz"]

    for url in urls:
        if not os.path.isdir(dataset_directory):
            os.makedirs(dataset_directory)

        # Check if the dataset has been downloaded, else download and extract it
        file_name = dataset_directory + "dataset.tgz"
        if os.path.isfile(file_name):
            print("{} already downloaded. Skipping download.".format(file_name))
        else:
            print("Downloading '{}' into '{}' file".format(url, file_name))

            data_request = requests.get(url)
            with open(file_name, "wb") as file:
                file.write(data_request.content)

            print("Extracting {} into {}".format(file_name, dataset_directory))
            if file_name.endswith("tgz"):
                tar = tarfile.open(file_name, "r:")
                tar.extractall(path=dataset_directory)
                tar.close()
            else:
                print("Unknown format.")

    print("Input data setup successful.")
