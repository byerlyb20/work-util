import datetime
from pathlib import Path

def gen_out_filename(util_name):
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    Path("../out").mkdir(parents=True, exist_ok=True)
    out_file_name = f'../out/{util_name}_{timestamp}.csv'
    return out_file_name
