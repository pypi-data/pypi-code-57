def get_nested_value_by_path(nested_dict, path, default=None, mode='mix'):
    """
    Get a nested value of nested dict by path
    :param nested_dict: nested dict object
        {
          "club": [
            {
              "manager": {
                "last_name": "Lionel",
                "first_name": "Messi"
              }
            }
          ]
        }
    :param path: path to access the nested dict value
        "club/0/manager/first_name"
    :param default: default value
    :param mode: ['json', 'list', 'mix']
    :return: value of dict
        "Messi"
    """
    current_nested_dict = nested_dict
    try:
        keys = path.split('/')
        for key in keys:
            if mode == 'json':
                current_nested_dict = current_nested_dict.get(key)
            elif mode == 'list':
                current_nested_dict = current_nested_dict[int(key)]
            elif mode == 'mix':
                try:
                    current_nested_dict = current_nested_dict[int(key)]
                except:
                    current_nested_dict = current_nested_dict.get(key)
    except Exception:
        current_nested_dict = default
    return current_nested_dict or default
