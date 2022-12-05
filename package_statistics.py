import argparse
from argparse import RawTextHelpFormatter
import os
import gzip
from heapq import nlargest
import io

# Constants
DEBIAN_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"
NUMBER_OF_RESULTS = 10

# Dictionary for Packages
package_dictionary = {}


def download_content_indice_file(file):
    wget_command = "wget {} --no-check-certificate".format(file)
    os.system(wget_command)


def read_content_indice_file(file):
    gz = gzip.open(file, 'rb')
    f = io.BufferedReader(gz)
    for line in f:
        line = line.decode("utf-8")
        line = line.rstrip()
        file_name, space, package_name = line.rpartition(' ')
        # Case admin/molly-guard,admin/systemd-sysv,admin/sysvinit-core
        package_name = package_name.split(',')
        for package in package_name:
            # Grab package name After last /
            package = package.rpartition('/')[2]
            # Uniquessness in keys
            if package not in package_dictionary.keys():
                package_dictionary[package] = []
            package_dictionary[package].append(file_name)

    gz.close()
    for package in nlargest(NUMBER_OF_RESULTS,
                            package_dictionary, key=lambda e: len(package_dictionary[e])):
        print(
            "{: >20} {: >20}".format(package, len(package_dictionary[package]))
        )


parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
parser.add_argument('--arch',
                    help="Enter the architecture, e.g. amd64, arm64 etc.")
args = parser.parse_args()

if args.arch:
    content_indice_file = "Contents-{arch}.gz".format(
        arch=args.arch
    )
    content_indice_file_url = "{deb_mirror}{content_indice_file}".format(
        content_indice_file=content_indice_file,
        deb_mirror=DEBIAN_URL,
    )
    print("******************************************************")
    print("Downloading Content Index file: %s" % content_indice_file)
    print("Downloading from: %s" % content_indice_file_url)
    download_content_indice_file(content_indice_file_url)
    print("Reading Content Index file: %s " % content_indice_file)
    read_content_indice_file(content_indice_file)
