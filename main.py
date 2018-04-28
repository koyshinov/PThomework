import json
import os
import importlib

from peewee_models import db, Control, Scandata


def imp_controls_from_json(json_filepath='controls.json'):
    try:
        with open(json_filepath, 'r') as f:
            contrs = json.load(f)

        query = Control.select()
        cursor = db.execute(query)

        control_fnames = [x[0] for x in cursor.fetchall()]

        for filename, description in contrs:
            if filename not in control_fnames:
                Control.create(filename=filename, description=description)
    except (ValueError, FileNotFoundError):
        print("Problems with controls.json! File is not exist, or format is not correct")


def add_control(filename, status):
    contrs = Control.filter(filename=filename)
    if not contrs:
        contr = Control.create(filename=filename)
    else:
        contr = contrs[0]

    Scandata.create(control=contr, status=status)


def run():
    if os.path.isfile("sqlite.db"):
        os.remove("sqlite.db")

    db.connect()
    db.create_tables([Control, Scandata])

    imp_controls_from_json()

    for file in os.listdir("scripts"):
        if file.endswith(".py"):
            try:
                scriptname = file[:-3]
                scriptpack = importlib.import_module("scripts.%s" % scriptname)
                status = scriptpack.main()
            except Exception as e:
                print(e)
                status = 5
            add_control(scriptname, status)

    db.close()


if __name__ == "__main__":
    run()