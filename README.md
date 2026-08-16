# FDNY EMS Data Explorer

The FDNY EMS Data Explorer is a Python web application that uses live FDNY EMS Incident Dispatch Data from NYC Open Data.

The application allows users to explore geographic and operational patterns in EMS incidents without manually downloading or analyzing the full EMS dataset.

## User Need

FDNY publishes a large historical EMS dispatch dataset through NYC Open Data. However, the raw dataset contains millions of records and is difficult for users to quickly interpret.

This application allows EMS leaders, emergency planners, public health officials, researchers, and other users to answer specific operational questions by filtering and summarizing the data.

## Current Analyses

The application currently supports three primary analyses.

### 1. EMS Call Type by ZIP Code

Users can enter an FDNY EMS final call type, such as `DROWN`, and identify which ZIP codes generated the greatest number of those incidents during a selected year.

The analysis displays:

- Total matching EMS incidents
- Number of matching incidents by ZIP code
- A ranked table of ZIP codes
- A bar chart of the highest-volume ZIP codes

#### Example Use Case

An EMS Special Operations planner evaluating whether selected ambulances should carry specialized water-rescue equipment could examine the geographic distribution of historical `DROWN` calls.

The application does not make a deployment or equipment recommendation. Instead, it provides historical data that can support further operational planning.

### 2. EMS Response Time by ZIP Code

Users can compare average EMS incident response times among ZIP codes.

The analysis can include:

- All severity levels
- Final severity levels 1 through 3 only

Only incidents that FDNY identifies as having valid incident response-time measurements are included.

Users can also select a minimum number of qualifying calls per ZIP code. This prevents ZIP codes with very small samples from disproportionately influencing the ranking.

The analysis displays:

- Average response time by ZIP code
- Number of qualifying incidents
- A ranked table of ZIP codes
- A bar chart showing ZIP codes with the longest average response times

#### Example Use Case

An EMS chief could identify geographic areas with longer average response times and then determine whether the pattern changes when the analysis is restricted to higher-severity incidents.

This can help distinguish between overall system performance and performance for more urgent calls.

### 3. Held EMS Incidents by ZIP Code

Users can examine the geographic distribution of EMS incidents marked as held in the FDNY EMS Incident Dispatch Data.

The analysis displays:

- Total qualifying EMS incidents
- Number of incidents marked as held
- Percentage of incidents marked as held
- Held percentage by ZIP code
- A ranked table of ZIP codes
- A bar chart showing ZIP codes with the highest held percentages

Users can analyze:

- All severity levels
- Final severity levels 1 through 3 only

Users can also set a minimum number of qualifying incidents per ZIP code to reduce the influence of very small sample sizes.

#### Example Use Case

An EMS chief or operations planner could use the analysis to identify geographic areas in which a relatively large share of EMS incidents are marked as held and determine whether the pattern changes when focusing on higher-severity calls.

#### Important Interpretation Note

The NYC Open Data dataset exposes `HELD_INDICATOR` as a Y/N field. The public dataset metadata does not provide a detailed operational definition explaining the specific circumstances that cause an incident to receive a held designation.

For that reason, this application reports the field descriptively as an incident being "marked as held." It does not assume that held status necessarily means that an incident was waiting specifically because no ambulance was available or assign another operational cause without additional documentation.

## Data Source

The application uses:

**FDNY EMS Incident Dispatch Data**

NYC Open Data dataset ID:

`76xm-jjuj`

SODA API endpoint:

`https://data.cityofnewyork.us/resource/76xm-jjuj.json`

The dataset includes information such as:

- Incident date and time
- Initial and final EMS call type
- Initial and final severity level
- Borough
- ZIP code
- Dispatch response time
- Incident response time
- Travel time
- Held indicator

The application uses NYC Open Data's SODA API to query the dataset directly rather than storing the complete dataset locally.

Server-side filtering and aggregation allow NYC Open Data to process much of the underlying data before returning summarized results to the application.

## Application Structure

The project separates the user interface from the data-retrieval and analysis functions.

- `app.py` contains the Streamlit web application and user interface.
- `main.py` contains NYC Open Data API queries and data-processing functions.
- `test_main.py` contains automated Pytest tests.
- `requirements.txt` lists required Python packages.
- `README.md` contains project documentation.

## Installation

Python 3 is required.

From the project directory, install the required packages:

```bash
python3 -m pip install -r requirements.txt
