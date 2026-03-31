import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
DOCS_DIR = BASE_DIR / "docs"

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "vertex_ops",
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "")
}

AI_AGENT_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.2,
    "max_tokens": 2000,
    "pareto_threshold": 0.8,
    "anomaly_zscore": 3.0
}

PROCESS_MAPPING_CONFIG = {
    "bottleneck_threshold": 1.5,
    "cycle_time_percentile": 0.95,
    "quality_defect_threshold": 0.03
}

LEAN_SIX_SIGMA_METRICS = {
    "defects_per_million_opportunities": 3.4,
    "process_capability_target": 1.33,
    "lead_time_reduction_target": 0.25
}

REPORTING_CONFIG = {
    "refresh_interval_minutes": 15,
    "alert_threshold_deviation": 0.15,
    "dashboard_export_format": "pdf"
}
