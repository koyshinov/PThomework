import datetime
import json
import os
import importlib.util

from config import DB_FILE, CONTROLS_FILE, STATUS_EXCEPTION, C_FAIL, C_OKGREEN, C_WARNING, C_END, TRANSPORTS_CONFIG_FILE

from models import db, Control, Scandata
from reporting import print_report


def check_env():
    try:
        with open(TRANSPORTS_CONFIG_FILE, 'r') as f:
            env = json.load(f)

        assert env.get("host")

        transports_ = env.get("transports")

        assert transports_

        ssh_ = transports_.get("SSH")

        if ssh_:
            assert ssh_.get("port")
            assert ssh_.get("login")
            assert ssh_.get("password")

        mysql_ = transports_.get("MySQL")

        if mysql_:
            assert mysql_.get("port")
            assert mysql_.get("login")
            assert mysql_.get("password")
            assert mysql_.get("db")

    except (AssertionError, json.decoder.JSONDecodeError):
        print("[{FAIL}ERR{END}] {TRANSP_C_FILE} file error! Test the project (doc tests/README.md)".format(
            FAIL=C_FAIL, END=C_END, TRANSP_C_FILE=TRANSPORTS_CONFIG_FILE))
        close_program()


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
                    uid=uid,
                    filename=contrs.get(uid).get("filename"),
                    title=contrs.get(uid).get("title"),
                    requirements=contrs.get(uid).get("requirements"),
                    description=contrs.get(uid).get("description")
                )

    except (ValueError, FileNotFoundError):
        print("[{FAIL}ERR{END}] {CONTROLS_FILE} file error! Test the project (doc tests/README.md)".format(
            FAIL=C_FAIL, END=C_END, CONTROLS_FILE=CONTROLS_FILE))
        close_program()
    else:
        print("[{OK}OK{END}]  Imported data from {CONTROLS_FILE}".format(OK=C_OKGREEN, END=C_END,
                                                                         CONTROLS_FILE=CONTROLS_FILE))


def add_control(filename, status, time_sec):
    contrs = Control.filter(filename=filename)
    if not contrs:
        contr = Control.create(filename=filename)
        print("[{WARN}WR{END}]  Control info about {SCRIPT} not found!".format(
            WARN=C_WARNING, END=C_END, SCRIPT=filename))
    else:
        contr = contrs[0]

    Scandata.create(control=contr, status=status, lead_time_sec=time_sec)


def run():
    total_time_start = datetime.datetime.now()

    try:
        if os.path.isfile(DB_FILE):
            os.remove(DB_FILE)
            print("[{OK}OK{END}]  Removed old {DB_FILE}.".format(OK=C_OKGREEN, END=C_END, DB_FILE=DB_FILE))

        db.connect()
        print("[{OK}OK{END}]  Connected to new {DB_FILE} database.".format(OK=C_OKGREEN, END=C_END, DB_FILE=DB_FILE))
        db.create_tables([Control, Scandata])
        print("[{OK}OK{END}]  Created tables.".format(OK=C_OKGREEN, END=C_END))
    except Exception as e:
        print("[{FAIL}ERR{END}] Unknown working problem with db".format(FAIL=C_FAIL, END=C_END))
        print("      Exception:", e)
        close_program()

    try:
        check_env()
        imp_controls_from_json()
    except Exception as e:
        print("[{FAIL}ERR{END}] Unknown problem with configuration files".format(FAIL=C_FAIL, END=C_END))
        print("      Exception:", e)
        close_program()

    try:
        for file in os.listdir("scripts"):
            if file.endswith(".py"):
                scriptname = file[:-3]
                time_start = datetime.datetime.now()

                try:
                    scriptpack = importlib.import_module("scripts.%s" % scriptname)
                    status = scriptpack.main()
                except Exception as e:
                    status = STATUS_EXCEPTION
                    print("[{WARN}WR{END}]  Finished script {SCRIPT} with status {STATUS}".format(
                        WARN=C_WARNING, END=C_END, SCRIPT=scriptname, STATUS=status))
                    print("      Exception:", e)
                else:
                    print("[{OK}OK{END}]  Finished script {SCRIPT} with status {STATUS}".format(
                        OK=C_OKGREEN, END=C_END, SCRIPT=scriptname, STATUS=status))

                time_delta = datetime.datetime.now() - time_start
                add_control(scriptname, status, time_delta.total_seconds())
    except Exception as e:
        print("[{FAIL}ERR{END}] Unknown problem scripts".format(FAIL=C_FAIL, END=C_END))
        print("      Exception:", e)
        close_program()

    total_time_finish = datetime.datetime.now()

    duration = (total_time_finish - total_time_start).total_seconds()

    scan_info = {
        "time_of_start_scanning": total_time_start.strftime("%d-%m-%Y %H:%M:%S"),
        "time_of_finish_scanning": total_time_finish.strftime("%d-%m-%Y %H:%M:%S"),
        "total_sec_scanning": duration
    }

    report_path = print_report(scan_info)

    db.close()

    full_durn = (datetime.datetime.now() - total_time_start).total_seconds()

    print("[{OK}OK{END}]  Closing database".format(OK=C_OKGREEN, END=C_END))
    print("[{OK}OK{END}]  It's fine! Scan took {SEC:0.2} seconds ".format(OK=C_OKGREEN, END=C_END, SEC=full_durn))

    return report_path


def close_program():
    print("[{FAIL}ERR{END}] Exiting program".format(FAIL=C_FAIL, END=C_END))
    exit()


if __name__ == "__main__":
    run()
