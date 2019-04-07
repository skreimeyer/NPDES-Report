**Status: Stable. All necessary functionality is present.**

# City of Little Rock annual NPDES report

Each year the City of Little Rock must produce a report on the condition of the Municipal Separate Storm Sewer System (MS4). The contents of this report are specified in the NPDES permit issued by Arkansas Department of Environmental Quality (ADEQ). Permits only change about every five years, so reporting tends to be highly formulaic.

Taking advantage of the predictability of the reports, the only thing that really needs to change are specific data points, such as the number of linear feet of drains cleaned, yards of litter removed by street sweepers, etc.

This repository should be able to be adapted to other municipal reports, or, at least the basic methodology. At a minimum, the template file would have to be rewritten to meet whatever your municipality/county/individual reporting requirements are. The DMR parser and graphing utilities are probably the most reusable.

## Ultimate project goals

- [X] Jinja2 template magic produces a passable-looking report in markdown
- [X] Parser for EPA CDX DMRs
- [X] Automatically generate informative graphs from the water quality data
- [ ] Static site generator creates a page for the report to be used on http://www.littlerock.gov
- [X] Refactor the scripts to make them more flexible
