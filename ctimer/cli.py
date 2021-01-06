"""Console script for ctimer."""
from ctimer import ctimer
import ctimer.ctimer_db as db
import sys
import argparse
from ctimer.visual import show_stats as ss
import logging
from ctimer import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        help="Shorten clock intervals for debugging purposes.",
        action="store_true",
    )
    parser.add_argument(
        "--stats",
        help="Show weekly stats of clock counts this week.",
        action="store_true",
    )
    parser.add_argument(
        "--overall", help="Show all clock counts across the years.", action="store_true"
    )
    parser.add_argument(
        "--hide",
        help="Display the timer always on top of other windows unless this statement is given",
        action="store_true",
    )
    parser.add_argument(
        "--silence",
        help="Silence Mode (visual hint instead of audio hint.",
        action="store_true",
    )
    parser.add_argument(
        "--db",
        type=utils.dir_path,
        help="The relative or absolute folder path to store and/or read db. When leave empty: look for previous location, otherwise create new at HOME/.ctimer",
        default=None,
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument(
        "--cus",
        action="store_true",
        help="give this argument if you want to customize length of clocks/breaks, and aim clock count. You will enter a commandline interface.",
    )
    args = parser.parse_args()
    # cache
    db_path = utils.get_cache_filepath(args.db, debug=args.debug)
    logging.info(f"{db_path} is where the db stored in.")

    if args.debug:
        db_file = f"{db_path}/ctimer_debug.db"
        db.create_connection(db_file)  # create if not exist
    else:
        db_file = f"{db_path}/ctimer.db"
        db.create_connection(db_file)  # create if not exist

    if args.overall:
        events = db.get_yearly_stats(db_file)
        ss.plot_calmap(events=events)
    elif args.stats:
        ss.plot_timetable(path=db_file, outpath=f"./")
    else:
        if args.cus:
            cus_meta = utils.ask_customized()
            ctimer.maintk(
                db_file,
                hide=args.hide,
                debug=args.debug,
                silence=args.silence,
                meta=cus_meta,
            )
        else:
            ctimer.maintk(
                db_file, hide=args.hide, debug=args.debug, silence=args.silence
            )


if __name__ == "__main__":
    sys.exit(main())
