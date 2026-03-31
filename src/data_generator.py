import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_operational_data(n_records=15000):
    """
    Generate synthetic pharmaceutical operational data.
    Simulates production, quality, and supply chain processes.
    """
    
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=i) for i in range(n_records)]
    
    processes = ["API Manufacturing", "Formulation", "Filling", "Packaging", 
                 "Quality Control", "Storage", "Distribution"]
    
    sites = ["Site A - Boston", "Site B - New Jersey", "Site C - California"]
    
    product_lines = ["Oncology", "Cardiovascular", "Immunology", "Neurology"]
    
    data = {
        "record_id": range(1, n_records + 1),
        "timestamp": dates,
        "process_step": np.random.choice(processes, n_records),
        "site_location": np.random.choice(sites, n_records),
        "product_line": np.random.choice(product_lines, n_records),
        "batch_id": [f"BATCH-{np.random.randint(1000, 9999)}" for _ in range(n_records)],
        "cycle_time_minutes": np.random.lognormal(4.2, 0.6, n_records),
        "defect_count": np.random.poisson(2, n_records),
        "resource_utilization": np.clip(np.random.normal(0.75, 0.15, n_records), 0.3, 1.0),
        "wait_time_minutes": np.random.exponential(25, n_records),
        "temperature_celsius": np.random.normal(22, 2, n_records),
        "humidity_percent": np.random.normal(45, 5, n_records),
        "operator_id": [f"OP-{np.random.randint(100, 999)}" for _ in range(n_records)],
        "equipment_id": [f"EQ-{np.random.randint(1, 50):03d}" for _ in range(n_records)],
        "yield_percent": np.clip(np.random.normal(94, 4, n_records), 70, 100),
        "rework_required": np.random.choice([0, 1], n_records, p=[0.88, 0.12]),
        "cost_usd": np.random.lognormal(8.5, 1.2, n_records)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce bottlenecks in specific processes
    bottleneck_mask = df["process_step"].isin(["Quality Control", "Filling"])
    df.loc[bottleneck_mask, "cycle_time_minutes"] *= 1.8
    df.loc[bottleneck_mask, "wait_time_minutes"] *= 2.2
    
    # Add quality issues to specific product lines
    quality_issue_mask = df["product_line"] == "Oncology"
    df.loc[quality_issue_mask, "defect_count"] = np.random.poisson(5, quality_issue_mask.sum())
    
    # Add anomalies
    anomaly_idx = np.random.choice(df.index, size=int(0.02 * n_records), replace=False)
    df.loc[anomaly_idx, "cycle_time_minutes"] *= np.random.uniform(3, 5, len(anomaly_idx))
    df.loc[anomaly_idx, "cost_usd"] *= np.random.uniform(2, 4, len(anomaly_idx))
    
    return df

if __name__ == "__main__":
    df = generate_operational_data(15000)
    df.to_csv("/home/claude/handson_project/data/vertex_operations.csv", index=False)
    print(f"Generated {len(df)} operational records")
    print(df.head())
    print(f"\nData shape: {df.shape}")
    print(f"\nColumn types:\n{df.dtypes}")
