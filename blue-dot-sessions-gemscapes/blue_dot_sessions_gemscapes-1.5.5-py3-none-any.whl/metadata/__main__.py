import argparse

from . import get_blue_dot_sessions_metadata


def create_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description="Get Blue Dot Sessions meta data for a track")
    parser.add_argument("file_paths", metavar="file-paths", type=str, nargs="+",
                        help="Files from which to get metadata")

    return parser


def main():
    parsed = create_parser().parse_args()

    for file_path in parsed.file_paths:
        metadata = get_blue_dot_sessions_metadata(file_path)
        if metadata is None:
            print(f"{file_path} has no metadata")
            continue
        metadata_str = "\n".join([f"{key}: {metadata[key]}" for key in metadata])
        print(f"Metadata for {file_path}\n{metadata_str}")

main()
