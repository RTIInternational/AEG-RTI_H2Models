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

The Python version updates index.html after running. To view the results, open index.html in a browser.

### R
1. Clone code from this repository to your local machine. Make sure you're on the "main" branch.
2. Install the `renv` package in R: `install.packages("renv")`
3. Set your working directory to the R directory within the main repository
     * If you're on the command line, use the `cd` command: `cd path_to_repository\R\`
     * If you're using RStudio, use the R console to change the directory. The function `getwd()` shows your current directory and `setwd()` allows you to change directories: `setwd("path_to_repository/R/")`
4. Run `renv::restore()` from the R console to set up packages. If prompted, type 'Y' to activate the project. This will set up your local R environment (packages, versioning, etc.) to match the development environment.
5. If this doesn't work, you can always manually install the following packages:
     * renv
     * here
     * import
     * jsonlite [`install.packages('jsonlite', repos = c('https://jeroen.r-universe.dev', 'https://cloud.r-project.org'))`]
     * dplyr
6. Now you're ready to run! This can be done in several ways:
     * **From the command line.** Pick your favorite application for using the terminal. Some options are command prompt (can be accessed via VS Code), gitbash, or the built-in R Terminal. From the R directory, type `Rscript run.R default-smr-natural-gas-no-cc.json` You can input the name of any json in the data\default directory or a sequence of jsons separated by spaces.
     * **From the RStudio editor. Just click 'Source' to run or select lines of code and run with 'ctrl+Enter' Note, you'll need to re-define the variable args, which is set up by default to accept input from the command line. Set args to equal a vector of one or more json names: `args = c('default-autothermal-reforming-natural-gas-with-cc.json')` 

## Tax Credits

### 45Q

> 45Q tax credit gives $85/ton of CO2 sequestered for SMR-CCS

To enable, set `CO2_credit` to `85` in `default-smr-natural-gas-with-cc.json`

### 45V

> 45V is a hydrogen production tax credit of $0.60/kg for the first ten years of operation

To enable, set `dollars_per_kg_h2_10yr_credit` to `0.6`.
