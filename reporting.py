import json
import os
import jinja2
import weasyprint

from config import TRANSPORTS_CONFIG_FILE, STATUS_COMPLIANT, STATUS_NOT_APPLICABLE, C_OKGREEN, C_END, C_FAIL
from models import Scandata


def print_report(scan_info):
    controls_query = Scandata.select()

    controls_info = [{
        "uid": i.control.uid,
        "filename": i.control.filename,
        "title": i.control.title,
        "requirements": i.control.requirements,
        "description": i.control.description,
        "dur_secs": i.lead_time_sec,
        "status": i.status,
        "print_status": Scandata.STATUS_FROM_CODE.get(i.status)
    } for i in controls_query.iterator()]

    with open(TRANSPORTS_CONFIG_FILE, 'r') as f:
        system_info = json.load(f)

    count_of_bad_connection = controls_query.filter(status=STATUS_NOT_APPLICABLE).count()

    count_contrs = controls_query.count()
    count_compliant_contrs = controls_query.filter(status=STATUS_COMPLIANT).count()
    percent_of_cc = "{:0.2f}".format(count_compliant_contrs / count_contrs * 100)

    data = {
        "scan_info": scan_info,
        "system_info": system_info,
        "controls_info": controls_info,
        "count_contrs": count_contrs,
        "count_compliant_contrs": count_compliant_contrs,
        "percent_of_cc": percent_of_cc,
        "count_of_bad_connection": count_of_bad_connection
    }

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )

    try:
        template = env.get_template('index.html')
        print("[{OK}OK{END}]  Get template index.html".format(OK=C_OKGREEN, END=C_END))
        whtml = weasyprint.HTML(string=template.render(data).encode('utf8'))
        print("[{OK}OK{END}]  Render template".format(OK=C_OKGREEN, END=C_END))
        wcss = weasyprint.CSS(filename='./templates/style.css')

        host = system_info.get("host")

        if not os.path.isdir("reports/{}".format(host)):
            os.makedirs("reports/{}".format(system_info.get("host")))
            print("[{OK}OK{END}]  Created dir {HOST} in reports folder".format(OK=C_OKGREEN, END=C_END, HOST=host))

        report_path = 'reports/{}/report at {}.pdf'.format(host, scan_info.get("time_of_start_scanning"))

        whtml.write_pdf(report_path, stylesheets=[wcss])

        print("[{OK}OK{END}]  Created report {REPORT}".format(OK=C_OKGREEN, END=C_END, REPORT=report_path))

        return os.path.abspath(report_path)

    except jinja2.exceptions.TemplateNotFound:
        print("[{FAIL}ERR{END}] Can't find ./templates/index.html".format(FAIL=C_FAIL, END=C_END))
        close_program()
    except FileNotFoundError:
        print("[{FAIL}ERR{END}] Can't find ./templates/style.css".format(FAIL=C_FAIL, END=C_END))
        close_program()
    except Exception as e:
        print("[{FAIL}ERR{END}] Unknown problem with making report".format(FAIL=C_FAIL, END=C_END))
        print("      Exception:", e)
        close_program()


def close_program():
    print("[{FAIL}ERR{END}] Exiting program".format(FAIL=C_FAIL, END=C_END))
    exit()
