"""
Interactive HTML Visualizations Generator
Creates Plotly-based interactive charts that can be opened in browser
"""

import sys
sys.path.append('../src')

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from data_generator import generate_operational_data
from lean_six_sigma import LeanSixSigmaAnalyzer
from ai_agent import AIAnalysisAgent

print("Loading data...")
try:
    df = pd.read_csv('../data/vertex_operations.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print(f"Loaded {len(df)} records from existing file")
except:
    print("Generating new data...")
    df = generate_operational_data(15000)
    df.to_csv('../data/vertex_operations.csv', index=False)
    print(f"Generated {len(df)} new records")

# Initialize analyzers
lss = LeanSixSigmaAnalyzer(df)
agent = AIAnalysisAgent(df)

# Color scheme
colors = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'info': '#9467bd'
}

print("\nGenerating interactive visualizations...")

# 1. KPI Dashboard
print("1. Creating KPI dashboard...")
kpi_metrics = {
    'avg_cycle_time': df['cycle_time_minutes'].mean(),
    'defect_rate': (df['defect_count'].sum() / len(df)) * 100,
    'oee': lss.calculate_oee()['OEE'],
    'avg_cost': df['cost_usd'].mean()
}

fig_kpi = make_subplots(
    rows=1, cols=4,
    subplot_titles=['Avg Cycle Time', 'Defect Rate', 'OEE', 'Avg Cost'],
    specs=[[{"type": "indicator"}] * 4]
)

fig_kpi.add_trace(go.Indicator(
    mode="number+delta",
    value=kpi_metrics['avg_cycle_time'],
    title={'text': "Cycle Time (min)"},
    delta={'reference': 100, 'relative': True},
    domain={'x': [0, 1], 'y': [0, 1]}
), row=1, col=1)

fig_kpi.add_trace(go.Indicator(
    mode="number+delta",
    value=kpi_metrics['defect_rate'],
    title={'text': "Defect Rate (%)"},
    delta={'reference': 3, 'relative': True},
    domain={'x': [0, 1], 'y': [0, 1]}
), row=1, col=2)

fig_kpi.add_trace(go.Indicator(
    mode="number+gauge",
    value=kpi_metrics['oee'] * 100,
    title={'text': "OEE (%)"},
    gauge={'axis': {'range': [0, 100]}, 
           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 85}},
    domain={'x': [0, 1], 'y': [0, 1]}
), row=1, col=3)

fig_kpi.add_trace(go.Indicator(
    mode="number+delta",
    value=kpi_metrics['avg_cost'],
    title={'text': "Avg Cost (USD)"},
    delta={'reference': 5000, 'relative': True},
    domain={'x': [0, 1], 'y': [0, 1]}
), row=1, col=4)

fig_kpi.update_layout(height=300, title_text="Key Performance Indicators Dashboard")
fig_kpi.write_html('../outputs/kpi_dashboard.html')
print("   Saved: kpi_dashboard.html")

# 2. Pareto Chart
print("2. Creating Pareto chart...")
pareto_result = agent.pareto_analysis(group_by="process_step", metric="defect_count")
pareto_data = pareto_result['pareto_data']

fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])

fig_pareto.add_trace(
    go.Bar(x=pareto_data['category'], y=pareto_data['value'],
           name="Defect Count", marker_color=colors['primary']),
    secondary_y=False
)

fig_pareto.add_trace(
    go.Scatter(x=pareto_data['category'], y=pareto_data['cumulative_percentage'],
              name="Cumulative %", mode="lines+markers",
              marker=dict(size=10, color=colors['warning']),
              line=dict(width=3)),
    secondary_y=True
)

fig_pareto.add_hline(y=80, line_dash="dash", line_color="red", 
                     annotation_text="80% Threshold", secondary_y=True)

fig_pareto.update_layout(
    title="Pareto Analysis: Defect Distribution",
    xaxis_title="Process Step",
    height=600,
    hovermode="x unified"
)
fig_pareto.update_yaxes(title_text="Defect Count", secondary_y=False)
fig_pareto.update_yaxes(title_text="Cumulative %", secondary_y=True)

fig_pareto.write_html('../outputs/pareto_chart.html')
print("   Saved: pareto_chart.html")

# 3. Bottleneck Heatmap
print("3. Creating bottleneck heatmap...")
pivot = df.pivot_table(
    values='cycle_time_minutes',
    index='process_step',
    columns='site_location',
    aggfunc='mean'
)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=pivot.values,
    x=pivot.columns,
    y=pivot.index,
    colorscale='RdYlGn_r',
    text=pivot.values.round(1),
    texttemplate='%{text} min',
    textfont={"size": 10},
    colorbar=dict(title="Avg Cycle Time (min)")
))

fig_heatmap.update_layout(
    title="Process Bottleneck Analysis by Site",
    xaxis_title="Site Location",
    yaxis_title="Process Step",
    height=600
)

fig_heatmap.write_html('../outputs/bottleneck_heatmap.html')
print("   Saved: bottleneck_heatmap.html")

# 4. Quality Control Chart
print("4. Creating quality control chart...")
process_groups = df.groupby('process_step')
fig_control = go.Figure()

for process in df['process_step'].unique():
    process_data = df[df['process_step'] == process]['defect_count']
    fig_control.add_trace(go.Scatter(
        y=process_data,
        mode='markers',
        name=process,
        marker=dict(size=5)
    ))

mean_val = df['defect_count'].mean()
std_val = df['defect_count'].std()

fig_control.add_hline(y=mean_val, line_dash="dash", line_color="green",
                     annotation_text="Mean")
fig_control.add_hline(y=mean_val + 3*std_val, line_dash="dash", line_color="red",
                     annotation_text="UCL (3-sigma)")
fig_control.add_hline(y=max(0, mean_val - 3*std_val), line_dash="dash", line_color="red",
                     annotation_text="LCL (3-sigma)")

fig_control.update_layout(
    title="Quality Control Chart: Defect Monitoring",
    yaxis_title="Defect Count",
    xaxis_title="Observation",
    height=600
)

fig_control.write_html('../outputs/quality_control_chart.html')
print("   Saved: quality_control_chart.html")

# 5. Cost Analysis
print("5. Creating cost analysis...")
fig_cost = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Cost by Process", "Cost Distribution"),
    specs=[[{"type": "bar"}, {"type": "box"}]]
)

cost_by_process = df.groupby('process_step')['cost_usd'].mean().sort_values(ascending=True)

fig_cost.add_trace(
    go.Bar(y=cost_by_process.index, x=cost_by_process.values,
          orientation='h', marker_color=colors['info']),
    row=1, col=1
)

fig_cost.add_trace(
    go.Box(y=df['cost_usd'], name="Cost Distribution",
          marker_color=colors['secondary']),
    row=1, col=2
)

fig_cost.update_layout(height=600, showlegend=False, title_text="Cost Distribution Analysis")
fig_cost.write_html('../outputs/cost_analysis.html')
print("   Saved: cost_analysis.html")

# 6. Trend Analysis
print("6. Creating trend analysis...")
daily_metrics = df.groupby(pd.Grouper(key="timestamp", freq="D")).agg({
    'cycle_time_minutes': 'mean',
    'defect_count': 'sum',
    'cost_usd': 'mean'
}).reset_index()

fig_trend = make_subplots(
    rows=3, cols=1,
    subplot_titles=("Cycle Time Trend", "Daily Defects", "Cost Trend"),
    vertical_spacing=0.1
)

fig_trend.add_trace(
    go.Scatter(x=daily_metrics["timestamp"], y=daily_metrics["cycle_time_minutes"],
              mode="lines", name="Cycle Time", line=dict(color=colors['primary'])),
    row=1, col=1
)

fig_trend.add_trace(
    go.Scatter(x=daily_metrics["timestamp"], y=daily_metrics["defect_count"],
              mode="lines+markers", name="Defects", line=dict(color=colors['warning'])),
    row=2, col=1
)

fig_trend.add_trace(
    go.Scatter(x=daily_metrics["timestamp"], y=daily_metrics["cost_usd"],
              mode="lines", name="Cost", line=dict(color=colors['success'])),
    row=3, col=1
)

fig_trend.update_layout(height=900, showlegend=False, title_text="Operational Trends Over Time")
fig_trend.write_html('../outputs/trend_analysis.html')
print("   Saved: trend_analysis.html")

# 7. 3D Surface Plot - Process Performance
print("7. Creating 3D surface plot...")
pivot_3d = df.pivot_table(
    values='yield_percent',
    index='process_step',
    columns='product_line',
    aggfunc='mean'
)

fig_3d = go.Figure(data=[go.Surface(
    z=pivot_3d.values,
    x=pivot_3d.columns,
    y=pivot_3d.index,
    colorscale='Viridis'
)])

fig_3d.update_layout(
    title="3D Surface: Yield by Process and Product Line",
    scene=dict(
        xaxis_title="Product Line",
        yaxis_title="Process Step",
        zaxis_title="Yield %"
    ),
    height=700
)

fig_3d.write_html('../outputs/3d_surface_plot.html')
print("   Saved: 3d_surface_plot.html")

# 8. Sunburst Chart - Hierarchical Defects
print("8. Creating sunburst chart...")
defect_hierarchy = df.groupby(['site_location', 'process_step', 'product_line'])['defect_count'].sum().reset_index()

fig_sunburst = px.sunburst(
    defect_hierarchy,
    path=['site_location', 'process_step', 'product_line'],
    values='defect_count',
    title='Hierarchical Defect Distribution: Site > Process > Product'
)

fig_sunburst.update_layout(height=700)
fig_sunburst.write_html('../outputs/sunburst_defects.html')
print("   Saved: sunburst_defects.html")

# 9. Scatter Matrix
print("9. Creating scatter matrix...")
scatter_data = df[['cycle_time_minutes', 'defect_count', 'resource_utilization', 
                   'cost_usd', 'yield_percent']].sample(1000)

fig_scatter = px.scatter_matrix(
    scatter_data,
    dimensions=['cycle_time_minutes', 'defect_count', 'resource_utilization', 
                'cost_usd', 'yield_percent'],
    title='Correlation Matrix: Key Metrics'
)

fig_scatter.update_layout(height=900, width=900)
fig_scatter.write_html('../outputs/scatter_matrix.html')
print("   Saved: scatter_matrix.html")

# 10. Animated Timeline
print("10. Creating animated timeline...")
daily_data = df.groupby([pd.Grouper(key='timestamp', freq='D'), 'process_step']).agg({
    'defect_count': 'sum',
    'cycle_time_minutes': 'mean'
}).reset_index()

fig_animated = px.bar(
    daily_data,
    x='process_step',
    y='defect_count',
    animation_frame=daily_data['timestamp'].dt.strftime('%Y-%m-%d'),
    title='Daily Defect Evolution by Process',
    labels={'defect_count': 'Defect Count', 'process_step': 'Process Step'}
)

fig_animated.update_layout(height=600)
fig_animated.write_html('../outputs/animated_timeline.html')
print("   Saved: animated_timeline.html")

print("\n" + "="*70)
print("HTML VISUALIZATIONS COMPLETED")
print("="*70)
print("\nGenerated 10 interactive HTML files:")
print("1. kpi_dashboard.html - Real-time KPI indicators")
print("2. pareto_chart.html - Interactive 80/20 analysis")
print("3. bottleneck_heatmap.html - Process bottleneck heatmap")
print("4. quality_control_chart.html - Statistical quality monitoring")
print("5. cost_analysis.html - Cost distribution and analysis")
print("6. trend_analysis.html - Time-series trends")
print("7. 3d_surface_plot.html - 3D yield surface")
print("8. sunburst_defects.html - Hierarchical defect view")
print("9. scatter_matrix.html - Correlation analysis")
print("10. animated_timeline.html - Animated daily evolution")
print("\nAll files saved in: outputs/")
print("\nTo view: Open any HTML file in your web browser")
