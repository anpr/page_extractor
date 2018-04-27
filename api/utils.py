def dict_slice(d: dict, keys: set):
    """Slices a dict to only include the given keys and returns it. Cf https://stackoverflow.com/a/29216912/1214398

    Args:
        d - dictionary that should be sliced
        keys - set of keys that d should be limited to
    """
    return {key: d[key] for key in d.keys() & keys}
