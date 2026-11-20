# 5 Key Insights – Wind Turbine SCADA Data

## Project Overview
This notebook analyzes Wind Farm A SCADA readings from the **Wind Turbine SCADA Data for Early Fault Detection** dataset. It loads event information, feature descriptions, and SCADA readings, prepares selected variables, stores the data in SQLite, and develops five data-driven insights.

## Scope
This notebook focuses on five key insights. For each insight, it presents:
- **Finding:** the result calculated from the dataset.
- **Meaning:** what the result indicates.
- **Suggested Action:** a practical follow-up to consider.

## The Five Insights

1. **Highest Average Gearbox Temperature**  
   Groups SCADA readings by `asset_id` and identifies the asset with the highest average `gearbox_temp`.

2. **Lowest Average Power Output**  
   Uses the asset-level summary to identify the asset with the lowest average `power_output`.

3. **Operating Status with Lowest Average Power Output**  
   Groups readings by `status_type_id` and identifies the status with the lowest average `power_output`. The notebook maps status IDs to the labels Normal, Derated, Idling, Service, Downtime, and Other.

4. **Strongest Correlation Between Measurements**  
   Calculates the correlation matrix for `wind_speed`, `ambient_temp`, `wind_direction`, `gearbox_temp`, `nacelle_temp`, and `power_output`, then identifies the pair with the strongest absolute correlation. Correlation does not prove causation.

5. **Event with Highest Average Gearbox Temperature**  
   Calculates average `gearbox_temp` by `event_id`, joins the event description, and identifies the event group with the highest average.

The findings are calculated when the notebook is run; the specific values depend on the dataset returned at runtime.

## Notebook Workflow
1. Install and import the required Python libraries.
2. Load `comma_event_info.csv` and `comma_feature_description.csv` from the dataset.
3. Load the SCADA files listed by the event IDs and retain the selected columns.
4. Save raw CSV copies and inspect the data using shape, data types, descriptive statistics, and missing-value checks.
5. Fill missing event descriptions with `Normal`, rename selected sensor columns, and convert timestamp columns to datetime.
6. Visualize selected variables with boxplots and clip outliers in `wind_speed` and `power_output` using the IQR bounds.
7. Save the processed CSV files and a data dictionary.
8. Create a SQLite database, define the tables, and load the status, event, feature, and SCADA data.
9. Run SQL queries for event counts, status counts, asset performance, temperature summaries, wind bands, high-temperature readings, train/test groups, and monthly readings.
10. Calculate and display the five key insights, then export their summary to CSV.

## Dataset
**Wind Turbine SCADA Data for Early Fault Detection**  
https://www.kaggle.com/datasets/azizkasimov/wind-turbine-scada-data-for-early-fault-detection

The notebook uses `kagglehub` to load the dataset files. The dataset is not included with these files.

## Libraries and Tools
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SQLite3
- KaggleHub
- Jupyter Notebook / Google Colab

## How to Run
1. Open `5_Key_Insights.ipynb` in Google Colab or Jupyter Notebook.
2. Run the cells in order.
3. Ensure internet access is available for `kagglehub` to retrieve the dataset.
4. If Kaggle requests authentication or dataset access, complete the required Kaggle setup.
5. After successful execution, the notebook saves the five-insight summary to `data/processed/youmna_5_key_insights.csv`.

## Main Output
The final output is a table with five rows and the columns:
- `Insight`
- `Finding`
- `Meaning`
- `Suggested Action`

It is displayed in the notebook and exported as `data/processed/youmna_5_key_insights.csv`.
