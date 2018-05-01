import json
import os
import jinja2
import weasyprint

from config import TRANSPORTS_CONFIG_FILE, STATUS_COMPLIANT, STATUS_NOT_APPLICABLE
from peewee_models import Scandata


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

    template = env.get_template('index.html')
    whtml = weasyprint.HTML(string=template.render(data).encode('utf8'))
    wcss = weasyprint.CSS(filename='./templates/style.css')

    if not os.path.isdir("reports/{}".format(system_info.get("host"))):
        os.makedirs("reports/{}".format(system_info.get("host")))

    whtml.write_pdf('reports/{}/report at {}.pdf'.format(
        system_info.get("host"),
        scan_info.get("time_of_start_scanning")
    ), stylesheets=[wcss])
