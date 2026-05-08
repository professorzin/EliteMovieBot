import re

def clean_filename(name):

    if not name:
        return "Unknown File"

    name = re.sub(r'\[.*?\]', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r'[^a-zA-Z0-9\s]', ' ', name)
    name = re.sub(r'\s+', ' ', name)

    return name.strip().title()
