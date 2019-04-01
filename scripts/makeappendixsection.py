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
'linktitle': '1997 NPDES Report',
'link': 'assets/old-reports/Report 1997.pdf',
'index': 'B',
'preamble': 'The first report by the City of Little Rock on the status of the MS4 was given in 1997 and can be found in the link below.'
}
permit = {
'title': 'City of Little Rock and ARDOT District VI NPDES Permit',
'linktitle': 'ARS00002',
'link': 'https://github.com/skreimeyer/NPDES-Report/blob/master/assets/ARS000002%20-%202013%20Final.pdf',
'index': 'A',
'preamble': 'The contents of this report have been prepared to confirm to ADEQ discharge permit ARS000002, which can be found at the link below.'
}
annexations = {
'title': 'Annexations',
'contents': [{
'title': 'Recent Annexations in the City of Little Rock',
'caption': 'Lands incorporated into the City of Little Rock within the report year. A total of 284 acres was annexed in 2018',
'location':'figures/annexations.png',
'index': 'C',
'preamble': 'All annexations for the permit year are given in this section.'
}]
}

monitoringSummary = {
'title': 'Monitoring Summary',
'index': 'E',
'preamble': 'Water quality monitoring results in the MS4 are represented in this section. Radar charts are given for their expressive visualization of the large number of measured parameters.'
}
radarlist = []
for r in radar:
    item = {}
    yr = r[6:10]
    # item['title'] = f'City of Little Rock Water Quality Parameters for {yr}'
    item['location'] = f'figures/{r}'
    # item['caption'] = f'Radar chart showing all parameters measured during {yr} normalized to available EPA water quality recommendations for the area. Where specific guidance is absent, measurements are normalized to the 95th percentile of all previous measures'
    radarlist.append(item)
monitoringSummary['contents'] = radarlist

trendAnalysis = {
'title': 'Water Quality Trend Analysis',
'index': 'F',
'preamble': 'The time series data recorded for the purpose of this permit is complex, and meaningful visualization of data is challenging. To assist with interpreting useful information from the high levels of noise, the median value of measurements is provided with a savgol filter.'
}
timeserieslist = []
for t in timeseries:
    item = {}
    param = t.split('-')[1][:-4]
    # item['title'] = f'City of Little Rock Water Quality Parameters for {param}'
    item['location'] = f'figures/{t}'
    # item['caption'] = f'Scatter plot of water quality measurements for {param} at each sampling location. The `median` line is the median for measurements at all locations passed through a noise-filtering algorithm for better legibility'
    timeserieslist.append(item)
trendAnalysis['contents'] = timeserieslist

seasonalAnalysis = {
'title': 'Seasonal Analysis',
'index': 'G',
'preamble': 'Distributions of measurements from 1997 to the present for each measured parameter are given in this section. There are no variations in these distributions of note.'
}
seasonallist = []
for s in seasonal:
    item = {}
    param = s.split('-')[1][:-4]
    # item['title'] = f'City of Little Rock Water Quality Parameters for {param} by season'
    item['location'] = f'figures/{s}'
    # item['caption'] = f'Distributions of measurements for {param} from all recorded measurements grouped by season.'
    seasonallist.append(item)
seasonalAnalysis['contents'] = seasonallist

regionalAnalysis = {
'title': 'Regional Analysis',
'index': 'H',
'preamble':'Distributions of measurements are separated by region. While there does appear to be some regional variation in some of the measured parameters, these variations do not appear to be indicative of significant water quality concerns.'
}
regionallist = []
for r in regional:
    item = {}
    param = r.split('-')[1][:-4]
    # item['title'] = f'City of Little Rock Water Quality Parameters for {param} by Region'
    item['location'] = f'figures/{r}'
    # item['caption'] = f'Distributions of measurements for {param} from all recorded measurements grouped by location.'
    regionallist.append(item)
regionalAnalysis['contents'] = regionallist

educationalResources = {
'title': 'Educational and Outreach Material',
'index': 'D',
'preamble': 'The City of Little Rock makes use of a wide variety of media in its work to promote education about water quality. Several of the publications used by the City are given in this section.'
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
'a_permit':permit,
'b_firstReport':firstReport,
'c_annexations':annexations,
'h_regionalAnalysis':regionalAnalysis,
'g_seasonalAnalysis':seasonalAnalysis,
'e_monitoringSummary':monitoringSummary,
'f_trendAnalysis':trendAnalysis,
'd_educationalResources':educationalResources
}



with open('latex-friendly','w') as outfile:
    outfile.write(yaml.dump(main))
