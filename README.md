# Hydrogen Analysis (H2A) Python and R packages

## Running

H2A can be run in Python or R. See instructions below for each.

### Python

Pre-req: pipenv

```bash
python -m pip install pipenv
```

You may also need to set PATH via Control Panel in Windows.

Installing dependencies:

```bash
pipenv install
```

Running:
  
```bash
pipenv run python py/run.py
```

### R

Pre-req: renv

Installing dependencies:

```R
cd R/
renv::restore()
```

Running:
  
```bash
Rscript R/run.R
```

## Tax Credits

### 45Q

> 45Q tax credit gives $85/ton of CO2 sequestered for SMR-CCS

To enable, set `CO2_credit` to `85` in `default-smr-natural-gas-with-cc.json`

### 45V

> 45V is a hydrogen production tax credit of $0.60/kg for the first ten years of operation

To enable, set `dollars_per_kg_h2_10yr_credit` to `0.6`.
