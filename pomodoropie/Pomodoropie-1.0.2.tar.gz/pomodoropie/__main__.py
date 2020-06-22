import argparse
import subprocess

from . import session


def main():
    # parse arguments - length of work sessions, length of short breaks, length of long break
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--work", "-w", type=int, help="Length of work segment", default=25
    )
    parser.add_argument(
        "--short", "-s", type=int, help="Length of short break", default=5
    )
    parser.add_argument(
        "--long", "-l", type=int, help="Length of long break", default=15
    )

    args = parser.parse_args()

    # create segments
    work_segs = [session.Segment(args.work, "work")] * 4
    short_breaks = [session.Segment(args.short, "short")] * 3
    long_break = session.Segment(args.long, "long")

    segments = [
        work_segs[0],
        short_breaks[0],
        work_segs[1],
        short_breaks[1],
        work_segs[2],
        short_breaks[2],
        work_segs[3],
        long_break,
    ]

    newsession = session.Session(segments)

    print(f"Start working! {args.work} minute(s) remaining.")
    newsession.start()

    while newsession.next_segment():
        if newsession.segment_type() == "work":
            proc = subprocess.run(
                [
                    "zenity",
                    "--info",
                    "--text",
                    f"Start working - {args.work} minute(s) remaining.",
                ]
            )
        elif newsession.segment_type() == "short":
            proc = subprocess.run(
                [
                    "zenity",
                    "--info",
                    "--text",
                    f"Take a short break - {args.short} minute(s) remaining.",
                ]
            )
        else:
            proc = subprocess.run(
                [
                    "zenity",
                    "--info",
                    "--text",
                    f"Take a long break - {args.long} minute(s) remaining.",
                ]
            )

    print("That's the end of this session. Rerun to start a new session.")
    newsession.stop()


if __name__ == "__main__":
    main()
