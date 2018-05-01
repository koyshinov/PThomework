import datetime
import json
import os
import importlib

from config import DB_FILE, CONTROLS_FILE, STATUS_EXCEPTION
from peewee_models import db, Control, Scandata
from reporting import print_report


def imp_controls_from_json(json_filepath=CONTROLS_FILE):
    try:
        with open(json_filepath, 'r') as f:
            contrs = json.load(f)

        query = Control.select()
        cursor = db.execute(query)

        control_fnames = [x[0] for x in cursor.fetchall()]

        for uid in contrs:
            if contrs.get("filename") not in control_fnames:
                Control.create(
                    uid = uid,
                    filename = contrs.get(uid).get("filename"),
                    title = contrs.get(uid).get("title"),
                    requirements = contrs.get(uid).get("requirements"),
                    description = contrs.get(uid).get("description")
                )

    except (ValueError, FileNotFoundError):
        print("Problems with %s! File is not exist, or format is not correct" % CONTROLS_FILE)


def add_control(filename, status, time_sec):
    contrs = Control.filter(filename=filename)
    if not contrs:
        contr = Control.create(filename=filename)
    else:
        contr = contrs[0]

    Scandata.create(control=contr, status=status, lead_time_sec=time_sec)


def run():
    if os.path.isfile(DB_FILE):
        os.remove(DB_FILE)

    db.connect()
    db.create_tables([Control, Scandata])

    imp_controls_from_json()

    total_time_start = datetime.datetime.now()

    for file in os.listdir("scripts"):
        if file.endswith(".py"):
            scriptname = file[:-3]
            time_start = datetime.datetime.now()
            try:
                scriptpack = importlib.import_module("scripts.%s" % scriptname)
                status = scriptpack.main()
            except Exception as e:
                print(e)
                status = STATUS_EXCEPTION
            time_delta = datetime.datetime.now() - time_start
            add_control(scriptname, status, time_delta.total_seconds())

    total_time_finish = datetime.datetime.now()

    duration = (total_time_finish - total_time_start).total_seconds()

    scan_info = {
        "time_of_start_scanning": total_time_start.strftime("%d-%m-%Y %H:%M:%S"),
        "time_of_finish_scanning": total_time_finish.strftime("%d-%m-%Y %H:%M:%S"),
        "total_sec_scanning": duration
    }

    print_report(scan_info)

    db.close()


if __name__ == "__main__":
    run()
