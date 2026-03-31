#!/bin/bash

# Git Repository Setup Script for AI Operational Excellence Project
# This script initializes a new Git repo and prepares for GitHub upload

echo "==========================================="
echo "Git Repository Setup"
echo "AI Operational Excellence Project"
echo "==========================================="
echo ""

# Navigate to project directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)
echo "Project directory: $PROJECT_DIR"
echo ""

# Initialize Git repository
echo "[1/6] Initializing Git repository..."
git init

# Create .gitkeep files for empty directories
echo "[2/6] Creating .gitkeep files..."
touch data/.gitkeep
touch outputs/.gitkeep

# Add all files
echo "[3/6] Adding files to Git..."
git add .gitignore
git add README.md
git add README_GITHUB.md
git add HUONG_DAN.md
git add requirements.txt
git add run_complete_analysis.py
git add quick_start.sh
git add setup_git.sh
git add src/
git add notebooks/
git add configs/
git add docs/
git add data/.gitkeep
git add outputs/.gitkeep

# Check what will be committed
echo ""
echo "[4/6] Files staged for commit:"
git status --short

# Commit
echo ""
echo "[5/6] Creating initial commit..."
git commit -m "Initial commit: AI-Powered Operational Excellence Project

Features:
- End-to-end AI pipeline processing 15K+ pharmaceutical records
- Lean Six Sigma integration (DPMO, Cpk, OEE, VSM)
- AI agents for Pareto analysis and root cause identification
- 22 professional visualizations (10 HTML + 12 PNG)
- Strategic recommendations with ROI estimates
- AI Governance framework (FDA, GxP compliance)
- Complete documentation and training materials

Tech Stack: Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, Plotly, Jupyter"

# Success
echo ""
echo "[6/6] Git repository initialized successfully!"
echo ""
echo "==========================================="
echo "Next Steps:"
echo "==========================================="
echo ""
echo "1. CREATE GITHUB REPO:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: ai-operational-excellence"
echo "   - Description: AI-Powered Operational Excellence & Agentic Workflow Automation"
echo "   - Make it: Public (so employers can see it)"
echo "   - DO NOT initialize with README (we already have one)"
echo ""
echo "2. CONNECT TO GITHUB:"
echo "   Run these commands (replace lequo-neu):"
echo ""
echo "   git remote add origin https://github.com/lequo-neu/ai-operational-excellence.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. VERIFY:"
echo "   - Visit: https://github.com/lequo-neu/ai-operational-excellence"
echo "   - README should display with images"
echo "   - All files should be visible"
echo ""
echo "==========================================="
echo "Repository Location: $PROJECT_DIR"
echo "==========================================="
