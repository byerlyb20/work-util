import argparse
import os


def rename_files(start):
    files = [f for f in os.listdir() if os.path.isfile(f)]
    files.sort()

    for file in files:
        name, extension = os.path.splitext(file)
        os.rename(file, f"{start}-1{extension}")
        #print(f"{file} -> {start}{extension}")
        start += 1


def run_standalone():
    arg_parser = argparse \
        .ArgumentParser(description='Rename all files in the directory in ascending alphabetical order to record'
                                    'attachment names.')
    arg_parser.add_argument('-s', dest='start', nargs='?', type=int, required=True,
                            help='beginning record number')

    args = arg_parser.parse_args()
    rename_files(args.start)
    print(f'All done!')


if __name__ == '__main__':
    run_standalone()
