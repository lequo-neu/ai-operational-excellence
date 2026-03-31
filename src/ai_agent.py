import pandas as pd
import numpy as np
from typing import Dict, List, Any

class AIAnalysisAgent:
    """
    AI Agent for automated operational analysis.
    Performs Pareto analysis, root cause identification, and generates recommendations.
    """
    
    def __init__(self, df, config=None):
        self.df = df
        self.config = config or {}
        self.pareto_threshold = self.config.get("pareto_threshold", 0.8)
    
    def pareto_analysis(self, group_by="process_step", metric="defect_count"):
        """
        Automated Pareto analysis to identify vital few vs trivial many
        """
        grouped = self.df.groupby(group_by)[metric].sum().sort_values(ascending=False)
        total = grouped.sum()
        
        grouped_df = pd.DataFrame({
            "category": grouped.index,
            "value": grouped.values,
            "percentage": (grouped.values / total * 100).round(2),
            "cumulative_percentage": (grouped.values.cumsum() / total * 100).round(2)
        })
        
        vital_few = grouped_df[grouped_df["cumulative_percentage"] <= self.pareto_threshold * 100]
        
        return {
            "pareto_data": grouped_df,
            "vital_few": vital_few,
            "vital_few_count": len(vital_few),
            "total_categories": len(grouped_df)
        }
    
    def detect_anomalies(self, metric="cycle_time_minutes", method="zscore", threshold=3.0):
        """
        Detect statistical anomalies in operational data
        """
        data = self.df[metric].dropna()
        
        if method == "zscore":
            z_scores = np.abs(stats.zscore(data))
            anomalies_idx = np.where(z_scores > threshold)[0]
        elif method == "iqr":
            q1, q3 = data.quantile([0.25, 0.75])
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            anomalies_idx = data[(data < lower) | (data > upper)].index
        else:
            raise ValueError(f"Unknown method: {method}")
        
        anomalies = self.df.iloc[anomalies_idx] if len(anomalies_idx) > 0 else pd.DataFrame()
        
        return {
            "anomaly_count": len(anomalies_idx),
            "anomaly_percentage": round(len(anomalies_idx) / len(data) * 100, 2),
            "anomalies": anomalies,
            "threshold_used": threshold
        }
    
    def root_cause_analysis(self):
        """
        Automated root cause identification using correlation and statistical tests
        """
        high_defect_mask = self.df["defect_count"] > self.df["defect_count"].quantile(0.75)
        high_defect_df = self.df[high_defect_mask]
        
        root_causes = {}
        
        # Analyze by process
        process_defects = high_defect_df.groupby("process_step")["defect_count"].agg(["mean", "count"])
        process_defects["defect_rate"] = (process_defects["mean"] * process_defects["count"]).round(2)
        root_causes["process"] = process_defects.sort_values("defect_rate", ascending=False).head(3)
        
        # Analyze by product line
        product_defects = high_defect_df.groupby("product_line")["defect_count"].agg(["mean", "count"])
        product_defects["defect_rate"] = (product_defects["mean"] * product_defects["count"]).round(2)
        root_causes["product_line"] = product_defects.sort_values("defect_rate", ascending=False)
        
        # Analyze environmental factors
        temp_corr = self.df["temperature_celsius"].corr(self.df["defect_count"])
        humidity_corr = self.df["humidity_percent"].corr(self.df["defect_count"])
        
        root_causes["environmental"] = {
            "temperature_correlation": round(temp_corr, 3),
            "humidity_correlation": round(humidity_corr, 3)
        }
        
        # Equipment analysis
        equipment_defects = high_defect_df.groupby("equipment_id")["defect_count"].agg(["sum", "count"])
        equipment_defects = equipment_defects[equipment_defects["count"] > 10]
        root_causes["equipment"] = equipment_defects.sort_values("sum", ascending=False).head(5)
        
        return root_causes
    
    def generate_strategic_recommendations(self, analysis_results):
        """
        Generate prioritized strategic recommendations based on analysis
        """
        recommendations = []
        
        # Process bottleneck recommendations
        if "bottlenecks" in analysis_results:
            bottlenecks = analysis_results["bottlenecks"]
            for idx, row in bottlenecks.head(3).iterrows():
                recommendations.append({
                    "priority": "HIGH",
                    "category": "Process Optimization",
                    "issue": f"Bottleneck identified in {idx}",
                    "metric": f"Cycle time {row.get('cycle_time_minutes_mean', 0):.1f} min",
                    "recommendation": f"Implement parallel processing or resource reallocation for {idx}",
                    "expected_impact": "15-25% cycle time reduction"
                })
        
        # Quality recommendations
        if "pareto_quality" in analysis_results:
            vital_few = analysis_results["pareto_quality"]["vital_few"]
            for _, row in vital_few.iterrows():
                recommendations.append({
                    "priority": "HIGH",
                    "category": "Quality Control",
                    "issue": f"High defect rate in {row['category']}",
                    "metric": f"{row['percentage']:.1f}% of total defects",
                    "recommendation": f"Conduct FMEA and implement preventive controls for {row['category']}",
                    "expected_impact": "30-40% defect reduction"
                })
        
        # Cost optimization
        if "cost_analysis" in analysis_results:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Cost Reduction",
                "issue": "High operational costs detected",
                "metric": f"Average cost: ${analysis_results['cost_analysis']['avg_cost']:.2f}",
                "recommendation": "Implement predictive maintenance and lean inventory management",
                "expected_impact": "10-15% cost reduction"
            })
        
        # Anomaly alerts
        if "anomalies" in analysis_results and analysis_results["anomalies"]["anomaly_count"] > 0:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "Anomaly Detection",
                "issue": f"{analysis_results['anomalies']['anomaly_count']} anomalies detected",
                "metric": f"{analysis_results['anomalies']['anomaly_percentage']:.2f}% of records",
                "recommendation": "Investigate anomalous patterns and implement real-time monitoring",
                "expected_impact": "Prevent potential quality escapes"
            })
        
        return pd.DataFrame(recommendations)
    
    def generate_executive_summary(self, all_results):
        """
        Generate executive summary for stakeholder reporting
        """
        summary = {
            "total_records_analyzed": len(self.df),
            "analysis_period": f"{self.df['timestamp'].min()} to {self.df['timestamp'].max()}",
            "key_findings": [],
            "critical_issues": 0,
            "high_priority_actions": 0,
            "estimated_savings_potential": "$0"
        }
        
        if "recommendations" in all_results and len(all_results["recommendations"]) > 0:
            recs = all_results["recommendations"]
            summary["critical_issues"] = len(recs[recs["priority"] == "CRITICAL"])
            summary["high_priority_actions"] = len(recs[recs["priority"] == "HIGH"])
        
        return summary

from scipy import stats
