# stdlib.
import json
from argparse import ArgumentParser
from os import makedirs
from os.path import  join, dirname

# toml.
import tomlkit
from tomlkit import TOMLDocument


def addCommonArgs(p_parser: ArgumentParser):
    p_parser.add_argument("-o", default= join(".", "downloads"), help= "relative desired path for output")

    p_parser.add_argument("--json", action= "store_true", help= "grab metadata as json")
    p_parser.add_argument("--toml", action= "store_true", help= "grab metadata as toml")


def writeJSON(p_outpath: str, p_data: dict):

    json_data = json.dumps(p_data, indent= 4)
    makedirs(dirname(p_outpath), exist_ok=True)

    with open(p_outpath + ".json", "w") as record:
        record.write(json_data)


def writeTOML(p_outpath: str, p_data: dict):

    toml_data: TOMLDocument = tomlkit.document()
    makedirs(dirname(p_outpath), exist_ok=True)

    for key in p_data:
        toml_data.add(key, p_data[key])

    with open(p_outpath + ".toml", "w", encoding= "utf-8") as record:
        record.write(tomlkit.dumps(toml_data))


def writePayload(p_outpath: str, p_payload):
    makedirs(dirname(p_outpath), exist_ok= True)

    with open(p_outpath, "wb") as out:
        out.write(p_payload)


# ==================================================================================================== #
# selenium.


# stdlib.
import sqlite3
from http import cookiejar
from os import environ, listdir
from os.path import splitext
from platform import system

# selenium.
from selenium.common import TimeoutException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


_os: str = system().lower()
_driver: WebDriver | None = None


def _handleFirefox() -> bool:

    def startDriver(p_profile_dir: str):
        global _driver

        options = FirefoxOptions()
        options.set_preference("profile", p_profile_dir)
        #options.headless = True

        _driver = Firefox(options=options)

        jar: cookiejar.CookieJar = cookiejar.CookieJar()

        database = sqlite3.connect(join(p_profile_dir, "cookies.sqlite"))
        cursor = database.cursor()
        #cursor.execute("SELECT * from moz_cookies")
        cursor.execute("PRAGMA table_info(moz_cookies)")

        for name in cursor.fetchall():
            #jar.set_cookie(cookie)
            print(name)

    # ---- handle os. ---- #

    if _os == "windows":
        profiles_dir = join(environ["APPDATA"], "Mozilla", "Firefox", "Profiles")

        for dir in listdir(profiles_dir):
            if splitext(dir)[1] == ".default-release":
                startDriver(join(profiles_dir, dir))

    # elif _os == "linux":

    # elif _os == "darwin":

    else:
        return False

    return True


def _handleBrave() -> bool:

    def startDriver(p_profile_dir: str):
        pass

    pass


def _handleChrome() -> bool:

    def startDriver(p_profile_dir: str):
        pass

    pass


def _handleSafari() -> bool:

    def startDriver(p_profile_dir: str):
        pass

    pass


def _handleEdge() -> bool:

    def startDriver(p_profile_dir: str):
        pass

    pass


_BROWSER_HANDLERS: dict = {
    "firefox": _handleFirefox,
    #"brave": _handleBrave,
    #"chrome": _handleChrome,
    #"safari": _handleSafari,
    #"edge": _handleEdge
}


_SYSTEM_BROWSERS: dict = {
    "windows": ["firefox"]#,#, "brave", "chrome", "edge"],
    #"linux": ["firefox"],#, "brave", "chrome"],
    #"darwin": ["firefox"]#, "brave", "chrome", "safari"]
}


def tryHandleBrowser(p_name: str):
    print(_os)

    if _os in _SYSTEM_BROWSERS.keys():
        if p_name in _SYSTEM_BROWSERS[_os]:
            return _BROWSER_HANDLERS[p_name]()

        else: print(f"Unhandled browser \"{p_name}\" selected on system \"{_os}\"")
    else: print(f"Browsers for system \"{_os}\" are not handled.")

    return False


def getPage(p_url: str) -> bool:
    retry: bool = True

    while retry:
        try:
            WebDriverWait(_driver, 10).until(ec.url_matches(p_url))
            return True

        except TimeoutException:
            good_in: bool = False

            while not good_in:
                yes = ['y', 'Y']
                no = ['n', 'N']

                user_in = input("page get failed. retry? (y/n):")

                if user_in in yes:      good_in = True; retry = True
                elif user_in in no:     good_in = True; retry = False

    return False


def find(p_mode, p_target: str) -> WebElement:
    return _driver.find_element(p_mode, p_target)


def findAll(p_mode, p_target: str) -> list[WebElement]:
    return _driver.find_elements(p_mode, p_target)
