import argparse
import os


def rename_files(start, verbose, force):
    files = [f for f in os.listdir() if os.path.isfile(f)]
    files.sort()

    filenames = [(file, os.path.splitext(file)) for file in files]
    red_flags = [extension != ".pdf" for file, (name, extension) in filenames]

    if any(red_flags) and not force and not verbose:
        print("Aborting: directory contains files that are not of type PDF")
        return

    for file, (name, extension) in filenames:
        if verbose:
            print(f"{file} -> {start}{extension}")
        else:
            os.rename(file, f"{start}-1{extension}")
        start += 1


def run_standalone():
    arg_parser = argparse \
        .ArgumentParser(description='Rename all files in the directory in ascending alphabetical order to record'
                                    'attachment names.')
    arg_parser.add_argument('-s', dest='start', nargs='?', type=int, required=True,
                            help='beginning record number')
    arg_parser.add_argument('-v', dest='v', nargs='?', type=bool, const=True, default=False, required=False,
                            help='print new filenames without renaming files')
    arg_parser.add_argument('-F', dest='force', nargs='?', type=bool, const=True, default=False, required=False,
                            help='force rename in directories with non-PDF files')

    args = arg_parser.parse_args()
    rename_files(args.start, args.v, args.force)
    print(f'All done!')


if __name__ == '__main__':
    run_standalone()
