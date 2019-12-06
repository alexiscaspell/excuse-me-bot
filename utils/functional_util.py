import inspect


def _get_value(elem, key):
    if callable(key):
        return key(elem)
    if not elem:
        return elem
    elif isinstance(elem, list):
        return _get_value(elem[0], key) if len(elem) > 0 else None
    elif isinstance(elem, dict):
        return elem.get(key, None)
    else:
        return getattr(elem, key)


def implicit(**implicit_args):
    def decorator(function):
        def wrapper(*args, **kwargs):

            for k in kwargs:
                if k in implicit_args:
                    o = kwargs[k]
                    for true_arg in implicit_args[k]:
                        kwargs.update({true_arg: _get_value(
                            o, implicit_args[k][true_arg])})
                    del kwargs[k]

            n_args = []

            if len(args) > 0:
                for i, a in enumerate(inspect.getfullargspec(function).args):
                    if a not in kwargs and i < len(args):
                        n_args.append(list(args)[i])

            return function(*n_args, **kwargs)
        return wrapper
    return decorator
