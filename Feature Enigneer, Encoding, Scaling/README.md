**Feature Engineering, Encoding & Scaling**
   - **Feature Engineering:** Extracts `hour` and `month` from `time_stamp`, and calculates `temp_diff` (`gearbox_temp - ambient_temp`)
   - **Encoding:** One-hot encodes `status_type_id` (`drop_first=True`) and label-encodes `train_test`
   - **Scaling:** Applies `StandardScaler` to continuous telemetry features (`wind_speed`, `ambient_temp`, `gearbox_temp`, `nacelle_temp`, `power_output`, `temp_diff`)
   - Exports the final ML-ready dataset (`1,196,747 × 17`) to `data/processed/scada_final.csv`