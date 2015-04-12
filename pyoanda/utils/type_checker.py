def type_checker(item, checker):
    """Type and range checker

        Given field name, check type and value's range
        e.g.
        inputs:
        item = {"x": 1, "y": None}
        checker = {
            "x": (int, range(1, 10)),
            "y" : (None,)
        }
    """
    assert isinstance(checker, dict)
    assert isinstance(item, dict)
    errors = []
    for field, check in checker.items():
        if field not in item:
            msg = "'{}' field is not present".format(field)
            errors.append(msg)
            continue
        value = item.get(field)
        typo = check[0] if isinstance(check[0], tuple) else (check[0],)
        rang = check[1] if len(check) > 1 else None

        if None in typo and value is None:
            continue

        elif not isinstance(value, typo):
            msg = "Field '{}'  is not {} type".format(field, typo)
            errors.append(msg)
            continue

        if rang and value not in rang:
            msg = "Field '{}'  is not in {} range".format(field, rang)
            errors.append(msg)
            continue
    # Check field existence
    for field in item:
        if field not in checker:
            msg = "Field '{}' is not in checker".format(field, rang)
            errors.append(msg)
    if errors:
        raise TypeError(errors)
