# Manhattan EMS Map

This project creates a simple map of EMS calls in Manhattan.

## Setup

Create and activate an Anaconda environment:

```bash
conda create -n ems-map python=3.11
conda activate ems-map
```

Install the packages:

```bash
pip install -r requirements.txt
```

No API keys or environment variables are required.

## Run

```bash
python main.py
```

This reads `sample_ems_calls.csv`, keeps Manhattan rows, and creates `ems_map.html`.
Open `ems_map.html` in a browser to see the map.

To use another dataset, replace `sample_ems_calls.csv` with a CSV containing these columns:

- `borough`
- `latitude`
- `longitude`

## Test

```bash
pytest
```

GitHub Actions also runs the tests automatically whenever code is pushed to GitHub.
