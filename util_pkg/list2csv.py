import workutil, csv, argparse, sys


def parse_list_stream(list_in, csv_out):
    writer = csv.writer(csv_out)
    record_count = 0
    active_line_out = []
    header_list = []
    header_ready = False
    for line_num, line in enumerate(list_in):

        # Remove line endings
        line = line.strip()

        # Skip empty lines
        if len(line) == 0:
            continue

        # Separate label and value
        sep = line.split(":")
        if len(sep) != 2:
            # Unexpected scenario, skip this line
            print(f'Skipping line {line_num + 1}, incorrect number of colons on a single line: exactly one colon '
                  f'permitted per line')
            continue
        label = sep[0].strip()
        value = sep[1].strip()

        if label not in header_list:
            if not header_ready:
                # Keep track of new labels
                header_list.append(label)
            else:
                # We'll have to skip this one, we learned about the label too late
                print(f'Skipping line {line_num + 1}, unknown label: all list items must include the same labels in the'
                      f' same order')
                continue
        elif label == header_list[0]:
            # Start of new line, write out prev line and recycle variables
            if not header_ready:
                header_ready = True
                writer.writerow(header_list)
            writer.writerow(active_line_out)
            record_count += 1
            active_line_out.clear()

        col_num = header_list.index(label)
        active_line_out.insert(col_num, value)
    
    # Write out final line
    writer.writerow(active_line_out)

    return record_count


def run_standalone():
    arg_parser = argparse\
        .ArgumentParser(description='Parse a list of paragraph records with colon-separated key value pairs.')
    arg_parser.add_argument('-I', dest='file_in', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                            help='input list of paragraph records')
    arg_parser.add_argument('-O', dest='file_out', nargs='?', type=argparse.FileType('w'),
                            default=workutil.gen_out_filename('list'), help='output csv file')

    args = arg_parser.parse_args()
    with args.file_out as csvfile:
        with args.file_in as f:
            record_count = parse_list_stream(f, csvfile)
            print(f'All done! {record_count} record(s) written to {args.file_out.name}')


if __name__ == '__main__':
    run_standalone()