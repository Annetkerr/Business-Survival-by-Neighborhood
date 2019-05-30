# DSI-CC7-San Francisco  -  Capstone Project
# Survival Analysis of Business Lifetimes in San Francisco
### Anne Kerr 

### Problem Statement

Can we use the changing characteristics of San Francisco neighborhoods explain and predict the survival rates of businesses?


<h1>Executive Summary</h1>

<h2>Introduction</h2>
I chose this topic because I wanted to explore the topic of gentrification.  I moved to SF a little over a year ago, and have encountered first hand lot concepts I had not been faced with before: gentrification, displacement, excusion. Wealthy people are moving in and forcing people out. Rent control is supposed to make the city affordable, but does it have the opposite effect? Tech buses regularly shuttle high paid workers up and down the peninsula, making it easier for people to live in the city and commute to work at the big tech giants. There is a common lament that sky-high rents are pushing established businesseses out. Sometimes new businesses take their place. Often, store fronts are left empty.

The issue is very complex and much bigger than can be handled on a three-week capstone projecgt. But, I though, perhaps there is part of this I can begin to explore. My inital thought was to see if I could find an ***unsupervised clustering*** technique use changing characteristics of SF neighborhoods to find natural groupings, then compare them with what we know about the actual neighborhods and see how well they align.

<h2>Methodology</h2>
When reviewing the project with my instructor, however, he introduced the idea of **survival analysis** to predict the lifetime of a business. This turns the question around a bit. Instead of looking at business lifetimes and other characteristics of neighborhoods as a predictors for gentrification, maybe we can find some neighborhood charactistics that could be predictors for business lifetimes. 

This method was appealing in several ways:

-  It is useful
-  It can be treated as a well-defined subset of the bigger questions
-  It is specifically designed to take into account the nature of the primary dataset. Specifically, it knows how to handle censored data. 

What is Survival Analysis and Why is it Needed?  (Reference Johns Hopkins School of Publi Health Lecture Notes>)

It is also called 'time to event' analysis.

It deals with time-to-even datat in the presence of censoring. Specifically, it: 
- takes time into account (duration, or lifetime, from a given start time to an specified event) In this case it is the time from when a business opens to when it closes.
- differentiates between full information and censored information 
    - full information - business has closed prior to the time of interest and we know when it was closed, therefore have complete information about the duration
    - censored information - the business is still open. The duration is the time since it opened until the present, but that is not complete information. This is a type of missing data

Other uses:
-  How long can you retain customers ( churn )
-  How long will a machine last
-  Traditional use - how long will a patient live after a certain diagnosis or a given treatment

Estimating Survival Rates - Kaplan-Meier
-  A non-parametric 

Survival Regression - Accounting for multiple predictor variables in estimating survival times
-  Can't use ordinary linear regression - You would either have to drop the censored subjects as missing data, or underestimate the duration
-  Can't use logistic regression because it can't take into account the time component
-  Can't use time series analysis because you are dealing with different start dates and durations, not calendar time

Survival analysis models takes into account censoring.  For each of your subjects of interest you identify the duration and whether or not the data is censored. 
E.g., Store a was open 10 years, and is now closed.  Store b has been open 4 years and is still open. 

<h2>Conclusions</h2>
Applying survival analysis has shown that there is a relationship between the lifetime of a business and the neighborhood it is in, and that there are certain changing characteristics about neighborhoods that do have predictive value when estimating business lifetimes.

We looked used two survival analysis approaches on two datasets to reach the following conclusions. 

***Kaplan-Meier - Estimating survival rates for specific populations***

We plotted the survival curve for businesses from the registered businesses dataset for all of SF and specific neighborhoods, selected to represent both non-gentrifying and gentrifying census tracts (reference: https://www.urbandisplacement.org/map/sf), and used Statistic logrank_test to show that there is a statistical difference between various neighborhoods.

We used the Cox Proportional Hazards Model to perform survival regression on the the registered businesses dataset and the, neighborhood by quarters dataset, which combined features from the business data and other resource. In both cases we found features with predictive value. 

With the survival regression, when determining whether certain variable can be predictors of the desired outcome, we first define a null hypothesis that states that ***there is no evidence that the data we observe could not happen by chance.*** We also define a threshold (alpha) probability beyond which we will conclude that it is not-likely to observe these results by chance. We measure this with a p-value. 

<h1> Overview of the Data</h1>

Three sources of data were used. Two datasets from the San Francisco Open Data Site (Registered Businesses and Eviction Notices), one dataset from Zillow (monthly median home value per square foot, by neighborhood) and geo location data provided by google and accessed through the geocoding api. The relevant data elements from each dataset (used for this project) are outlined in the following data dictioraries. Complete information about each dataset, as well as other information available from each source, can be obtained by following the links provided.

**Registered Businesses** - This was based on the Registered Businesses data available at __[ San Francisco Open Data](http://www.sfgov.org)__ , aka OpenDataSF, and downloaded using the Socrate API. More details about each of these can be found in the technical report. (here here here insert link) 

 Per the description contained in the metadata: 'This dataset includes the locations of businesses that pay taxes to the City and County of San Francisco. Each registered business may have multiple locations and each location is a single row. The Treasurer & Tax Collector’s Office collects this data through business registration applications, account update/closure forms, and taxpayer filings. .... '  

 Registered Businesses Data Dictionary (after dropping metadata columns, and those not used for analysis)

 | Data Element                      | Data Type   | Description   |
|:----------------------------------|:------------|:--------------|
| business_zip                      | float64     | Zip code             |
| certificate_number                | int64       | Unique Identifier              |
| city                              | object      | City name             |
| dba_name                          | object      | Doing business as name              |
| full_business_address             | object      | Street address - used to look up missing geo coordinates              |
| lic                               | object      | Business license type code              |
| lic_code_description              | object      | Business license type description              |
| location                          | Dictionary   | Geo coordinates and business address              |
| naic_code                         | object      | Industry sector code             |
| naic_code_description             | object      | Industry sector description             |
| neighborhoods_analysis_boundaries | object      | Neighborhood             |
| dba_start                         | object      | Doing business as start date             |
| dba_end                           | object      | Doing business as end date              |
| loc_start                         | object      | Location start date - used for this project as the business start date             |
| loc_end                           | object      | Location end date - used for this project as the business close date             |

 The data was augmented to contain several features. The description and source of additional data is also in the table. In addition data from this dataset was used to create a second dataset for analysis (described below.) 

 **Evictions** - This was based on the Evictions Notices data available at __[San Francisco Open Data](http://www.sfgov.org)__ , aka OpenDataSF, and downloaded using the Socrate API. More details about each of these can be found in the technical report. (here here here insert link) 

 Per the description contained in the metadata: 'Data includes eviction notices filed with the San Francisco Rent Board per San Francisco Administrative Code 37.9(c). A notice of eviction does not necessarily indicate that the tenant was eventually evicted, so the notices below may differ from actual evictions.  

 | Data Element            | Data Type   | Description   |
|:------------------------|:------------|:--------------|
| address                 | object      | Address of eviction property              |
| city                    | object      | City              |
| client_location         | Dictionary     | Geo coordinates and business address               |
| neighborhood            | object      | Neighborhood              |
| zip                     | object      | Zip code              |
| eviction_id             | object      | Unique id              |
| file_date               | object      | Date eviction notice was filed.               |
| lat                     | float64     | Latitude coordiate - extracted from client locaton or derived from address |
| lon                     | float64     | Latitude coordiate - extracted from client locaton or derived from address  |
| year                    | int64       | Derived from file_date              |
| quarter                 | int64       | Derived from file_date               |
| yq                      | object      | Derived from file_date               |


**Median Home Value Per Sq Ft ($)** - This was downloaded from __[Zillow Research](https://www.zillow.com/research/data/)__ as a csv file. Complete details about the methodology for data calculations can be found at their site.

| Data Element   | Data Type   | Description   |
|:---------------|:------------|:--------------|
| RegionID       | int64       | Numeric ID              |
| Neighborhood   | object      | Neighborhood              |
| RegionName     | object      | Neighborhood Alias              |
| City           | object      | City (San Francisco)            |
| State          | object      | State (CA)            |
| Metro          | object      | Metro (San Francisco - Oakland - Hawyard)              |
| CountyName     | object      | County Name (San Francisco)              |
| SizeRank       | int64       | Rank measure of neighborhood by Size             |
| 1996-04        | int64       | Monthly median sales price starting for April 1996 |
|    ...         | int64       |               |
| 2019-03        | int64       | ...through March 2019             |


The final combined dataset used for analysis looked like this:


 | Data Element                      | Data Type   | Description   | Source  |
|:----------------------------------|:------------|:--------------|---------|
| business_zip                      | float64     | Zip code             | Registered Businesses Dataset |
| certificate_number                | int64       | Unique Identifier              |  Registered Businesses Dataset |
| city                              | object      | City name             |  Registered Businesses Dataset |
| dba_name                          | object      | Doing business as name              |  Registered Businesses Dataset |
| full_business_address             | object      | Street address - used to look up missing geo coordinates |  Registered Businesses Dataset |
| lic                               | object      | Business license type code   |  Registered Businesses Dataset |
| lic_code_description              | object      | Business license type description  |   Registered Businesses Dataset |
| location                          | Dictionary   | Geo coordinates and business address  |  Registered Businesses Dataset |
| naic_code                         | object      | Industry sector code  |   Registered Businesses Dataset |
| naic_code_description             | object      | Industry sector description |  Registered Businesses Dataset |
| neighborhoods_analysis_boundaries | object      | Neighborhood  |  Registered Businesses Dataset |
| dba_start                         | object      | Doing business as start date  |  Registered Businesses Dataset |
| dba_end                           | object      | Doing business as end date  |  Registered Businesses Dataset |
| loc_start                         | object      | Location start date - used for this project as the business start date  |  Registered Businesses Dataset |
| loc_end                           | object      | Location end date - used for this project as the business close date  |  Registered Businesses Dataset |
| lat                     | float64     | Latitude coordiate - extracted from client locaton or derived from address | Derived from reg bus or geocoding api |
| lon                     | float64     | Latitude coordiate - extracted from client locaton or derived from address  | Derived from reg bus or geocoding api |
| y_start                 | int64       | Year business started - from location start              | Derived from reg bus  |
| q_start                 | int64       | Quarter business started - from location end              | Derived from reg bus |
| yq_start                | object      | Year-quarter business started - from location end              | Derived from reg bus |
| y_end                   | int64       | Year business ended - from location end               | Derived from reg bus |
| q_end                   | float64     | Quarter business ended - from location end                | Derived from reg bus |
| yq_end                  | object      | Year-quarter business ended - from location end             | Derived from reg bus |
| dur                     | int64       | Duration in quarters between from start to end              | Derived from reg bus |
| status                  | object      | Open or closed              | Derived | Derived from reg bus |
| new_neighborhood        | object      | Neighborhood - as calculated by lookup              | Derived from reg bus or Socrata API lookup |
| neighborhood_size       | object      | Feature created based on number of records in the dataset              | Derived from reg bus|
| size_rank               | int64       | Neighborhood size              | Zillow |
| bus_opened              | int64       | # opened during business start quarter              | Derived from reg bus |
| bus_closed              | int64       | # closed during business start quarter              | Derived from reg bus |
| evictions               | int64       | # evictions filed during business start quarter              | Derived from reg bus |
| med_pr_sqft             | int64       | # median home value for the first month of the business start quarter   | Derived from Zillow |


<h1>Overiew of the Process</h1>

**Getting and Cleaning Data, Feature Engineering** 

Constructing the dataset was a big part of this project. SF Open Data has a wealth of information to mine, and I only began to scratch the surface. With this project, though, I now have a framework upon which to build, and adding data and introducing new modeling techniques should be easier.

The primary dataset I used was the registered businesses data described above. I first stripped out any non-SF businesses. (There were some for surrounding areas.) Because there was a lot of missing location data (lat,lon) I needed to use the geocoding api to attempt to fill in as many coordinates as I could using the business addresses. I had hoped to use these for creating maps to visualize the data geographically (and still plan to in the future) but I also needed them to look up missing neighborhood data. This entire project is keyed on neighborhood so my goal was to fill in as many neighborhoods as possible. Of the 195,200 rows remaining after I removed the non-SF data, I was able to identify neighborhoods for 194,826. 

This involved a lot of trial and error. I used a geopandas geocoding api, which is simple and works reliably in test, but when trying it in a loop (.applying the lookup call to each row of a Pandas DataFrame) I got mixed results. I was first using a free coding service that returned a lot of errors on addresses that it can decode on a one-by-one basis. I realized I was hitting thresholds and being throttled. I put in a sleep to keep it from hitting the server to fast, but even that didn't help. Signing up for a google api key did the trick. It was still an iterative process, but much more reliable. 

A better way to do this, and what I will do in the future, is to create a database of known addresses and coordinates, and when presented with a new one to look up, check the database first. If it is not present I will look it up and then add it to the database for next time. I will also ignore apartment and suite numbers, realizing that the street address will always yield the same results. Finally, I will not attempt to geocode P.O. Boxes (:-])

Having completed this, I added data from the eviction notices data from SF Open Data and the median price data from zillow, as well as creating several new features (duration, neighborhood density) to use in the analysis.



Tools Used:<br><br>
**Socrata API**
The sodapy_dataset_reader import contains a classes that use the __[sodapy library](https://pypi.org/project/sodapy/)__ to interface with the __[Socrata API](https://dev.socrata.com/)__  
Many open data platforms are implemented using the Socrata (or SODA) API, including __[SFData.gov](https://data.sfgov.org/)__, which is used for this project.

Geopandas Geocode module with google geocoding API:  geo = geocode(addr, provider='google', api_key=google_key)

LatLong.py - Class to convert coordinates to SF neighborhoods. Adapted from  https://github.com/dylburger/sf-lat-long-mapper

The Pandas profiler is a utility function that expands on the initial data exploration steps one does when one first loads a new dataset. Code and documentation can be found here: __[Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling)__

**Analysis**

Tools Used:<br><br>
Lifelines Survival Analysis Library
Built on top of Pandas 
• Internal plotting methods 
• Simple and intuitive API 
• Only focus is survival analysis

Two methods used for this project
Kaplan-Meier - Estimating survival rates for specific populations
Cox Proportional Hazards Model - Survival Regression


**This project contains the following folders:**

| Folder  | Contents                                                              |
|---------|-----------------------------------------------------------------------|
| root    | README project overview for GitHub                                    |
| \code   | Jupyter notebooks                                                     |
| \code\lib | Python code - classes and utility functions for import              |
| \data   | Data directory for final data files (directory structure only - temp files not uploaded) |
| \tmp    | Temp directory for iterim data files (directory structure only - temp files not uploaded)
| \images | Graphs and charts in jpg format, pfd of final presentation and technical report        |

**This project contains the following jupyter notebooks:**

Section 1 - Getting Data
-  1.1-Registered-Businessess
-  1.1a-Location-Translation
-  1.1b-Extrat_Lat_Lon_From_Points
-  1.1c-Extract_Lat_Lon_From_Addresses
-  1.1d-Recombine-and-Finalize_Business-Coordinates
-  1.1e-Get-Remaining-Addresses
-  1.2-Eviction-Notices

Section 2 - Data Cleaning and Feature Engineering
-  2.1-Cleaning-and-Modifying-SF-Business_Data
-  2.2-Create-New-Dataset

Section 3 - Analyisis and Conclusions
-  3.1 - Survival-Analysis-All_Businesses
-  3.2 - Survival-Analysis-Younger-Businesses

*note: Zillow data was simply downloaded to .csv, so it doesn't get read until notebook 2.2*



**References**

https://www.census.gov/eos/www/naics/
https://www.urbandisplacement.org/map/sf
https://stats.stackexchange.com/questions/297740/what-is-the-difference-between-the-different-residuals-in-survival-analysis-cox
http://myweb.uiowa.edu/pbreheny/7210/f15/notes/11-10.pdf
http://www.statsmodels.org/stable/duration.html
http://ocw.jhsph.edu/courses/StatisticalReasoning2/PDFs/2009/StatR2_lec10a_mcgready.pdf
http://ocw.jhsph.edu/courses/StatisticalReasoning1/PDFs/Lecture7.pdf
https://towardsdatascience.com/survival-analysis-intuition-implementation-in-python-504fde4fcf8e
http://www.bdkeller.com/writing/hunger-games-survival-analysis
https://pypi.org/project/sodapy/
https://www.zillow.com/research/data/
https://datasf.org/opendata/
https://buildmedia.readthedocs.org/media/pdf/lifelines/stable/lifelines.pdf



