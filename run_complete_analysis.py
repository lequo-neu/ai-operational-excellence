#!/usr/bin/env python3
"""
Master Script - AI-Powered Operational Excellence Project
Runs complete analysis pipeline and generates all outputs
"""

import os
import sys
import subprocess
from datetime import datetime

def print_banner(text):
    print("\n" + "="*70)
    print(text)
    print("="*70)

def run_step(step_num, description, command):
    print(f"\n[{step_num}] {description}")
    print(f"    Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"    Status: SUCCESS")
        return True
    else:
        print(f"    Status: FAILED")
        print(f"    Error: {result.stderr}")
        return False

def main():
    print_banner("AI-POWERED OPERATIONAL EXCELLENCE - COMPLETE EXECUTION")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    print(f"\nProject Directory: {project_dir}")
    
    # Create outputs directory if not exists
    os.makedirs('outputs', exist_ok=True)
    print("Outputs directory ready")
    
    steps_completed = []
    
    # Step 1: Generate Data
    print_banner("STEP 1: DATA GENERATION")
    if run_step(1, "Generate 15,000 operational records", 
                "python src/data_generator.py"):
        steps_completed.append("Data Generation")
    
    # Step 2: Run Validation
    print_banner("STEP 2: VALIDATION SUITE")
    if run_step(2, "Validate all components", 
                "python src/validate.py"):
        steps_completed.append("Validation")
    
    # Step 3: Generate HTML Visualizations
    print_banner("STEP 3: INTERACTIVE HTML VISUALIZATIONS")
    if run_step(3, "Generate 10 interactive HTML charts", 
                "python src/generate_html_visualizations.py"):
        steps_completed.append("HTML Visualizations")
    
    # Step 4: Run Jupyter Notebook (if nbconvert available)
    print_banner("STEP 4: JUPYTER NOTEBOOK ANALYSIS")
    print("[4] Execute complete analysis notebook")
    print("    Note: Run manually with: jupyter notebook notebooks/operational_excellence_analysis.ipynb")
    print("    Or execute all cells with: jupyter nbconvert --to notebook --execute notebooks/operational_excellence_analysis.ipynb")
    
    # Summary
    print_banner("EXECUTION SUMMARY")
    print(f"\nCompleted Steps ({len(steps_completed)}/3):")
    for i, step in enumerate(steps_completed, 1):
        print(f"  {i}. {step}")
    
    print("\nGenerated Outputs:")
    if os.path.exists('outputs'):
        files = sorted([f for f in os.listdir('outputs') if not f.startswith('.')])
        for i, file in enumerate(files, 1):
            file_path = os.path.join('outputs', file)
            size = os.path.getsize(file_path)
            print(f"  {i}. {file} ({size:,} bytes)")
    
    print("\n" + "="*70)
    print("HOW TO VIEW RESULTS")
    print("="*70)
    print("\n1. STATIC CHARTS (PNG):")
    print("   Open outputs/*.png in any image viewer")
    print("\n2. INTERACTIVE CHARTS (HTML):")
    print("   Open outputs/*.html in web browser")
    print("   - Double-click any HTML file")
    print("   - Or: open outputs/kpi_dashboard.html")
    print("\n3. DATA REPORTS (XLSX):")
    print("   Open outputs/*.xlsx in Excel or Google Sheets")
    print("\n4. JUPYTER ANALYSIS:")
    print("   jupyter notebook notebooks/operational_excellence_analysis.ipynb")
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

if __name__ == "__main__":
    main()
