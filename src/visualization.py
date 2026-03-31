import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

class OperationalDashboard:
    def __init__(self, df):
        self.df = df
        self.colors = {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "warning": "#d62728",
            "info": "#9467bd"
        }
    
    def create_pareto_chart(self, pareto_data):
        """
        Create professional Pareto chart
        """
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(
                x=pareto_data["category"],
                y=pareto_data["value"],
                name="Count",
                marker_color=self.colors["primary"]
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=pareto_data["category"],
                y=pareto_data["cumulative_percentage"],
                name="Cumulative %",
                mode="lines+markers",
                marker=dict(size=8, color=self.colors["warning"]),
                line=dict(width=3)
            ),
            secondary_y=True
        )
        
        fig.add_hline(y=80, line_dash="dash", line_color="red", 
                      annotation_text="80% Threshold", secondary_y=True)
        
        fig.update_layout(
            title="Pareto Analysis: Defect Distribution",
            xaxis_title="Process Step",
            height=500,
            hovermode="x unified",
            template="plotly_white"
        )
        
        fig.update_yaxes(title_text="Defect Count", secondary_y=False)
        fig.update_yaxes(title_text="Cumulative Percentage", secondary_y=True)
        
        return fig
    
    def create_bottleneck_heatmap(self):
        """
        Create heatmap showing process bottlenecks
        """
        pivot = self.df.pivot_table(
            values="cycle_time_minutes",
            index="process_step",
            columns="site_location",
            aggfunc="mean"
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="RdYlGn_r",
            text=pivot.values.round(1),
            texttemplate="%{text} min",
            textfont={"size": 10},
            colorbar=dict(title="Avg Cycle Time (min)")
        ))
        
        fig.update_layout(
            title="Process Bottleneck Analysis by Site",
            xaxis_title="Site Location",
            yaxis_title="Process Step",
            height=500,
            template="plotly_white"
        )
        
        return fig
    
    def create_kpi_cards(self, metrics):
        """
        Create KPI summary cards
        """
        fig = go.Figure()
        
        kpis = [
            {"title": "Avg Cycle Time", "value": f"{metrics.get('avg_cycle_time', 0):.1f} min", "delta": "-12%"},
            {"title": "Defect Rate", "value": f"{metrics.get('defect_rate', 0):.2f}%", "delta": "+5%"},
            {"title": "OEE", "value": f"{metrics.get('oee', 0)*100:.1f}%", "delta": "+8%"},
            {"title": "Cost per Unit", "value": f"${metrics.get('avg_cost', 0):.2f}", "delta": "-7%"}
        ]
        
        fig = make_subplots(
            rows=1, cols=4,
            subplot_titles=[kpi["title"] for kpi in kpis],
            specs=[[{"type": "indicator"}] * 4]
        )
        
        for i, kpi in enumerate(kpis, 1):
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=float(kpi["value"].replace("$", "").replace("%", "").replace(" min", "")),
                    delta={"reference": 100, "valueformat": ".1f"},
                    domain={"x": [0, 1], "y": [0, 1]}
                ),
                row=1, col=i
            )
        
        fig.update_layout(height=200, template="plotly_white")
        
        return fig
    
    def create_quality_control_chart(self):
        """
        Create control chart for quality monitoring
        """
        process_stats = self.df.groupby("process_step")["defect_count"].agg(["mean", "std"])
        
        fig = go.Figure()
        
        for process in process_stats.index:
            process_data = self.df[self.df["process_step"] == process]["defect_count"]
            
            fig.add_trace(go.Scatter(
                y=process_data,
                mode="markers",
                name=process,
                marker=dict(size=5)
            ))
        
        mean_val = self.df["defect_count"].mean()
        std_val = self.df["defect_count"].std()
        
        fig.add_hline(y=mean_val, line_dash="dash", line_color="green", 
                      annotation_text="Mean")
        fig.add_hline(y=mean_val + 3*std_val, line_dash="dash", line_color="red",
                      annotation_text="UCL (3σ)")
        fig.add_hline(y=max(0, mean_val - 3*std_val), line_dash="dash", line_color="red",
                      annotation_text="LCL (3σ)")
        
        fig.update_layout(
            title="Quality Control Chart: Defect Monitoring",
            yaxis_title="Defect Count",
            xaxis_title="Observation",
            height=500,
            template="plotly_white"
        )
        
        return fig
    
    def create_cost_distribution(self):
        """
        Create cost distribution analysis
        """
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Cost by Process", "Cost Distribution"),
            specs=[[{"type": "bar"}, {"type": "box"}]]
        )
        
        cost_by_process = self.df.groupby("process_step")["cost_usd"].mean().sort_values(ascending=True)
        
        fig.add_trace(
            go.Bar(
                y=cost_by_process.index,
                x=cost_by_process.values,
                orientation="h",
                marker_color=self.colors["info"]
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Box(
                y=self.df["cost_usd"],
                name="Cost Distribution",
                marker_color=self.colors["secondary"]
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            height=500,
            showlegend=False,
            template="plotly_white"
        )
        
        return fig
    
    def create_trend_analysis(self):
        """
        Create time-series trend analysis
        """
        daily_metrics = self.df.groupby(pd.Grouper(key="timestamp", freq="D")).agg({
            "cycle_time_minutes": "mean",
            "defect_count": "sum",
            "cost_usd": "mean"
        }).reset_index()
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=("Cycle Time Trend", "Daily Defects", "Cost Trend"),
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Scatter(x=daily_metrics["timestamp"], y=daily_metrics["cycle_time_minutes"],
                      mode="lines", name="Cycle Time", line=dict(color=self.colors["primary"])),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=daily_metrics["timestamp"], y=daily_metrics["defect_count"],
                      mode="lines+markers", name="Defects", line=dict(color=self.colors["warning"])),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=daily_metrics["timestamp"], y=daily_metrics["cost_usd"],
                      mode="lines", name="Cost", line=dict(color=self.colors["success"])),
            row=3, col=1
        )
        
        fig.update_layout(height=800, showlegend=False, template="plotly_white")
        
        return fig
