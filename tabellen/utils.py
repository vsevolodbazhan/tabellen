from typing import Optional


def read_between(value: str, prefix: str, postfix: str) -> Optional[str]:
    """Read a sequence between given prefix and postfix.

    Args:
        value (str): A value to read a sequence from.
        prefix (str): A prefix after which a sequence starts.
        postfix (str): A postfix before which a sequence ends.

    Returns:
        str: The sequence.
        None: If prefix or postfix were not found.

    Examples:
        >>> read_between(value='abc', prefix='a', postfix='c')
        'b'
        >>> read_between(value='abc', prefix='a', postfix='d')
        >>> read_between(value='abc', prefix='z', postfix='c')
    """

    start = value.find(prefix)
    if start == -1:
        return None
    start += len(prefix)

    end = value.find(postfix)
    if end == -1:
        return None

    return value[start:end]
