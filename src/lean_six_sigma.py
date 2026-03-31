import pandas as pd
import numpy as np
from scipy import stats

class LeanSixSigmaAnalyzer:
    def __init__(self, df):
        self.df = df
        self.metrics = {}
    
    def calculate_dpmo(self, defect_col="defect_count", opportunity_col=None):
        """
        Calculate Defects Per Million Opportunities
        """
        total_defects = self.df[defect_col].sum()
        total_units = len(self.df)
        opportunities_per_unit = 1 if not opportunity_col else self.df[opportunity_col].mean()
        
        dpmo = (total_defects / (total_units * opportunities_per_unit)) * 1_000_000
        sigma_level = self._dpmo_to_sigma(dpmo)
        
        self.metrics["dpmo"] = dpmo
        self.metrics["sigma_level"] = sigma_level
        return {"DPMO": dpmo, "Sigma_Level": sigma_level}
    
    def _dpmo_to_sigma(self, dpmo):
        """Convert DPMO to Sigma level"""
        if dpmo <= 3.4:
            return 6.0
        elif dpmo <= 233:
            return 5.0
        elif dpmo <= 6210:
            return 4.0
        elif dpmo <= 66807:
            return 3.0
        else:
            return 2.0
    
    def process_capability_analysis(self, metric_col="yield_percent", 
                                    lsl=90, usl=100):
        """
        Calculate Cp, Cpk for process capability
        """
        data = self.df[metric_col].dropna()
        mean = data.mean()
        std = data.std()
        
        cp = (usl - lsl) / (6 * std) if std > 0 else 0
        cpk = min((usl - mean) / (3 * std), (mean - lsl) / (3 * std)) if std > 0 else 0
        
        self.metrics["cp"] = cp
        self.metrics["cpk"] = cpk
        
        return {"Cp": cp, "Cpk": cpk, "Mean": mean, "Std": std}
    
    def identify_bottlenecks(self, threshold_multiplier=1.5):
        """
        Identify process bottlenecks using cycle time analysis
        """
        process_stats = self.df.groupby("process_step").agg({
            "cycle_time_minutes": ["mean", "std", "count"],
            "wait_time_minutes": "mean",
            "resource_utilization": "mean"
        }).round(2)
        
        process_stats.columns = ["_".join(col).strip() for col in process_stats.columns]
        
        overall_mean = self.df["cycle_time_minutes"].mean()
        process_stats["bottleneck_score"] = (
            process_stats["cycle_time_minutes_mean"] / overall_mean
        )
        
        bottlenecks = process_stats[
            process_stats["bottleneck_score"] > threshold_multiplier
        ].sort_values("bottleneck_score", ascending=False)
        
        return bottlenecks
    
    def value_stream_mapping(self):
        """
        Calculate value-added vs non-value-added time
        """
        vsm = self.df.groupby("process_step").agg({
            "cycle_time_minutes": "mean",
            "wait_time_minutes": "mean"
        })
        
        vsm["total_time"] = vsm["cycle_time_minutes"] + vsm["wait_time_minutes"]
        vsm["value_added_ratio"] = (
            vsm["cycle_time_minutes"] / vsm["total_time"]
        ).round(3)
        vsm["waste_percentage"] = (
            (1 - vsm["value_added_ratio"]) * 100
        ).round(1)
        
        return vsm.sort_values("waste_percentage", ascending=False)
    
    def fishbone_root_cause_data(self, defect_threshold=3):
        """
        Prepare data for root cause analysis (Ishikawa diagram)
        """
        high_defect_records = self.df[self.df["defect_count"] >= defect_threshold]
        
        categories = {
            "Process": high_defect_records.groupby("process_step").size().to_dict(),
            "Product": high_defect_records.groupby("product_line").size().to_dict(),
            "Location": high_defect_records.groupby("site_location").size().to_dict(),
            "Equipment": high_defect_records.groupby("equipment_id").size().nlargest(10).to_dict()
        }
        
        return categories
    
    def calculate_oee(self):
        """
        Calculate Overall Equipment Effectiveness
        """
        availability = (self.df["resource_utilization"].mean())
        performance = (self.df["yield_percent"].mean() / 100)
        quality = 1 - (self.df["rework_required"].mean())
        
        oee = availability * performance * quality
        
        return {
            "Availability": availability,
            "Performance": performance,
            "Quality": quality,
            "OEE": oee
        }
