from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class OperationalRecord(Base):
    __tablename__ = "operational_records"
    
    record_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    process_step = Column(String(100), nullable=False)
    site_location = Column(String(100), nullable=False)
    product_line = Column(String(100), nullable=False)
    batch_id = Column(String(50), nullable=False)
    cycle_time_minutes = Column(Float, nullable=False)
    defect_count = Column(Integer, nullable=False)
    resource_utilization = Column(Float, nullable=False)
    wait_time_minutes = Column(Float, nullable=False)
    temperature_celsius = Column(Float)
    humidity_percent = Column(Float)
    operator_id = Column(String(50))
    equipment_id = Column(String(50))
    yield_percent = Column(Float)
    rework_required = Column(Boolean)
    cost_usd = Column(Float)

class DatabaseManager:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def load_csv_to_db(self, csv_path):
        df = pd.read_csv(csv_path)
        df.to_sql("operational_records", self.engine, if_exists="replace", index=False)
        return len(df)
    
    def execute_query(self, query):
        return pd.read_sql_query(query, self.engine)

# Analytical SQL queries
QUERIES = {
    "process_bottlenecks": """
        SELECT 
            process_step,
            COUNT(*) as record_count,
            AVG(cycle_time_minutes) as avg_cycle_time,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY cycle_time_minutes) as p95_cycle_time,
            AVG(wait_time_minutes) as avg_wait_time,
            AVG(resource_utilization) as avg_utilization
        FROM operational_records
        GROUP BY process_step
        ORDER BY avg_cycle_time DESC
    """,
    
    "quality_defects_by_line": """
        SELECT 
            product_line,
            COUNT(*) as total_batches,
            SUM(defect_count) as total_defects,
            AVG(defect_count) as avg_defects_per_batch,
            SUM(CASE WHEN rework_required = 1 THEN 1 ELSE 0 END) as rework_count,
            AVG(yield_percent) as avg_yield
        FROM operational_records
        GROUP BY product_line
        ORDER BY avg_defects_per_batch DESC
    """,
    
    "site_performance": """
        SELECT 
            site_location,
            COUNT(*) as operations,
            AVG(cycle_time_minutes) as avg_cycle_time,
            AVG(cost_usd) as avg_cost,
            SUM(defect_count) as total_defects,
            AVG(resource_utilization) as avg_utilization
        FROM operational_records
        GROUP BY site_location
        ORDER BY avg_cost DESC
    """,
    
    "equipment_efficiency": """
        SELECT 
            equipment_id,
            COUNT(*) as usage_count,
            AVG(cycle_time_minutes) as avg_cycle_time,
            SUM(defect_count) as total_defects,
            AVG(yield_percent) as avg_yield
        FROM operational_records
        GROUP BY equipment_id
        HAVING COUNT(*) > 100
        ORDER BY total_defects DESC
        LIMIT 20
    """
}
