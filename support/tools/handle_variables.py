from Schema import IDInput
from collections import Iterable


def return_id_input(ids):
    if isinstance(ids, Iterable) and not isinstance(ids, str):
        return [IDInput(id=i) for i in ids]
    else:
        return IDInput(id=ids)
