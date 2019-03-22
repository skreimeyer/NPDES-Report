#! /usr/env/python3
"""
Generates a markdown-formatted report from the templates directory using data
from the report-data.yml file in the data folder. Nothing more, nothing less.
"""

from jinja2 import Template
import yaml

# load reporting data
with open("../data/report-data.yml", "r") as infile:
    report_data = yaml.load(infile)
# load template
with open("../templates/report.tmpl", "r") as infile:
    template = Template(infile.read())
# render and write to report.md in the top folder
with open("../report.md", "w") as outfile:
    outfile.write(template.render(report_data))
