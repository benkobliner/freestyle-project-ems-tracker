# FDNY EMS Data Explorer

This project uses live FDNY EMS incident data from NYC Open Data to explore patterns in emergency medical demand.

The data comes from the FDNY EMS Incident Dispatch Data dataset:

https://data.cityofnewyork.us/resource/76xm-jjuj.json

## Current Implementation

The current version retrieves a sample of Manhattan EMS incidents directly from the NYC Open Data API and loads the results into a pandas DataFrame.

Future versions will support analysis of:

- EMS call type and geographic patterns
- EMS response times and severity levels
- Daytime versus nighttime EMS demand

## Setup

Install the required packages:

```bash
python3 -m pip install -r requirements.txt
