def type_checker(item, checker):
    errors = []
    for field, check in checker.items():
        if field not in item:
            msg = "'{}' field is not present".format(field)
            errors.append(msg)
            continue
        value = item.get(field)
        typo, rang = check if isinstance(check, tuple) and len(check) > 1 else (check, 1)
        if not isinstance(value, typo):
            msg = "Field '{}'  is not {} type".format(field, typo)
            errors.append(msg)
            continue

        if rang and value not in rang:
            msg = "Field '{}'  is not in {} range".format(field, rang)
            errors.append(msg)
            continue

    for field in item:
        if field not in checker:
            msg = "Field '{}' is not in checker".format(field, rang)
            errors.append(msg)

    if errors:
        raise TypeError(errors)
