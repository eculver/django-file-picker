"""
Parsing of various strings used as input
"""

import mimetypes

def parse_types(path):
    (mime_type, encoding) = mimetypes.guess_type(path)
    try:
        return mime_type.split('/')
    except:
        return ['text', 'plain']

def parse_options(s):
    """
    Expects a string in the form "key=val:key2=val2" and returns a
    dictionary.
    """
    options = {}
    for option in s.split(':'):
        if '=' in option:
            key, val = option.split('=')
            options[str(key).strip()] = val.strip()
    return options
