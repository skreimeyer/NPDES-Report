#! /usr/env/python3
"""
Generates a markdown-formatted report from the templates directory using data
from the report-data.yml file in the data folder. Nothing more, nothing less.
"""

from jinja2 import FileSystemLoader, Environment
import yaml

environment = Environment(loader=FileSystemLoader("../templates"))
# Custom slugify filter
def slugify(text):
    """replaces white-space separation with hyphens"""
    return "-".join(text.split())


environment.filters["slugify"] = slugify

# load reporting data
with open("../data/report-data.yml", "r") as infile:
    report_data = yaml.load(infile)
# load template
template = environment.get_template("report.tmpl")
# render and write to report.md in the top folder
with open("../report.md", "w") as outfile:
    outfile.write(template.render(report_data))
