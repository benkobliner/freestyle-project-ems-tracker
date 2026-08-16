# FDNY EMS Data Explorer

The FDNY EMS Data Explorer is a Python web application that uses live FDNY EMS Incident Dispatch Data from NYC Open Data.

The application allows users to explore geographic and operational patterns in EMS incidents without manually downloading or analyzing the full EMS dataset.

## User Need

FDNY publishes a large amount of historical EMS dispatch data through NYC Open Data. However, the raw dataset contains millions of records and is difficult for users to quickly interpret.

This application allows emergency planners, EMS leaders, public health officials, researchers, and other users to answer specific questions by filtering and summarizing the data.

## Current Analyses

The application currently supports three primary analyses.

### 1. EMS Call Type by ZIP Code

Users can enter an FDNY EMS final call type, such as `DROWN`, and identify which ZIP codes generated the greatest number of those incidents during a selected year.

Example use case:

An EMS Special Operations planner evaluating whether certain ambulances should carry water-rescue equipment could examine the geographic distribution of historical `DROWN` calls.

### 2. EMS Response Time by ZIP Code

Users can compare average incident response times among ZIP codes.

The application can analyze:

- All severity levels
- Final severity levels 1 through 3 only

Only incidents marked by FDNY as having valid incident response time measurements are included.

Users can also specify a minimum number of qualifying calls per ZIP code to prevent very small samples from dominating the results.

Example use case:

An EMS chief could identify areas with longer average response times and determine whether the pattern changes when focusing only on higher-severity incidents.

### 3. Day vs. Night EMS Demand

Users can compare EMS incident volume during daytime and nighttime hours.

For this application:

- Day = 08:00 through 19:59
- Night = 20:00 through 07:59

Example use case:

An EMS operations planner could examine how demand shifts geographically between daytime and nighttime hours.

## Data Source

FDNY EMS Incident Dispatch Data

NYC Open Data dataset ID:

`76xm-jjuj`

SODA API endpoint:

`https://data.cityofnewyork.us/resource/76xm-jjuj.json`

The application uses server-side queries so that NYC Open Data performs much of the filtering and aggregation before returning results. This avoids downloading the complete dataset.

## Installation

Python 3 is required.

Install the project's dependencies:

```bash
python3 -m pip install -r requirements.txt
