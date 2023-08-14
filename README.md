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
     * **From the RStudio editor.** Just click 'Source' to run or select lines of code and run with 'ctrl+Enter'. To run, you'll have to set 2 variables manually in the flagged section of code (look for USER INPUTS and a bunch of ###s). The user should point the code to the inputs sheet (described below) and set a name for the file that will contain the output data. These pointers should include directory structures and file-type suffixes, as in the example below:

       `input_filename = "./parameters/parameters_example.csv"`
       
       `output_filename = "sample_results.csv"`

     Sample parameters sheets are included in the repository
* **Editing the parameters sheet.** Two example parameter sheets are included in the repository by default.
    * `R/parameters/parameters_default.csv` - This sheet will just run the default versions of each of the five models with no modifications.
    * `R/parameters/parameters_example.csv` (see image below) - This is an example showing how to make changes to parameters. Using this sheet will run the SMR-with-CC model 6 times with several combinations of parameters.
Column A in the spreadsheet, titled 'baseline' will indicate the default model configuration to use, i.e. the model starting point. This should be one of the 5 default model types (without .json extension):
      * 'default-autothermal-reforming-natural-gas-with-cc'
      * 'default-pem-electrolysis'
      * 'default-smr-natural-gas-no-cc'
      * 'default-smr-natural-gas-with-cc'
      * 'default-solid-oxide-electrolysis'

![example input sheet](https://i.imgur.com/3IpWTch.png)

Each additional column will give the user the option to modify an additional input parameter. For example, in the example shown above, the user chooses to test several different combinations of the variables `dollars_per_kg_h2_10yr_credit` and `CO2_Capture_Efficiency.` In each row, enter the new parameter value that will overwrite the model default. For example, the first row indicates that the SMR-CCS model should be run with a tax credit of 10 cents per kilogram and a capture efficiency of 90%. Note that the user can enter "default" or "Default" in any cell to revert to the default value given for the model.

## Tax Credits

### 45Q

> 45Q tax credit gives $85/ton of CO2 sequestered for SMR-CCS

To enable, set `CO2_credit` to `85` in `default-smr-natural-gas-with-cc.json`

### 45V

> 45V is a hydrogen production tax credit of $0.60/kg for the first ten years of operation

To enable, set `dollars_per_kg_h2_10yr_credit` to `0.6`.
