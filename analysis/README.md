# EDA & Visualization

EDA and visualization part for the Predictive Maintenance project using the Wind Farm A SCADA dataset from [Kaggle](https://www.kaggle.com/datasets/azizkasimov/wind-turbine-scada-data-for-early-fault-detection/data).

## File (`analysis.ipynb`)
- Loads the dataset and merges event labels and turbine status names for analysis.
- EDA: summary statistics, distributions, correlation heatmap, power curve, and group-by analysis.
- Visualization: KPIs, monthly wind and power trends, turbine comparisons, temperature boxplots, and an interactive Plotly power curve.

## Main Findings
- ~1.2M readings from 5 turbines over 10 years (11 normal events and 11 anomalies).
- Wind speed and power output have a strong correlation (0.93).
- 75.09% of readings are in normal operating status.
- Turbine 13 has the highest average gearbox temperature (55°C), while Turbine 10 has the lowest average power output.

By: Mostafa Magdy
