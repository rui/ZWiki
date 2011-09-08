def strip2(src, start_token, end_token=None):
    """
    remove start_token and end_token from src

    >>> src = "blah=blahme;"
    >>> start_token = 'blah='
    >>> end_token = ';'
    >>>
    >>> assert "blahme" == strip_str(src, start_token, end_token)
    """
    STR_NOT_FOUND = -1
    
    pos = src.find(start_token)
    if pos == STR_NOT_FOUND:
        return src
    tmp = src[:pos]

    if end_token is not None:
        end = tmp.find(end_token)
        if end == STR_NOT_FOUND:
            return tmp
        return tmp[:end]
    return tmp
