import csv


def csv_to_dict(primary_key, input_file_path):
    """Description:
        Reads CSV file and turns it into a dictionary

    Args:
        primary_key (str): Becomes the `key` of each dictionary entry
        input_file_path (str): Input file path

    Example:
        Example CSV file:

            Id,Email
            1,john@example.com
            2,jane@example.com

        Example usage:

            >>> from onnmisc.transformers.csv import csv_to_dict
            >>> from pprint import pprint
            >>>
            >>> output = csv_to_dict('accounts.csv')
            >>> print(output)
            {'1': {'Email': 'john@example.com'}, '2': {'Email': 'jane@example.com'}}

    Returns:
        list
    """
    output = {}

    dict_reader = csv.DictReader(open(input_file_path))
    for row in dict_reader:
        primary_value = row.pop(primary_key)

        output[primary_value] = {}

        for row_key, row_value in row.items():
            output[primary_value][row_key] = row_value

    return output


def csv_to_list(input_file_path):
    """Description:
        Reads CSV file and turns it into a list

    Args:
        input_file_path (str): Input file path

    Example:
        Example CSV file:

            Id,Email
            1,john@example.com
            2,jane@example.com

        Example usage:

            >>> from onnmisc.transformers.csv import csv_to_list
            >>> from pprint import pprint
            >>>
            >>> output = csv_to_list('accounts.csv')
            >>> pprint(output)
            [{'Email': 'john@example.com', 'Id': '1'},
            {'Email': 'jane@example.com', 'Id': '2'}]

    Returns:
        list
    """
    output = []
    dict_reader = csv.DictReader(open(input_file_path))

    for row in dict_reader:
        csv_dict = {}

        for key, value in row.items():
            csv_dict[key] = value

        output.append(csv_dict)

    return output
