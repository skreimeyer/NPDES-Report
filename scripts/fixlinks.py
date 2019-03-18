#! /usr/environment python3
"""
Throwaway script to format working links in the template.
"""
import re

with open("../templates/report.tmpl", "r") as infile:
    report = infile.readlines()

link_preamble = re.compile(r"^\[")
link_content = re.compile(r"(?<=\(#).*(?=\)$)")
title_preamble = re.compile(r"^#+")
title = re.compile(r"(?<=#)\s.*")


# slug-ify link text in the table of contents
for i, line in enumerate(report):
    if link_preamble.match(line):
        found = link_content.search(line)
        if found:
            link_string = found.group(0)
            new_string = re.sub("\s", "-", link_string.strip())
            report[i] = re.sub(link_content, new_string, line)
    # make anchors
    if title_preamble.match(line) and i > 9:
        found = title.search(line)
        if found:
            name_field = re.sub("\s", "-", found.group(0).strip())
            anchor = f'<a name="{name_field}"></a>\n'
            report[i] = line.strip() + anchor

with open("../templates/report-fix.tmpl", "w") as outfile:
    outfile.writelines(report)
