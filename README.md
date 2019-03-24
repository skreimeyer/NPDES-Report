# City of Little Rock annual NPDES report

Each year the City of Little Rock must produce a report on the condition of the Municipal Separate Storm Sewer System (MS4). The contents of this report are specified in the NPDES permit issued by Arkansas Department of Environmental Quality (ADEQ). Permits only change about every five years, so reporting tends to be highly formulaic.

Taking advantage of the predictability of the reports, the only thing that really needs to change are specific data points, such as the number of linear feet of drains cleaned, yards of litter removed by street sweepers, etc.

This repository should be able to be adapted to other municipal reports, or, at least the basic methodology. At a minimum, the template file would have to be rewritten to meet whatever your municipality/county/individual reporting requirements are. The DMR parser and graphing utilities are probably the most reusable.

## Ultimate project goals

- [X] Jinja2 template magic produces a passable-looking report in markdown
- [X] Parser for EPA CDX DMRs
- [ ] Automatically generate informative graphs from the water quality data
- [ ] Static site generator creates a page for the report to be used on http://www.littlerock.gov
- [ ] Refactor the scripts to make them more flexible

## FAQ

1. GPL? What are you, a communist?
I would be OK with these scripts being used to help other municipalities with their reporting, but I would be pretty miffed if somebody Zuckerberg'd the code and started selling it to towns at exorbitant cost. Use your powers for good.
2. This is kind of . . . clunky
Yeah. Work in progress. If there is any interest at all, then I will make the scripts more generalized.
3. I want to do this for my city/county/whatever, help!
Call the Public Works and ask for me. I will find a way to make this work for you.
4. Why YAML?
YAML is pretty expressive while still being highly legible. The decision was between one YAML file with all the data or a couple different CSVs. I think it's easier to reason about one (not too large) file rather than about 10 small separate files.
