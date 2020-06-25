"""
    Package responsible to get transparent all files independent of its extensions.
"""

__all__ = ['file', 'tools', 'get_file', 'SUPPORTED_EXTENSIONS', 'ExtensionNotSupported']


from matchup.presentation.formats.file import Txt, Pdf, get_extension


SUPPORTED_EXTENSIONS = ['', '.txt', '.pdf']


class ExtensionNotSupported(RuntimeError):
    ...


def get_file(file_path: str):
    extension = get_extension(file_path)

    if extension not in SUPPORTED_EXTENSIONS:
        raise ExtensionNotSupported(f"{extension} is not supported.")

    if extension == '.txt' or not extension:
        return Txt(file_path)
    elif extension == '.pdf':
        return Pdf(file_path)
