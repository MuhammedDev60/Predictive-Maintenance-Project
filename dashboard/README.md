[README.md](https://github.com/user-attachments/files/35103599/README.md)
# Wind Turbine Performance Monitoring Dashboard

A Plotly/Dash dashboard for exploring the team's **cleaned Wind Farm A SCADA data**. This is Mossab's dashboard component of the graduation project. It uses the existing cleaned dataset and **does not** re-run preprocessing, train a model, or modify the database.

## 1. Project folder structure

Keep the dashboard and cleaned CSV in the following locations:

```text
Graduation_Project/
├── data/
│   └── processed/
│       └── scada_clean.csv
└── dashboard/
    ├── app.py
    ├── requirements-dashboard.txt
    └── README.md
```

**Important:** The CSV must be at `data/processed/scada_clean.csv` **relative to the project root**, which is the folder containing both `data` and `dashboard`. The CSV is supplied by the team's existing data-preparation work; it is not included in the GitHub handoff ZIP.

## 2. Run the dashboard with Anaconda Prompt (Windows)

Open **Anaconda Prompt**. Run the following three commands **one at a time**.

**Command 1 — Go to your project root.** Replace the example path with the location of the folder containing `dashboard` **and** `data` on your computer:

```bat
cd /d "C:\path\to\Graduation_Project"
```

For example, if the `dashboard` folder is directly on `C:\Users\IT\Desktop\dashboard`, the project root is `C:\Users\IT\Desktop`, and the cleaned CSV must be at `C:\Users\IT\Desktop\data\processed\scada_clean.csv`:

```bat
cd /d "C:\Users\IT\Desktop"
```

**Command 2 — Install the required libraries:**

```bat
python -m pip install -r dashboard\requirements-dashboard.txt
```

**Command 3 — Start the dashboard:**

```bat
python dashboard\app.py
```

Open **http://127.0.0.1:8050/** in your browser (or use the address displayed in Anaconda Prompt). **Leave Anaconda Prompt open** while using the dashboard. Press `Ctrl + C` in the prompt to stop it.

> If you work in a separate Conda environment, activate that environment **before** Commands 2 and 3. Creating a new environment is not required by this dashboard.

## 3. Dashboard features

**KPI cards:**
- Number of SCADA readings
- Number of distinct turbines
- Average power output
- Average wind speed
- Average gearbox temperature

**Interactive filters:**
- Turbine ID
- Date range (inclusive)
- Turbine status
- Train/prediction data split

**Plotly charts:**
- Average power by month
- Average power by turbine
- Distribution of SCADA readings by status
- Average power by wind-speed band

Changing the filters updates the KPI cards and charts.

## 4. Notes on interpretation

- SCADA reading counts are **not** counts of confirmed turbine failures.
- Measurement labels say **source units** because this dashboard does not assume engineering units not established in the provided source documentation.
- The wind-speed bands follow the team's existing notebook analysis.
- Empty filter results are handled by the application.

## 5. Troubleshooting

- **`The system cannot find the path specified`**: Check the folder location in Command 1. The example path must be replaced with your real project path.
- **`FileNotFoundError: ... scada_clean.csv`**: Confirm that `data/processed/scada_clean.csv` exists alongside `dashboard/` under the same project root.
- **`ModuleNotFoundError: No module named 'dash'`**: Run Command 2 with the same Python/Conda environment used in Command 3.
- **Port 8050 is already in use**: Stop any previous instance of the dashboard with `Ctrl + C` before starting another.

## 6. Team / GitHub integration

Commit the `dashboard/` folder to the team's existing project repository. The team must provide the cleaned CSV separately at the documented path. Do not upload an Anaconda environment or repeat the notebook's preprocessing as part of this dashboard component.
