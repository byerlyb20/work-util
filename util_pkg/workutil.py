import datetime

def gen_out_filename(util_name):
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    out_file_name = f'../out/{util_name}_{datetime.datetime.now().isoformat("_", "seconds")}.csv'
    return out_file_name
