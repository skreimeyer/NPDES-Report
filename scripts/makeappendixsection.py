"""
Note that the dictionary order MUST be rearranged in report-data.yml!
"""

import os
import yaml

allfiles = os.listdir('../figures')

radar = [a for a in allfiles if 'radar' in a]
timeseries = [a for a in allfiles if 'time' in a]
seasonal = [a for a in allfiles if 'seasonal' in a]
regional = [a for a in allfiles if 'regional' in a]

firstReport = {
'title': '1997 NPDES Report',
'link': 'assets/old-reports/Report 1997.pdf'
}
permit = {
'title': 'City of Little Rock and ARDOT District VI NPDES Permit',
'link': 'assets/ARS000002 - 2013 Final.pdf'
}
annexations = {
'title': 'Annexations',
'contents': {
'title': 'Recent Annexations in the City of Little Rock',
'caption': 'Lands incorporated into the City of Little Rock within the report year',
'location':'figures/annexations.png'
}
}

monitoringSummary = {
'title': 'Monitoring Summary'
}
radarlist = []
for r in radar:
    item = {}
    yr = r[6:10]
    item['title'] = f'City of Little Rock Water Quality Parameters for {yr}'
    item['location'] = f'figures/{r}'
    item['caption'] = f'Radar chart showing all parameters measured during {yr} normalized to available EPA water quality recommendations for the area. Where specific guidance is absent, measurements are normalized to the 95th percentile of all previous measures'
    radarlist.append(item)
monitoringSummary['contents'] = radarlist

trendAnalysis = {
'title': 'Water Quality Trend Analysis'
}
timeserieslist = []
for t in timeseries:
    item = {}
    param = t.split('-')[1][:-4]
    item['title'] = f'City of Little Rock Water Quality Parameters for {param}'
    item['location'] = f'figures/{t}'
    item['caption'] = f'Scatter plot of water quality measurements for {param} at each sampling location. The `median` line is the median for measurements at all locations passed through a noise-filtering algorithm for better legibility'
    timeserieslist.append(item)
trendAnalysis['contents'] = timeserieslist

seasonalAnalysis = {
'title': 'Seasonal Analysis'
}
seasonallist = []
for t in seasonal:
    item = {}
    param = t.split('-')[1][:-4]
    item['title'] = f'City of Little Rock Water Quality Parameters for {param} by season'
    item['location'] = f'figures/{t}'
    item['caption'] = f'Distributions of measurements for {param} from all recorded measurements grouped by season.'
    seasonallist.append(item)
seasonalAnalysis['contents'] = seasonallist

regionalAnalysis = {
'title': 'Regional Analysis'
}
regionallist = []
for r in regional:
    item = {}
    param = t.split('-')[1][:-4]
    item['title'] = f'City of Little Rock Water Quality Parameters for {param} by Region'
    item['location'] = f'figures/{t}'
    item['caption'] = f'Distributions of measurements for {param} from all recorded measurements grouped by location.'
    regionallist.append(item)
regionalAnalysis['contents'] = regionallist

educationalResources = {
'title': 'Educational and Outreach Material',
}
edimgs = []
for e in os.listdir('../assets/images/'):
    item = {}
    item['title'] = e.split('.')[0]
    item['location'] = f'assets/images/{e}'
    item['caption'] = 'Example promotional and educational material used by the City of Little Rock to promote water qualtiy.'
    edimgs.append(item)
educationalResources['contents'] = edimgs

main = {}
main['appendices'] = {
'permit':permit,
'firstReport':firstReport,
'annexations':annexations,
'regionalAnalysis':regionalAnalysis,
'seasonalAnalysis':seasonalAnalysis,
'monitoringSummary':monitoringSummary,
'trendAnalysis':trendAnalysis,
'educationalResources':educationalResources
}

i = 'A'
for key,value in main['appendices'].items():
    value['index']  = i
    i = chr(ord(i)+1)


with open('test','w') as outfile:
    outfile.write(yaml.dump(main))
