import datetime


def gen_out_filename(util_name, extension='.csv'):
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    return f'{util_name}_{timestamp}{extension}'
