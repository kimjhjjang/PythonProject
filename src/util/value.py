
def get_value(d, key):

    keys = key.split(".")

    found = True
    for k in keys:
        if d is None:
            return None

        if k in d:
            d = d[k]
        else:
            found = False
            break

    if not found:
        return None
    return d


class DictHelper(object):

    def __init__(self, d):
        if isinstance(d, dict):
            self.d = d
            return
        raise ValueError("D is not dict")


    def __str__(self):
        return str(self.d)


    def get(self, key):
        return get_value(self.d, key)


