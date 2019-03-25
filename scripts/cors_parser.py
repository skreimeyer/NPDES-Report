#! /usr/bin/env python3
"""
EPA discharge monitoring reports can be downloaded as 'CORS'
CORS are available in XML format. This parser will walk a directory for files
named 'dmrSubmission.xml', queue these filenames and then spawn a few processes
to extract the target information and write these files out to a csv.

### development notes

Primary goal:
[X] - read a sample xml file. Create a dictionary of metadata and sample values
[X] - walk the CORS directory and find all report files
[X] - output a csv compatible with the historical DMR data csv

Secondary goal:
[ ] - filter out reports using a datetime from CLI args
[ ] - take the target walk directory from CLI args
[ ] - reformat DMR csv for ergonomics. Refactor this script to match that format


"""
from os import walk, path
import xml.etree.ElementTree as ET
import csv


def parse_record(xml_file):
    """dmrSubmission.xml files have a predictable structure, so we can take the
    fairly complex xml and extract only the information we care about and write
    it to a dictionary that can conveniently handled by other functions.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # metadata
    location = root.find("PermittedFeatureIdentifier").text
    rep_date = root.find("MonitoringPeriodEndDate").text
    # node containing measurements
    params = root.find("Parameters")
    # target data-structure for measurements
    results = {}
    for child in params:
        try:
            name = child.find("ParameterName").text
            # Flow values are stored in a different end-node, so we need a condition
            if name == "Flow, in conduit or thru treatment plant":
                units = child.find("PermitQuantityUnitDescription").text
                value = child.find("Quantity2").find("ReportedValue").text
            else:
                units = child.find("PermitConcentrationUnitDescription").text
                value = child.find("Concentration3").find("ReportedValue").text
            results[name] = {"units": units, "value": value}
        except:
            # This will only happen if no results were recorded, so kill the loop
            # return None so we can detect this error downstream
            return None
    return {"date": rep_date, "location": location, "data": results}


def find_records(directory="../assets/CORS"):
    """By convention, the CORS files will live in assets/CORS, but we can take
    an argument of a different directory name if we want. The result is an array
    of paths to 'dmrSubmission.xml' files that live in our CORS directory.
    """
    # empty array of file paths
    results = []
    target = "dmrSubmission.xml"
    for root, _, files in walk(directory):
        if target in files:
            results.append(path.join(root, target))
    return results


def write_out(target="../data/NewDMR.csv"):
    """Our csv output *might* not be safe to append to our DMR data directly,
    so currently the implementation is to just write to a new file and then
    copy and paste the rows we actually need into 'CLR DMV.csv'

    Ideally, a future refactor should include checks on dates, so that we are
    not overwriting our past data, or, worse, we are creating duplicate rows and
    polluting our data source.
    """

    def flatten(datum):
        """Convenience closure to take our nested data and return an array with
        one item for each measurement.
        """
        results = []
        for k, v in datum["data"].items():
            row = [
                datum["location"],
                k,
                v["units"],
                "1 / 3 MO.",
                datum["date"],
                v["value"],
            ]
            results.append(row)
        return results

    header = ["Location", "Parameter", "Unit", "Frequency", "Date", "Value"]
    data = []
    raw_data = list(map(parse_record, find_records()))
    # flatten. I don't actually remember why this was a more convenient format
    # for the csv...
    for rd in raw_data:
        if rd:  # Beceause we might get 'None'
            data += flatten(rd)
    with open(target, "w") as csvoutfile:
        cw = csv.writer(csvoutfile)
        cw.writerow(header)
        cw.writerows(data)


if __name__ == "__main__":
    write_out()
