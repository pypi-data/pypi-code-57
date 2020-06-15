import base64


def convert_to_base64(entry):
    """Description:
        Converts a string to base64

    Args:
        entry (str): Text to convert to base64

    Example:
        Example usage:

            >>> b64_output = convert_to_base64('this is a test')
            >>> print(b64_output)
            dGhpcyBpcyBhIHRlc3Q=

    Returns:
        str"""

    entry_bytes = entry.encode('ascii')
    message_bytes = base64.b64encode(entry_bytes)
    encoded_entry = message_bytes.decode('ascii')

    return encoded_entry


def convert_from_base64(entry):
    """Description:
        Decodes a base64 string

    Args:
        entry (str): base64 text to decode

    Example:
        Example usage:

            >>> output = convert_from_base64('dGhpcyBpcyBhIHRlc3Q=')
            >>> print(output)
            this is a test

    Returns:
        str"""

    base64_bytes = entry.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    decoded_entry = message_bytes.decode('ascii')

    return decoded_entry


def base64_alphanumeric_only(entry):
    """Description:
        Converts a string to base64 but only keeps the alphanumeric characters

        Useful for when a deterministic, unique string is required. e.g An S3 bucket name.

    Args:
        entry (str): String to convert

    Example:
        Example usage:

            >>> output = base64_alphanumeric_only('this is a test')
            >>> print(output)
            dGhpcyBpcyBhIHRlc3Q

    Returns:
        str"""
    base64_chars = convert_to_base64(entry)
    alphanum_only = [char for char in base64_chars if char.isalpha() or char.isdigit()]
    joined_alphanum_only = ''.join(alphanum_only)

    return joined_alphanum_only
