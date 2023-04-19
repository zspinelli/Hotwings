# hotwings.
import common

# stdlib.
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from os.path import isfile, join, splitext
from requests import session
from sys import argv

# bs4.
from bs4 import BeautifulSoup


_CellInfo = namedtuple("CellInfo", ["href", "title", "ext", "date"])

_URL: str = "http://g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa/"
_TRY_MSG: str = "trying {}: {}"
_NO_CLOB_MSG: str = "skipping to avoid clobbering"

_session: session = session()
_session.proxies = {"http": "socks5h://localhost:9150", "https": "socks5h://localhost:9150"}

_parsed: Namespace | None = None
_user: str = ""
_stubs: list[str] = []


def _getCellInfo(p_cells) -> _CellInfo:
    name = p_cells[1].find("a")

    href: str = name["href"]
    title: str = name.text
    ext: str = splitext(href)[1]

    date: str = p_cells[2].text[:10]

    return _CellInfo(href, title, ext, date)


def _localExists(p_path) -> bool:
    if isfile(p_path):
        print(_NO_CLOB_MSG)
        return True

    return False


def _process():
    while _stubs:
        curr_stub: str = _stubs.pop(0)
        url: str = _URL + curr_stub

        posted_items = _session.get(url).text
        posted_items = BeautifulSoup(posted_items, "html.parser")
        posted_items = posted_items.find_all("tr")[3:-1]

        print(f"** now scraping: {curr_stub} **")
        #print(f"url: {url}")

        for item in posted_items:
            info = _getCellInfo(item.find_all("td"))
            print("found", info.title)
            link: str = f"{url}{info.href}"
            #print("link:", link)

            # some kind of file.
            if info.ext:
                full_dest: str = join(_parsed.o, "felthier", _user, info.title)

                # html.
                if info.ext == ".html" and (_parsed.json or _parsed.toml):
                    dest_no_ext = splitext(full_dest)[0].rstrip('.')

                    # title already exists locally.
                    if(
                        _parsed.json and isfile(dest_no_ext + ".json") or
                        _parsed.toml and isfile(dest_no_ext + ".toml")
                    ):
                        print(_NO_CLOB_MSG)
                        continue

                    print(_TRY_MSG.format("html", info.title))

                    desc = _session.get(link).text
                    desc = BeautifulSoup(desc, "html.parser")
                    desc = desc.find("pre").text.strip()

                    meta = {
                        "artist": _user,
                        "uploaded": info.date,
                        "description": desc
                    }

                    if _parsed.json:    common.writeJSON(dest_no_ext, meta)
                    elif _parsed.toml:  common.writeTOML(dest_no_ext, meta)

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

        print(f"** finished scraping: {curr_stub} **")


def _parseArgs():
    global _parsed

    parser: ArgumentParser = ArgumentParser()

    common.addCommonArgs(parser)

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
