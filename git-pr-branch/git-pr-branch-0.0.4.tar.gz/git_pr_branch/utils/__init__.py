def get_ellipsised(text, max_length):
    if len(text) <= max_length:
        return text
    return text[:max_length] + "…"
