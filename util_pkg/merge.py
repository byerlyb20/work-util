import argparse
import sys
import workutil

import q


def build_select_list(statement):
    # Build a SELECT table list, combining analogous fields with the coalesce function
    select_cols = ''
    if not statement:
        select_cols = 'a.*, b.*'
    else:
        display_fields = statement.split(",")
        for field in display_fields:
            field = field.strip()
            if '=' in field:
                eq_fields = field.split("=")
                if len(eq_fields) != 2:
                    print('Incorrect number of analogous fields, ignoring display field')
                    continue
                field = f"COALESCE({eq_fields[0]},{eq_fields[1]})"
            if select_cols:
                select_cols += ","
            select_cols += field
    return select_cols


def build_query(select_cols, key_a, key_b, file_a, file_b):
    # Build the SQLite query
    # Since SQLite does not support FULL OUTER JOIN, we immitate the functionality by combining two LEFT OUTER JOIN
    # operations as follows
    query_merge = f"""SELECT {select_cols}
    FROM {file_a} AS a
        LEFT JOIN {file_b} AS b
            ON a.{key_a} = b.{key_b}
    UNION ALL
    SELECT {select_cols}
    FROM {file_b} AS b
        LEFT JOIN {file_a} AS a
            ON a.{key_a} = b.{key_b}
    WHERE a.{key_a} IS NULL"""
    return query_merge


def cleanse_input(string):
    return contains_any(string, [' ', '(', ')'])


def contains_any(string, set):
    return True in [c in string for c in set]


def run_standalone():
    arg_parser = argparse.ArgumentParser(description='Merge two CSV files against an equivalent key column.')
    arg_parser.add_argument('-A', dest='file_in_a', required=True, help='file A to merge')
    arg_parser.add_argument('-B', dest='file_in_b', required=True, help='file B to merge')
    arg_parser.add_argument('--key-a', dest='key_a', required=True, help='key column to compare against in file A')
    arg_parser.add_argument('--key-b', dest='key_b', required=True, help='key column to compare against in file B')
    arg_parser.add_argument('-O', dest='file_out', nargs='?', type=argparse.FileType('w'),
                            default=workutil.gen_out_filename('mg'), help='output csv file')
    arg_parser.add_argument('-F', dest='field_statement',
                            help='statement of output fields with analogous fields separated by equal signs and '
                                 'non-analogous fields separated by commas')
    arg_parser.add_argument('-V', dest='verbose', action='store_true', help='print SQLite query')

    args = arg_parser.parse_args()

    if cleanse_input(args.file_in_a) or cleanse_input(args.file_in_b):
        raise Exception('Illegal character in filename')

    select_list = build_select_list(args.field_statement)
    query_merge = build_query(select_list, args.key_a, args.key_b, args.file_in_a, args.file_in_b)

    if args.verbose:
        print()
        print('Here is the SQL query: ')
        print()
        print(query_merge)
        print()

    default_input_params = q.QInputParams(skip_header=True, delimiter=',')
    q_engine = q.QTextAsData(default_input_params=default_input_params)

    q_output = q_engine.execute(query_merge)

    output_params = q.QOutputParams(delimiter=',', output_header=True)
    q_output_printer = q.QOutputPrinter(output_params)

    with args.file_out as outfile:
        q_output_printer.print_output(outfile, sys.stderr, q_output)
        print(f'All done! Merged output written to {args.file_out.name}')


if __name__ == '__main__':
    run_standalone()