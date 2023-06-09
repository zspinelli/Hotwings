# stdlib.
import re
from atexit import register
from os import environ, path
from platform import system as plat_sys
from subprocess import Popen

# tor.
from stem import process


_os: str = plat_sys().lower()


_BASE_PATH: dict = {
    "windows": path.join(environ["USERPROFILE"], "Desktop", "Tor Browser", "Browser", "TorBrowser")
    # "linux": path.join()
    # "darwin": path.join()
}


_TOR_PATH: dict = {
    "windows": path.join(_BASE_PATH[_os], "Tor", "tor.exe")
    # "linux": path.join()
    # "darwin": path.join()
}


_tor_proc: Popen | None = None


def start() -> bool:
    global _tor_proc

    try: # tor_ex
        print(f"base:\t{_BASE_PATH[_os]}")
        print(f"tor:\t{_TOR_PATH[_os]}\n")

        print("tor.py starting tor...")
        _tor_proc = process.launch_tor_with_config(
            config={"SocksPort": "9150"},
            init_msg_handler=lambda line: print(line) if re.search("Bootstrapped", line) else False,
            tor_cmd=_TOR_PATH[_os]
        )

        return True

    except Exception as tor_ex:
        print("tor_ex:", tor_ex)
        return False


def stop():
    global _tor_proc

    if _tor_proc:
        print("tor.py stopping tor...")
        _tor_proc.kill()
        _tor_proc = None


"""
CURRENT KNOWN ISSUES:
- sometimes the tor connection will drop.
- the tor interface is not able to use an existing tor connection.
- the tor interface is not able to find tor in other locations.
"""
