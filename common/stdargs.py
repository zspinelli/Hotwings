# stdlib.
from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from os import path


MSG_NO_CLOBBER: str = "skipping for avoid clobbering\n"
MSG_TRY: str = "trying {}: {}\n"


_need_meta: bool = False
_need_date_cutoff: bool = False
_need_date_resume: bool = False

_lower_limit: datetime | None = None
_upper_limit: datetime | None = None


def needMeta() -> bool:         return _need_meta
def needDateCutoff() -> bool:   return _need_date_cutoff
def needDateResume() -> bool:   return _need_date_resume


# ==================================================================================================== #
# standard arguments.


def addOutputArgs(p_parser: ArgumentParser):
    output_group = p_parser.add_argument_group("output")

    output_group.add_argument(
        "-os", "-output-structured",
        help="output path (structured). builds an organized folder tree in the directory if applicable."
    )

    output_group.add_argument(
        "-ou", "-output-unstructured",
        help="output path (unstructured). dumps everything into the directory."
    )


def addMetaArgs(p_parser: ArgumentParser):
    meta_group = p_parser.add_argument_group("metadata")

    meta_group.add_argument("--json", action="store_true", help="grab description/metadata as json")
    meta_group.add_argument("--toml", action="store_true", help="grab description/metadata as toml")
    meta_group.add_argument("--fibr", action="store_true", help="grab description/metadata for filebrary")


def addDateCutoffArgs(p_parser: ArgumentParser):
    date_cutoff_group = p_parser.add_argument_group("date cutoff")

    date_cutoff_group.add_argument(
        "-dcb", "-date-cutoff-before",
        type=lambda d: datetime.strptime(d, "%Y-%m-%d"),
        help="ignore posts before a YYYY-MM-DD date"
    )

    date_cutoff_group.add_argument(
        "-dca", "-date-cutoff-after",
        type=lambda d: datetime.strptime(d, "%Y-%m-%d"),
        help="ignore posts after a YYYY-MM-DD date"
    )

    date_cutoff_group.add_argument(
        "-dcbi", "-date-cutoff-before-incl",
        type=lambda d: datetime.strptime(d, "%Y-%m-%d"),
        help="ignore posts before or on a YYYY-MM-DD date"
    )

    date_cutoff_group.add_argument(
        "-dcai", "-date-cutoff-after-incl",
        type=lambda d: datetime.strptime(d, "%Y-%m-%d"),
        help="ignore posts after or on a YYYY-MM-DD date"
    )


def addDateResumeArgs(p_parser: ArgumentParser):
    resume_group = p_parser.add_argument_group("resume")

    resume_group.add_argument(
        "--lrr", "--last-run-resume",
        action="store_true",
        help="store last run date for resume"
    )


# ==================================================================================================== #
# helper functions.


def outsideDateCutoffLimits(p_date: datetime) -> bool:
    outside: bool = False

    if _lower_limit and p_date < _lower_limit: outside = True
    if _upper_limit and p_date > _upper_limit: outside = True

    return outside


def readDateResume(p_filepath: str) -> datetime | None:
    if path.isfile(p_filepath):
        with open(p_filepath, "r") as file:
            return datetime.strptime(file.readline(), "%Y-%m-%d")

    return None


def writeDateResume(p_filepath: str):
    with open(p_filepath, "w") as file:
        file.write(datetime.today().strftime("%Y-%m-%d"))
        print(f"** WROTE RESUME INFO: {p_filepath} **")


# ==================================================================================================== #
# helper analysis.


def analyze(p_parsed: Namespace):
    global _need_meta, _need_date_cutoff, _lower_limit, _upper_limit

    # ---- output. ---- #

    if p_parsed.os and p_parsed.ou:
        print("Output path conflict: -P_ and -ou cannot be used simultaneously.")
        exit()

    # ---- meta. ---- #

    if p_parsed.json or p_parsed.toml or p_parsed.fibr:
        _need_meta = True

    # ---- date cutoff. ---- #

    if(
        p_parsed.dcb or
        p_parsed.dcbi or
        p_parsed.dca or
        p_parsed.dcai
    ):
        _need_date_cutoff = True

        # ---- incompatible limits. ---- #

        if p_parsed.dcb and p_parsed.dcbi:
            print("Date cutoff conflict: -date-cutoff-before and -date-cutoff-before-incl cannot be used simultaneously.")
            exit()

        if p_parsed.dca and p_parsed.dcai:
            print("Date cutoff conflict: -date-cutoff-after and -date-cutoff-after-incl cannot be used simultaneously.")
            exit()

        # ---- lower limit. ---- #

        if p_parsed.dcb:
            _upper_limit = datetime.strptime(p_parsed.dcb, "%Y-%m-%d")

        elif p_parsed.dcbi:
            _upper_limit = datetime.strptime(p_parsed.dcbi, "%Y-%m-%d") + timedelta(days=1)

        # ---- upper limit. ---- #

        if p_parsed.dca:
            _lower_limit = datetime.strptime(p_parsed.dca, "%Y-%m-%d")

        elif p_parsed.dcai:
            _lower_limit = datetime.strptime(p_parsed.dcai, "%Y-%m-%d") - timedelta(days=1)
