# Does National Wealth Predict Athletic Success?

**Setup:**

Requirements

  Python 3.12
  
  Install dependencies:
  
    pip install pandas scipy matplotlib seaborn
  
No environment file! Just install these dependencies and download the necessary data from the report document

**Data File Structure:**
```
data/
├── Olympic_Medal_Tally_History.csv\
├── team_appearances.csv
├── gdp_data/
│   └── API_NY.GDP.MKTP.CD_DS2_en_csv_v2_234.csv
├── gdp_percap_data/
│   └── API_NY.GDP.PCAP.CD_DS2_en_csv_v2_33610.csv
└── pop_data/
    └── API_SP.POP.TOTL_DS2_en_csv_v2_33112.csv
```
WorldBank data may have different number suffixes, so you'll have to change the file names accordingly in the
files that load data

**Files:**

- code/data_processor.py - Handles the loading of datafiles into Pandas Dataframes, and creates necessary scoring columns for analysis
- code/merging.py - Merges the Dataframes created by the functions in data_processor. Each sport's data is merged with the 3 WorldBank datasets
  using a dict to standardize the country names across the datasets
- code/eda.py - Gets the necessary data and visualizations for the EDA portion of the Assignment
- code/analysis.py - Gets the necessary data for the final portion of the project. Primarily correlation coefficients and p values

**Running the Project**
The project is primarily ran in both eda.py and analysis.py, while the other 2 code files provide the necessary functions to support those files

eda.py - 
```
cd code
python eda.py
```

analysis.py - 
```
cd code
python analysis.py
```
