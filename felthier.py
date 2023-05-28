# hotwings.
from common import stdargs, record, tor

# stdlib.
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from datetime import datetime
from os import path
from sys import argv

# scraping.
from bs4 import BeautifulSoup, ResultSet
from requests import session


_CellInfo = namedtuple("CellInfo", ["href", "title", "ext", "date"])


_ROOT: str = "http://g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa/{}"


_session: session = session()
_session.proxies = {"http": "socks5h://localhost:9150", "https": "socks5h://localhost:9150"}


_parsed: Namespace = Namespace()
_dest_dir: str = ""
_resume: datetime | None = None
_subdirs: list = []
_link: str = ""
_out_filepath: str = ""


def _writePayload():
    payload = _session.get(_link, stream=True)
    record.writeBinary(_out_filepath, payload.content)


def _sanitizeName(p_name: str) -> str:
    new_name = p_name
    bad_chars = ['\x03']

    for c in p_name:
        if c in bad_chars:
            ho = hex(ord(c))
            ci = chr(int(ho, 16) + 0x2662)
            new_name = new_name.replace(c, ci)

    return new_name


def _splitTitle(p_name: str, p_sep: str) -> str:
    parts = p_name.split(p_sep, 1)
    return parts[1] if len(parts) > 1 else parts[0]


def _getCellInfo(p_cells) -> _CellInfo:
    anchor = p_cells[1].find("a")

    href: str = anchor["href"]
    title: str = _sanitizeName(anchor.text)
    ext: str = path.splitext(href)[1]
    date: str = p_cells[2].text[:10]

    return _CellInfo(href, title, ext, date)


def _parseArgs():
    global _parsed

    parser: ArgumentParser = ArgumentParser()

    # ---- common args. ---- #

    stdargs.addOutputArgs(parser)
    stdargs.addMetaArgs(parser)
    stdargs.addDateCutoffArgs(parser)
    stdargs.addDateResumeArgs(parser)

    # ---- felthier args. ---- #

    felthier_group = parser.add_argument_group("felthier")
    felthier_group.add_argument("-pt", type=str, default="", help="combo of: i, w, a, f, u")
    felthier_group.add_argument("names", nargs="+", help="space-separated sequence of usernames")

    # ---- start parsing. ---- #

    _parsed = parser.parse_args()
    print(f"input: {_parsed}\n")


def _process():
    global _out_filepath, _link

    subdir: str = _subdirs.pop(0)
    url: str = _ROOT.format(subdir)
    print(f"** NOW ENTERING: {url} **\n")

    posts_soup: BeautifulSoup = BeautifulSoup(_session.get(url).text, "html.parser")
    posts: ResultSet = posts_soup.find_all("tr")[3:-1]

    for item in posts:
        info: _CellInfo = _getCellInfo(item.find_all("td"))
        _link = url + info.href
        # print("link:", _link)

        # file.
        if info.ext:
            print(f"found file: {info.title}")
            _out_filepath = path.join(_dest_dir, info.title)

            # last run resume.
            if(
                stdargs.needDateResume() and
                datetime.strptime(info.date, "%Y-%m-%d") <= _resume
            ):
                print("skipping for resume date\n")
                continue

            # date cutoff.
            if(
                stdargs.needDateCutoff() and
                stdargs.outsideDateCutoffLimits(info.date)
            ):
                print("skipping for date cutoff\n")
                continue

            # html.
            if info.ext == ".html":
                # metadata wanted.
                if stdargs.needMeta():
                    out_filepath_no_ext: str = path.splitext(_out_filepath)[0].rstrip('.')
                    desc: str = BeautifulSoup(_session.get(_link).text, "html.parser").find("pre").text.strip()

                    if _parsed.fibr:
                        if path.isfile(out_filepath_no_ext + ".fibr"):
                            print(stdargs.MSG_NO_CLOBBER)
                            continue

                        print(stdargs.MSG_TRY.format("html", info.title))

                        title: str = path.basename(out_filepath_no_ext)
                        title = _splitTitle(title, '.')
                        title = _splitTitle(title, '_')
                        title = path.splitext(title)[0]

                        tags: list = []
                        tags.append("author:" + name)
                        tags.append("published:" + info.date[:4])

                        extra: dict = {}
                        extra.update({"full_published": info.date})

                        record.writeFIBR(out_filepath_no_ext, title, tags, desc, extra)

                    if _parsed.json:
                        if path.isfile(out_filepath_no_ext + ".json"):
                            print(stdargs.MSG_NO_CLOBBER)
                            continue

                        meta: dict = {
                            "artist": name,
                            "uploaded": info.date,
                            "description": desc
                        }

                        print(stdargs.MSG_TRY.format("html", info.title))
                        record.writeJSON(out_filepath_no_ext, meta)

                    if _parsed.toml:
                        if path.isfile(out_filepath_no_ext + ".toml"):
                            print(stdargs.MSG_NO_CLOBBER)
                            continue

                        meta: dict = {
                            "artist": name,
                            "uploaded": info.date,
                            "description": desc
                        }

                        print(stdargs.MSG_TRY.format("html", info.title))
                        record.writeTOML(out_filepath_no_ext, meta)

            # unknown.
            elif info.ext == "." and 'u' in _parsed.pt:
                _out_filepath = _out_filepath[:-1]

                if path.isfile(_out_filepath):
                    print(stdargs.MSG_NO_CLOBBER)
                    continue

                print(stdargs.MSG_TRY.format("unknown", info.title))
                _writePayload()

            # flash.
            elif info.ext == ".sfw" and 'f' in _parsed.pt:
                if path.isfile(_out_filepath):
                    print(stdargs.MSG_NO_CLOBBER)
                    continue

                print(stdargs.MSG_TRY.format("flash", info.title))
                _writePayload()

            # image.
            elif info.ext in [".png", ".jpg", ".jpeg", ".gif"] and 'i' in _parsed.pt:
                if path.isfile(_out_filepath):
                    print(stdargs.MSG_NO_CLOBBER)
                    continue

                print(stdargs.MSG_TRY.format("image", info.title))
                _writePayload()

            # audio.
            elif info.ext in [".mp3", ".ogg", ".flac"] and 'a' in _parsed.pt:
                if path.isfile(_out_filepath):
                    print(stdargs.MSG_NO_CLOBBER)
                    continue

                print(stdargs.MSG_TRY.format("audio", info.title))
                _writePayload()

            # writing.
            elif info.ext in [".txt", ".docx", ".odt", ".pdf"] and 'w' in _parsed.pt:
                if path.isfile(_out_filepath):
                    print(stdargs.MSG_NO_CLOBBER)
                    continue

                print(stdargs.MSG_TRY.format("writing", info.title))
                _writePayload()

        # subdir.
        else:
            print(f"found subdir: {info.title}\n")
            new_subdir: str = f"{subdir}{info.href}"
            _subdirs.append(new_subdir)


if __name__ == "__main__":
    argv = argv[1:]

    _parseArgs()
    stdargs.analyze(_parsed)

    if _parsed.ou:
        _dest_dir = _parsed.ou

    if tor.start():
        print() # note: space between tor init and scraper output.

        for name in _parsed.names:
            if _parsed.os:
                _dest_dir = path.join(_parsed.os, "felthier", name)

            resume_file: str = path.join(_dest_dir, f"{name}-date-resume.txt")

            # ---- read resume file? ---- #

            if stdargs.needDateResume():
                _resume = stdargs.readDateResume(resume_file)

            # ---- scrape. ---- #

            print(f"** STARTED SCRAPING: {name} **\n")

            _subdirs.append(name + '/')

            while _subdirs:
                _process()

            print(f"** FINISHED SCRAPING: {name} **\n")

            # ---- write resume file? ---- #

            if stdargs.needDateResume():
                stdargs.writeDateResume(resume_file)

        tor.stop()
