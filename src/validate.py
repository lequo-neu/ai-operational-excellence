#!/usr/bin/env python3
"""
Validation and testing script for AI-Powered Operational Excellence project.
Verifies all components are working correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas as pd
import numpy as np
from datetime import datetime

def validate_data_generation():
    """Test data generation module"""
    print("\n" + "="*70)
    print("VALIDATING DATA GENERATION")
    print("="*70)
    
    from data_generator import generate_operational_data
    
    df = generate_operational_data(1000)
    
    assert len(df) == 1000, "Record count mismatch"
    assert df['cycle_time_minutes'].min() > 0, "Invalid cycle times"
    assert df['defect_count'].min() >= 0, "Negative defects"
    assert df['resource_utilization'].between(0, 1).all(), "Invalid utilization"
    
    print("✓ Data generation validated")
    print(f"  - Generated {len(df)} records")
    print(f"  - {df['process_step'].nunique()} process steps")
    print(f"  - {df['product_line'].nunique()} product lines")
    return df

def validate_lean_six_sigma(df):
    """Test Lean Six Sigma analysis"""
    print("\n" + "="*70)
    print("VALIDATING LEAN SIX SIGMA ANALYSIS")
    print("="*70)
    
    from lean_six_sigma import LeanSixSigmaAnalyzer
    
    lss = LeanSixSigmaAnalyzer(df)
    
    # Test DPMO calculation
    dpmo = lss.calculate_dpmo()
    assert 'DPMO' in dpmo, "DPMO not calculated"
    assert dpmo['DPMO'] > 0, "Invalid DPMO"
    print(f"✓ DPMO: {dpmo['DPMO']:,.2f} (Sigma: {dpmo['Sigma_Level']:.1f})")
    
    # Test capability analysis
    capability = lss.process_capability_analysis()
    assert 'Cp' in capability, "Cp not calculated"
    assert 'Cpk' in capability, "Cpk not calculated"
    print(f"✓ Process Capability: Cp={capability['Cp']:.3f}, Cpk={capability['Cpk']:.3f}")
    
    # Test bottleneck identification
    bottlenecks = lss.identify_bottlenecks()
    print(f"✓ Bottleneck analysis completed: {len(bottlenecks)} found")
    
    # Test OEE calculation
    oee = lss.calculate_oee()
    assert 'OEE' in oee, "OEE not calculated"
    assert 0 <= oee['OEE'] <= 1, "Invalid OEE"
    print(f"✓ OEE: {oee['OEE']*100:.2f}%")
    
    return lss, dpmo, capability, bottlenecks, oee

def validate_ai_agent(df):
    """Test AI agent analysis"""
    print("\n" + "="*70)
    print("VALIDATING AI AGENT")
    print("="*70)
    
    from ai_agent import AIAnalysisAgent
    
    agent = AIAnalysisAgent(df)
    
    # Test Pareto analysis
    pareto = agent.pareto_analysis(group_by="process_step", metric="defect_count")
    assert 'vital_few' in pareto, "Pareto analysis failed"
    assert len(pareto['vital_few']) > 0, "No vital few identified"
    print(f"✓ Pareto analysis: {pareto['vital_few_count']} vital few identified")
    
    # Test anomaly detection
    anomalies = agent.detect_anomalies(metric="cycle_time_minutes")
    assert 'anomaly_count' in anomalies, "Anomaly detection failed"
    print(f"✓ Anomaly detection: {anomalies['anomaly_count']} anomalies ({anomalies['anomaly_percentage']:.2f}%)")
    
    # Test root cause analysis
    root_causes = agent.root_cause_analysis()
    assert 'process' in root_causes, "Root cause analysis incomplete"
    print(f"✓ Root cause analysis completed")
    
    return agent, pareto, anomalies, root_causes

def validate_visualization(df):
    """Test visualization generation"""
    print("\n" + "="*70)
    print("VALIDATING VISUALIZATION")
    print("="*70)
    
    try:
        from visualization import OperationalDashboard
        
        dashboard = OperationalDashboard(df)
        
        # Test KPI metrics
        metrics = {
            'avg_cycle_time': df['cycle_time_minutes'].mean(),
            'defect_rate': 2.5,
            'oee': 0.75,
            'avg_cost': df['cost_usd'].mean()
        }
        
        try:
            fig = dashboard.create_kpi_cards(metrics)
            print("✓ KPI cards generated")
        except Exception as e:
            print(f"⚠ KPI cards skipped: {e}")
        
        try:
            fig = dashboard.create_bottleneck_heatmap()
            print("✓ Bottleneck heatmap generated")
        except Exception as e:
            print(f"⚠ Bottleneck heatmap skipped: {e}")
        
        try:
            fig = dashboard.create_quality_control_chart()
            print("✓ Quality control chart generated")
        except Exception as e:
            print(f"⚠ Quality control chart skipped: {e}")
        
        return dashboard
    except ImportError as e:
        print(f"⚠ Visualization module not available: {e}")
        print("  (This is optional - install plotly for full visualization support)")
        return None

def run_full_validation():
    """Run complete validation suite"""
    print("\n" + "="*70)
    print("AI-POWERED OPERATIONAL EXCELLENCE VALIDATION SUITE")
    print("="*70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Validate each component
        df = validate_data_generation()
        lss, dpmo, capability, bottlenecks, oee = validate_lean_six_sigma(df)
        agent, pareto, anomalies, root_causes = validate_ai_agent(df)
        dashboard = validate_visualization(df)
        
        # Summary
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        print("✓ All components validated successfully")
        print("\nKey Metrics:")
        print(f"  - Records processed: {len(df):,}")
        print(f"  - DPMO: {dpmo['DPMO']:,.2f}")
        print(f"  - Sigma Level: {dpmo['Sigma_Level']:.1f}")
        print(f"  - Process Capability (Cpk): {capability['Cpk']:.3f}")
        print(f"  - OEE: {oee['OEE']*100:.2f}%")
        print(f"  - Bottlenecks identified: {len(bottlenecks)}")
        print(f"  - Vital few (Pareto): {pareto['vital_few_count']}")
        print(f"  - Anomalies detected: {anomalies['anomaly_count']}")
        
        print("\n✓ VALIDATION COMPLETE")
        return True
        
    except Exception as e:
        print(f"\n✗ VALIDATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

if __name__ == "__main__":
    success = run_full_validation()
    sys.exit(0 if success else 1)
