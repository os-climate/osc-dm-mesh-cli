
## Datasets

Example datasets that are being considered for use are from:
- [OECD/Organisation for Economic Co-operation and Development](https://www.oecd.org/)
- [RMI/Utility Transition Hub](https://utilitytransitionhub.rmi.org/)
- [PRIMAP](https://www.pik-potsdam.de/paris-reality-check/primap-hist/)
- [WDI](https://databank.worldbank.org/source/world-development-indicators)
- [EDGAR](https://edgar.jrc.ec.europa.eu/)
- [UNFCCC](https://unfccc.int/process-and-meetings/transparency-and-reporting/greenhouse-gas-data/information-on-data-sources)
- [PCAF](someurl)

### PRIMAP

https://doi.org/10.5281/zenodo.10006301

### OECD (New Portal)

OECD offers a new "Data Explorer" which seems to be pretty easy to use
and transform to consumable APIs. To actually get the URL for a CSV
output (most common):
1. Open [OECD Data Explorer](https://data-explorer.oecd.org/)
2. Click on a Topic (for example: Environment)
3. Refine the request using "Filters" (left side of page)
4. Find and click the "Download" button (in middle right above data description)
5. Your should see two options: (a) Filtered data in tabular text (CSV), and,
(b) Unfiltered data in tabular text (CSV)
6. To get your *filtered* data CSV, *right-click* the "Filtered" option to
get the URL (if you are using Chrome, use "Copy Link Address" in the right-click menu)
7. To get all *all* data CSV, *right-click* the "Unfiltered" option to get the URL
8. Use "curl" with the URL to download the data (or you can use the URL
in a python program)

Example curl command to get CSV data (using the "format=csvfilewithlabels" provided at the
end of the URL):
~~~~
curl https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/CAN..PS._T..?startPeriod=2010&endPeriod=2021&dimensionAtObservation=AllDimensions&format=csvfilewithlabels
~~~~

Example curl command to get JSON data (using the "format=jsondata" provided at the
end of the URL):
~~~~
curl https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/CAN..PS._T..?startPeriod=2010&endPeriod=2021&dimensionAtObservation=AllDimensions&format=jsondata
~~~~

About formats...The simplest approach is to use the "format".  According to
the [OECD documentation](https://gitlab.algobank.oecd.org/public-documentation/dotstat-migration/-/raw/main/OECD_Data_API_documentation.pdf):
~~~~
Alternatively, it is possible to use the following non-SDMX standard ‘format’ URL parameter:
• SDMX-ML v2.1 generic data format (obsolete): ‘genericdata’
• SDMX-ML v2.1 structure-specific data format: ‘structurespecificdata’
• SDMX-JSON v2: ‘jsondata’
• SDMX-CSV v1: ‘csv’
• SDMX-CSV v1 as attached file: ‘csvfile’
• SDMX-CSV v1 as attached file including the names of objects in addition to their identifiers:
‘csvfilewithlabels’
~~~~

In the same APi document, the OECD offers other ways to format the
data output using headers:
~~~~
Selection of the Appropriate Representation
Use one of the following values for the ‘Accept’ header for data and reference metadata queries:
• SDMX-ML v2.1 generic data format (obsolete): ‘application/vnd.sdmx.genericdata+xml;
charset=utf-8; version=2.1’
• SDMX-ML v2.1 structure-specific data format:
‘application/vnd.sdmx.structurespecificdata+xml; charset=utf-8; version=2.1’
• SDMX-ML v3 structure-specific data format (experimental):
‘application/vnd.sdmx.structurespecificdata+xml; charset=utf-8; version=3.0’
• SDMX-JSON v1: ‘application/vnd.sdmx.data+json; charset=utf-8; version=1.0’
• SDMX-JSON v2: ‘application/vnd.sdmx.data+json; charset=utf-8; version=2’
• SDMX-CSV v1: ‘application/vnd.sdmx.data+csv; charset=utf-8’
• SDMX-CSV v2: ‘application/vnd.sdmx.data+csv; charset=utf-8; version=2’
For SDMX-CSV, optionally add the settings:
• ‘; labels=both’ to include the names of objects inside the response in addition to their
identifiers.
• ‘timeformat= normalized’ to obtain a pivotable time period format
~~~~

OECD topic/hierarchy include (as of October 2023):
- Agriculture
    - Agricultural output
- Finance
- Jobs
    - Earnings and Wages
    - Employment
    - Unemployment
- Economy
    - Corproate Sector
    - International Trade
    - Leading Indicators
- Government
    - General Government
- Society
    - Demographics
- Environment
    - Air and Climate
    - Biodiversity
    - Enviornmental Policy
    - Water
- Innovation and Technology
    - Broadband Access
    - Entrepreneurship
    - Industry
    - Information and Communication Technology (ICT)
    - Research and Development (R&D)

Canadian population data:
Returns CSV
~~~~
curl https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/CAN.POP.PS._T._T.H\?startPeriod\=2010\&endPeriod\=2021\&dimensionAtObservation\=AllDimensions\&format\=csvfilewithlabels
~~~~

All population data:
Returns CSV
~~~~
curl https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/all?dimensionAtObservation=AllDimensions&format=csvfilewithlabels
~~~~

Other Useful links:
- [Data Explorer - NEW](https://data-explorer.oecd.org/)
- [SDMX Details API Docs](https://gitlab.algobank.oecd.org/public-documentation/dotstat-migration/-/raw/main/OECD_Data_API_documentation.pdf)

### OECD (Old Portal)

The OECD offers an older port but it is being migrated, with an
end of life sometime in 2024.  Nevertheless, here are some
useful links:
- [Data Portal - OLD](https://stats.oecd.org/)
- [JSON API Documentation](https://data.oecd.org/api/sdmx-json-documentation/)
- [API Developer Documenation](https://data.oecd.org/api/)
- [More API Documentation](https://gitlab.algobank.oecd.org/public-documentation/dotstat-migration/-/raw/main/OECD_Data_API_documentation.pdf)
- [Medium Article to use APIs](https://medium.com/@koki_noda/how-to-use-oecd-data-in-python-69a0234c6b27)
- [JSON Example - OLD](https://stats.oecd.org/SDMX-JSON/data/HISTPOP/AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EU27+G20+OECD+WLD+NMEC+ARG+BRA+BGR+CHN+HRV+CYP+IND+IDN+MLT+ROU+RUS+SAU+SGP+ZAF.W+M+T.TOTAL+0_4+05_9+10_14+15_19+20_24+25_29+30_34+35_39+40_44+45_49+50_54+55_59+60_64+65_69+70_74+75_79+80_84+85_OVER+50_OVER+LESS_20+15-64+20-64+65_OVER+LESS_15_SHARE+15-24_SHARE+15-64_SHARE+65_OVER_SHARE+YD_L20+OAD20-64+TOTD20-64/all?startTime=2010&endTime=2022)
- [XML Example - OLD](https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/HISTPOP/AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EU27+G20+OECD+WLD+NMEC+ARG+BRA+BGR+CHN+HRV+CYP+IND+IDN+MLT+ROU+RUS+SAU+SGP+ZAF.W+M+T.TOTAL+0_4+05_9+10_14+15_19+20_24+25_29+30_34+35_39+40_44+45_49+50_54+55_59+60_64+65_69+70_74+75_79+80_84+85_OVER+50_OVER+LESS_20+15-64+20-64+65_OVER+LESS_15_SHARE+15-24_SHARE+15-64_SHARE+65_OVER_SHARE+YD_L20+OAD20-64+TOTD20-64/all?startTime=2010&endTime=2022)
- [Data Explorer - NEW - Query](https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CSociety%23SOC%23&fs[1]=Time%20horizon%2C0%7CHistorical%23H%23&pg=0&fc=Time%20horizon&snb=1&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_POPULATION%40DF_POP_HIST&df[ag]=OECD.ELS.SAE&df[vs]=1.0&pd=2010%2C2021&dq=CAN.POP.PS._T._T.H&ly[cl]=TIME_PERIOD&to[TIME_PERIOD]=false)
- [XML Example - NEW](https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/CAN.POP.PS._T._T.H?startPeriod=2010&endPeriod=2021&dimensionAtObservation=AllDimensions)
- [CSV Example - NEW](https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/CAN.POP.PS._T._T.H?startPeriod=2010&endPeriod=2021&dimensionAtObservation=AllDimensions&format=csvfilewithlabels)

### RMI/Utility Transition Hub

### PCAF

- [OSC GitHub Repo/Code](https://github.com/os-climate/PCAF-sovereign-footprint)
- [OECD Data (from Portal/Export/SDMX)](https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/IO_GHG_2021/FD_CO2+PROD_CO2+BALCO2_FD+FFD_DCO2+DFD_FCO2+FD_PCCO2+PROD_PCCO2+FD_CO2_SH+FFD_DCO2PSH+DFD_FCO2PSH+EXGR_DCO2+EXGR_DCO2PSH+EXGR_FCO2+EXGR_FCO2PSH+EXGR_TCO2+EXGR_TCO2PSH+EXGR_TCO2INT+EXGR_INTDCO2+EXGR_INTDCO2PSH+EXGR_INTFCO2+EXGR_INTFCO2PSH+EXGR_INTTCO2+EXGR_INTTCO2PSH+EXGR_INTTCO2INT+EXGR_FNLDCO2+EXGR_FNLDCO2PSH+EXGR_FNLFCO2+EXGR_FNLFCO2PSH+EXGR_FNLTCO2+EXGR_FNLTCO2PSH+EXGR_FNLTCO2INT+IMGR_DCO2+IMGR_DCO2SH+IMGR_FCO2+IMGR_TCO2+IMGR_TCO2INT+BALCO2_GR+PROD_EFCO2.WLD+OECD+AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+NONOECD+ARG+BRA+BRN+BGR+KHM+CHN+HRV+CYP+IND+IDN+HKG+KAZ+LAO+MYS+MLT+MAR+MMR+PER+PHL+ROU+RUS+SAU+SGP+ZAF+TWN+THA+TUN+VNM+ROW+APEC+ASEAN+EASIA+EU27_2020+EU28+EU15+EU13+EA19+G20+ZEUR+ZASI+ZNAM+ZSCA+ZOTH.WLD+OECD+AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+NONOECD+ARG+BRA+BRN+BGR+KHM+CHN+HRV+CYP+IND+IDN+HKG+KAZ+LAO+MYS+MLT+MAR+MMR+PER+PHL+ROU+RUS+SAU+SGP+ZAF+TWN+THA+TUN+VNM+ROW+APEC+ASEAN+EASIA+EU27_2020+EU28+EU15+EU13+EA19+G20+ZEUR+ZASI+ZNAM+ZSCA+ZOTH+DXD.DTOTAL+D01T03+D01T02+D03+D05T09+D05T06+D07T08+D09+D10T33+D10T12+D13T15+D16T18+D16+D17T18+D19T23+D19+D20T21+D20+D21+D22+D23+D24T25+D24+D25+D26T27+D26+D27+D28+D29T30+D29+D30+D31T33+D35T39+D35+D36T39+D41T43+D45T82+D45T56+D45T47+D49T53+D49+D50+D51+D52+D53+D55T56+D58T63+D58T60+D61+D62T63+D64T66+D68+D69T82+D69T75+D77T82+D84T98+D84T88+D84+D85+D86T88+D90T98+D90T96+D90T93+D94T96+D97T98+D05T39+D41T98+D45T98+D58T82+DINFO+DMHH/all?startTime=1995&endTime=2018)
- [OECD Portal (query takes a long time)](https://stats.oecd.org/Index.aspx?DataSetCode=IO_GHG_2021)
- [UNFCCC Data/Time Series/Annex I](https://di.unfccc.int/time_series)
- [World Bank Data](https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv)
- [PRIMAP Python Libraries](https://github.com/pik-primap)
- [PRIMAP/UNFCCC Python Library](https://unfccc-di-api.readthedocs.io/en/stable/readme.html)

