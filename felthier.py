# hotwings.
import common

# stdlib.
from datetime import datetime
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from os.path import isfile, join, splitext, basename
from sys import argv

# scraping.
from bs4 import BeautifulSoup
from requests import session


_CellInfo = namedtuple("CellInfo", ["href", "title", "ext", "date"])

_URL: str = "http://g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa/"
_TRY_MSG: str = "trying {}: {}"
_NO_CLOB_MSG: str = "skipping for avoid clobbering"

_session: session = session()
_session.proxies = {"http": "socks5h://localhost:9150", "https": "socks5h://localhost:9150"}

_parsed: Namespace | None = None
_user: str = ""
_stubs: list[str] = []


def sanitizeName(p_name: str) -> str:
    new_name = p_name
    bad_chars = ['\x03']

    for c in p_name:
        if c in bad_chars:
            ho = hex(ord(c))
            ci = chr(int(ho, 16) + 0x2662)
            new_name = new_name.replace(c, ci)

    return new_name


def _getCellInfo(p_cells) -> _CellInfo:
    anchor = p_cells[1].find("a")

    href: str = anchor["href"]
    title: str = sanitizeName(anchor.text)
    ext: str = splitext(href)[1]
    date: str = p_cells[2].text[:10]

    return _CellInfo(href, title, ext, date)


def _localExists(p_path) -> bool:
    if isfile(p_path):
        print(_NO_CLOB_MSG)
        return True

    return False


def _process():
    dest_base: str = join(_parsed.o, "felthier", _user)

    resume_file: str = ""
    resume: datetime | None = None
    timestamps: dict = {}

    # ---- read resume text. ---- #

    if hasattr(_parsed, "sdr"):
        resume_file = join(dest_base, "date-resume.txt")

        if isfile(resume_file):
            with open(resume_file, "r") as read_date:
                resume = datetime.strptime(read_date.readline(), "%Y-%m-%d")

    # ---- start scraping. ---- #

    while _stubs:
        curr_stub: str = _stubs.pop(0)
        url: str = _URL + curr_stub

        posted_soup = BeautifulSoup(_session.get(url).text, "html.parser")
        posted_items = posted_soup.find_all("tr")[3:-1]

        print(f"\n** now scraping: {curr_stub} **")
        #print(f"url: {url}")

        for item in posted_items:
            info = _getCellInfo(item.find_all("td"))
            print("\nfound", info.title)

            # ---- check resume factors. ---- #

            # date resume, item date earlier than last run.
            if _parsed.sdr and resume and datetime.strptime(info.date, "%Y-%m-%d") <= resume:
                print("skipping for resume date")
                continue

            # ---- proceed with scraping. ---- #

            link: str = f"{url}{info.href}"
            #print("link:", link)

            # some kind of file.
            if info.ext:
                full_dest: str = join(dest_base, info.title)

                # html.
                if info.ext == ".html":
                    # metadata wanted.
                    if _parsed.json or _parsed.toml or _parsed.fibr:
                        dest_no_ext = splitext(full_dest)[0].rstrip('.')

                        desc = _session.get(link).text
                        desc = BeautifulSoup(desc, "html.parser")
                        desc = desc.find("pre").text.strip()

                        # ---- special metadata. ---- #

                        if _parsed.fibr and not _localExists(dest_no_ext + ".fibr"):
                            print(_TRY_MSG.format("html", info.title))

                            title: str = basename(dest_no_ext)

                            def _titleSplit(p_sep: str) -> str:
                                parts: list[str] = title.split(p_sep, 1)

                                if len(parts) > 1:  return parts[1]
                                else:               return parts[0]

                            title = _titleSplit('.')
                            title = _titleSplit(_user + "_")
                            title = splitext(title)[0]

                            tags: list[str] = []
                            tags.append("author:" + _user)
                            tags.append("published:" + info.date[:4])

                            extra: dict = {}
                            extra.update({"full_published": info.date})

                            common.writeFIBR(dest_no_ext, title, tags, desc, extra)

                        # ---- generic metadata. ---- #

                        if _parsed.json or _parsed.toml:
                            meta = {
                                "artist": _user,
                                "uploaded": info.date,
                                "description": desc
                            }

                            if _parsed.json and not _localExists(dest_no_ext + ".json"):
                                print(_TRY_MSG.format("html", info.title))
                                common.writeJSON(dest_no_ext, meta)

                            if _parsed.toml and not _localExists(dest_no_ext + ".toml"):
                                print(_TRY_MSG.format("html", info.title))
                                common.writeTOML(dest_no_ext, meta)

                # unknown type.
                elif info.ext == "." and 'u' in _parsed.pt:
                    full_dest = full_dest[:-1]

                    if _localExists(full_dest): continue
                    print(_TRY_MSG.format("unknown", info.title))

                    unknown = _session.get(link, stream=True)
                    common.writePayload(full_dest, unknown.content)

                # flash.
                elif 'f' in _parsed.pt and info.ext == ".swf":
                    if _localExists(full_dest): continue
                    print(_TRY_MSG.format("flash", info.title))

                    flash = _session.get(link, stream=True)
                    common.writePayload(full_dest, flash.content)

                # image.
                elif 'i' in _parsed.pt and info.ext in [".png", ".jpg", ".jpeg", ".gif"]:
                    if _localExists(full_dest): continue
                    print(_TRY_MSG.format("image", info.title))

                    image = _session.get(link, stream=True)
                    common.writePayload(full_dest, image.content)

                # audio.
                elif 'a' in _parsed.pt and info.ext in [".mp3", ".ogg", ".flac"]:
                    if _localExists(full_dest): continue
                    print(_TRY_MSG.format("audio", info.title))

                    audio = _session.get(link, stream=True)
                    common.writePayload(full_dest, audio.content)

                # writing.
                elif 'w' in _parsed.pt and info.ext in [".txt", ".docx", ".odt", ".pdf"]:
                    if _localExists(full_dest): continue
                    print(_TRY_MSG.format("writing", info.title))

                    writing = _session.get(link, stream=True)
                    common.writePayload(full_dest, writing.content)

            # subdir.
            else:
                subdir: str = f"{curr_stub}{info.href}"
                print(f"scheduled subdir: {subdir:}")
                _stubs.append(subdir)

        print(f"\n** finished scraping: {curr_stub} **")

    # ---- write resume text. ---- #

    if hasattr(_parsed, "sdr"):
        with open(resume_file, "w") as store_date:
            store_date.write(datetime.today().strftime('%Y-%m-%d'))
            print(f"** wrote resume info: {resume_file} **")


def _parseArgs():
    global _parsed

    parser: ArgumentParser = ArgumentParser()

    common.addCommonArgs(parser)
    common.addMetaArgs(parser)
    common.addResumeArgs(parser)

    parser.add_argument("-pt", action="store", type=str, default= "", help="combo of: i, w, a, f, u")
    parser.add_argument("names", nargs="+", help="space-separated sequence of usernames")

    _parsed = parser.parse_args()
    print(f"input: {_parsed}")


if __name__ == "__main__":
    argv = argv[1:]

    _parseArgs()

    for name in _parsed.names:
        _user = name
        _stubs.append(f"{name}/")
        _process()
