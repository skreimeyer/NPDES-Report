#! /usr/bin/env python3
"""
Generates a markdown-formatted report from the templates directory using data
from the report-data.yml file in the data folder. Nothing more, nothing less.
"""

from jinja2 import FileSystemLoader, Environment
import yaml
import csv

testmeta = {"index":1,"title":"This is the title","caption":"a caption","filename":"../data/csv/test.csv"}


environment = Environment(loader=FileSystemLoader("../templates"))
# Custom slugify filter
def slugify(text):
    """replaces white-space separation with hyphens"""
    return "-".join(text.split())

def maketable(tablemeta):
    """must only accept dictionary objects which possess the 'filename' key"""
    filename = tablemeta['filename']
    outputs = []
    with open(filename,'r') as csvfile:
        data = [row for row in csv.reader(csvfile)]
        title = tablemeta['title']
        slugged = slugify(title)
        title_heading = f'### {title}<a name="{slugged}"></a>'
        headers = "| "+" | ".join([h for h in data[0]])+" |"
        border = "|"+"---|"*len(data[0])
        outputs = [title_heading,headers,border]
        for row in data[1:]:
            outputs.append("| "+" | ".join([d for d in row])+" |")
        outputs.append(f'\nTable {tablemeta["index"]}: {tablemeta["caption"]}')
    return '\n'.join(outputs)

# register the filter
environment.filters["slugify"] = slugify
environment.filters["maketable"] = maketable

# load reporting data
with open("../data/report-data.yml", "r") as infile:
    report_data = yaml.load(infile)
# load template
template = environment.get_template("report.tmpl")
# render and write to report.md in the top folder
with open("../report.md", "w") as outfile:
    outfile.write(template.render(report_data))
