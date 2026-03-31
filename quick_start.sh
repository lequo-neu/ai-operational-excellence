#!/bin/bash

# Quick Launch Script for AI Operational Excellence Project
# Usage: ./quick_start.sh

echo "=========================================="
echo "AI Operational Excellence - Quick Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "ERROR: Virtual environment not found at ../.venv"
    echo "Please create it first: python -m venv ../.venv"
    exit 1
fi

# Activate virtual environment
echo "[1/4] Activating virtual environment..."
source ../.venv/bin/activate

# Install/verify dependencies
echo "[2/4] Checking dependencies..."
pip install -q pandas numpy scipy openpyxl jupyter matplotlib seaborn plotly

# Run complete analysis
echo "[3/4] Running complete analysis..."
python run_complete_analysis.py

# Open results
echo "[4/4] Opening results..."
echo ""
echo "Opening interactive dashboards in browser..."
sleep 2

# Open key HTML files
open outputs/kpi_dashboard.html 2>/dev/null
sleep 1
open outputs/pareto_chart.html 2>/dev/null
sleep 1
open outputs/3d_surface_plot.html 2>/dev/null

echo ""
echo "=========================================="
echo "COMPLETE!"
echo "=========================================="
echo ""
echo "View all results in: outputs/"
echo ""
echo "Next steps:"
echo "  1. Check opened browser tabs for interactive charts"
echo "  2. Run Jupyter: jupyter notebook notebooks/operational_excellence_analysis.ipynb"
echo "  3. View Excel reports: open outputs/*.xlsx"
echo ""
