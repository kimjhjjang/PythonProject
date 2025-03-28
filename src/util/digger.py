import re
import json
import logging


def parse_dict_key(expression, delimiter='.', escape_char='\\'):
    """
    Parses a string-based dictionary key expression, splitting by a delimiter
    while respecting escaped delimiters.

    Args:
        expression (str): The key expression to parse.
        delimiter (str): The delimiter to split by. Defaults to '.'.
        escape_char (str): The escape character used to escape the delimiter. Defaults to '\\'.

    Returns:
        list: A list of parsed keys.
    """
    # Create a regex pattern to split by unescaped delimiters
    pattern = rf'(?<!{re.escape(escape_char)}){re.escape(delimiter)}'

    # Split the string using the pattern
    parts = re.split(pattern, expression)

    # Replace escaped delimiters with the actual delimiter
    parsed_keys = [part.replace(f'{escape_char}{delimiter}', delimiter) for part in parts]

    return parsed_keys


def get_nested_value(d, expr):

    if d is None:
        return None

    """
    Retrieves a nested value from a dictionary using a complex key expression.

    Args:
        d (dict): The dictionary to search.
        key_expression (str): The complex key expression.

    Returns:
        Any: The value from the dictionary, or None if the key path is invalid.
    """
    keys = parse_dict_key(expr)

    current = d
    try:
        for key in keys:
            if key.startswith('[') and key.endswith(']'):
                index = int(key[1:-1])  # Extract the index
                current = current[index]
            else:
                current = current[key]
    except (KeyError, IndexError, TypeError):
        return None
    return current


def is_list_like(ds):
    if isinstance(ds, list) or isinstance(ds, tuple):
        return True
    return False


def dict_filter(d, k, v):
    if isinstance(d, dict):
        if k in d and d[k] == v:
            return True
    return False


def decode_bytes(data):
    """
    Recursively decodes byte strings into appropriate Python types.

    Args:
        data: Data to decode. Can be bytes, list, dict, or other types.

    Returns:
        Decoded data with all byte strings converted to appropriate types.
    """
    if isinstance(data, bytes):
        # Convert bytes to a UTF-8 string
        d = data.decode('utf-8')
        return decode_bytes(d)
    elif isinstance(data, dict):
        # Recursively decode keys and values in dictionaries
        return {decode_bytes(key): decode_bytes(value) for key, value in data.items()}
    elif isinstance(data, list):
        # Recursively decode items in lists
        return [decode_bytes(item) for item in data]
    elif isinstance(data, str):
        # Try parsing as JSON if possible
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return data
    else:
        # Leave other data types unchanged
        return data


# chaining
# user_yn == 'Y' and del_yn == 'N' and dist_ch_type == 'KKO' and ch_supply_code == 'LGCNS'

# querying
# group_id = helper.find('commonLst.[1]').equal('fieldId', 'mPushConnInfo').get('fieldValue.groupId')

# key
# commonLst.[1].a\.b\.c

class Digger(object):

    inner_ds = None

    def init(self, d):

        if isinstance(d, dict):
            self.inner_ds = d


    def __init__(self, d):
        self.init(d)


    def __str__(self):

        if self.inner_ds is None:
            return 'self.inner_dict is None'

        return str(self.inner_ds)


    def dig(self, expr):
        self.inner_ds = get_nested_value(self.inner_ds, expr)
        return self


    # if k == v
    def filter(self, key, value):

        # key == value
        found = None
        if isinstance(self.inner_ds, dict):
            found = {}
            for k, v in self.inner_ds.items():
                if dict_filter(v, key, value):
                    found[k] = v
        elif is_list_like(self.inner_ds):
            found = []
            for d in self.inner_ds:
                if dict_filter(d, key, value):
                    found.append(d)

        self.inner_ds = found
        return self


    def get(self, k):

        if self.inner_ds is None:
            return None

        if isinstance(self.inner_ds, dict):
            if k in self.inner_ds:
                return self.inner_ds[k]
        elif is_list_like(self.inner_ds):
            for d in self.inner_ds:
                if isinstance(d, dict):
                    if k in d:
                        return d[k]
        return None


    def nth(self, index = 0):

        flats = []
        if isinstance(self.inner_ds, dict):
            for k, v in self.inner_ds.items():
                flats.append(v)
        elif is_list_like(self.inner_ds):
            flats.extend(self.inner_ds)

        if len(flats) > index:
            self.inner_ds = flats[index]

        return self


    def print(self):
        logging.info(self.inner_ds)
        return self

