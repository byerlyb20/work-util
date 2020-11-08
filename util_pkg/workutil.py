import sys
import datetime


def gen_out_filename(util_name, extension='.csv'):
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    return f'{util_name}_{timestamp}{extension}'


def run_standalone():
    if len(sys.argv) <= 1:
        print("usage: workutil.py [list2csv|merge]")
        return

    command = sys.argv[1]

    # Strip the workutil.py script location for clearer usage messages that reference the name
    # of the actual tool
    sys.argv.pop(1)
    sys.argv[0] += f" {command}"

    if command == 'list2csv':
        import list2csv
        list2csv.run_standalone()
    elif command == 'merge':
        import merge
        merge.run_standalone()


if __name__ == '__main__':
    run_standalone()
