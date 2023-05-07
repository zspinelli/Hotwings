# stdlib.
import json
from argparse import ArgumentParser
from os import makedirs
from os.path import join, dirname

# toml.
import tomlkit
from tomlkit import TOMLDocument, table


def addCommonArgs(p_parser: ArgumentParser):
    p_parser.add_argument("-o", default= join(".", "downloads"), help= "relative desired path for output")


def addMetaArgs(p_parser: ArgumentParser):
    p_parser.add_argument("--json", action= "store_true", help= "grab metadata as json")
    p_parser.add_argument("--toml", action= "store_true", help= "grab metadata as toml")
    p_parser.add_argument("--fibr", action= "store_true", help= "grab metadata for filebrary")


def addResumeArgs(p_parser: ArgumentParser):
    p_parser.add_argument("--sdr", action= "store_true", help= "store date for resume")


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


def writeFIBR(p_outpath: str, p_name: str, p_tags: list, p_desc: str, p_extra: dict):

    fibr_data: TOMLDocument = tomlkit.document()
    makedirs(dirname(p_outpath), exist_ok=True)

    fields_table: table = table()
    fibr_data.add("fields", fields_table)

    fields_table.add("name", p_name)
    fields_table.add("tags", p_tags)
    fields_table.add("desc", p_desc)

    extra_table: table = table()
    fibr_data.add("extra", extra_table)

    for e in p_extra:
        extra_table.add(e, p_extra[e])

    with open(p_outpath + ".fibr", "w", encoding= "utf-8") as record:
        record.write(tomlkit.dumps(fibr_data))


def writePayload(p_outpath: str, p_payload):
    makedirs(dirname(p_outpath), exist_ok= True)

    with open(p_outpath.encode("utf-8"), "wb") as out:
        out.write(p_payload)

