#! /usr/bin/env python3
"""
Generates a markdown-formatted report from the templates directory using data
from the report-data.yml file in the data folder. Nothing more, nothing less.
"""

from jinja2 import FileSystemLoader, Environment
import yaml
import csv
import os
import subprocess

import pdb

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
        border = "|"+"----------|"*len(data[0])
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
template = environment.get_template("narrative.tmpl")
# render and write to narrative.md in the report folder
with open("../report/narrative.md", "w") as outfile:
    outfile.write(template.render(report_data))

templateC = environment.get_template("appendixC.tmpl")
# render and write to appendixC.md in the report folder
with open("../report/appendixC.md", "w") as outfile:
    outfile.write(templateC.render(report_data))

# load education data
with open("../data/education-data.yml","r") as infile:
    education_data = yaml.load(infile)

templateD = environment.get_template("appendixD.tmpl")
# render and write to appendixD.md in the report folder
with open("../report/appendixD.md", "w") as outfile:
    outfile.write(templateD.render(education_data))

# fetch all radar chart images.
radar_imgs = {'images':[i for i in os.listdir("../figures") if "radar" in i]}

templateE = environment.get_template("appendixE.tmpl")
# render and write to appendixE.md in the report folder
with open("../report/appendixE.md", "w") as outfile:
    outfile.write(templateE.render(radar_imgs))

# fetch all time-series chart images.
time_imgs = {'images':[i for i in os.listdir("../figures") if "time" in i]}

templateF = environment.get_template("appendixF.tmpl")
# render and write to appendixF.md in the report folder
with open("../report/appendixF.md", "w") as outfile:
    outfile.write(templateF.render(time_imgs))

# fetch all regional box plot images.
seasonal_images = {'images':[i for i in os.listdir("../figures") if "seasonal" in i]}

templateG = environment.get_template("appendixG.tmpl")
# render and write to appendixE.md in the report folder
with open("../report/appendixG.md", "w") as outfile:
    outfile.write(templateG.render(seasonal_images))

# fetch all seasonal box plot images.
regional_images = {'images':[i for i in os.listdir("../figures") if "regional" in i]}

templateH = environment.get_template("appendixH.tmpl")
# render and write to appendixE.md in the report folder
with open("../report/appendixH.md", "w") as outfile:
    outfile.write(templateH.render(regional_images))

# We're done with markdown. Call pandoc, generate pdfs and merge into top level
wd = os.path.join(os.path.dirname(os.getcwd()),'report') # we can't do directory transversal with the cwd kwarg

targets = [
'narrative.md',
'appendixC.md',
'appendixD.md',
'appendixE.md',
'appendixF.md',
'appendixG.md',
'appendixH.md'
]
subprocess.run(["pwd"],cwd=wd)
for t in targets:
    outputname = t.split('.')[0]+'.pdf'
    try:
        subprocess.run(["pandoc",f'{t}','-o',f'tmp/{outputname}'], cwd=wd)
        print(f'Wrote {outputname}')
    except:
        print(f'Failed to write component pdf file {outputname}')
# pdb.set_trace()
all_pdfs = [f'tmp/{f}' for f in sorted(os.listdir('../report/tmp'))]
# move narrative to the front
all_pdfs.insert(0,all_pdfs.pop())
pdfunite_args = ['pdfunite']+all_pdfs+['../report.pdf']
try:
    subprocess.run(pdfunite_args, cwd=wd)
    print('PDFs merged . . . exiting')
except:
    print("Failed to merge pdfs")

quit(0)
