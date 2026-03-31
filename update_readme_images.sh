#!/bin/bash

# Script to update README with proper GitHub image paths
# Run this after pushing to GitHub

GITHUB_USER="lequo-neu"
REPO_NAME="ai-operational-excellence"
BRANCH="main"

echo "Updating README.md with GitHub image paths..."

# Backup original
cp README.md README.md.backup

# Replace image paths
sed -i '' "s|outputs/process_capability.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/process_capability.png|g" README.md
sed -i '' "s|outputs/bottleneck_heatmap.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/bottleneck_heatmap.png|g" README.md
sed -i '' "s|outputs/value_stream_analysis.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/value_stream_analysis.png|g" README.md
sed -i '' "s|outputs/oee_analysis.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/oee_analysis.png|g" README.md
sed -i '' "s|outputs/pareto_chart.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/pareto_chart.png|g" README.md
sed -i '' "s|outputs/anomaly_detection.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/anomaly_detection.png|g" README.md
sed -i '' "s|outputs/root_cause_analysis.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/root_cause_analysis.png|g" README.md
sed -i '' "s|outputs/recommendations_overview.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/recommendations_overview.png|g" README.md
sed -i '' "s|outputs/executive_dashboard.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/executive_dashboard.png|g" README.md
sed -i '' "s|outputs/metric_distributions.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/metric_distributions.png|g" README.md
sed -i '' "s|outputs/process_analysis.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/process_analysis.png|g" README.md
sed -i '' "s|outputs/site_comparison.png|https://raw.githubusercontent.com/$GITHUB_USER/$REPO_NAME/$BRANCH/outputs/site_comparison.png|g" README.md

echo "README.md updated with GitHub URLs"
echo "Backup saved as README.md.backup"
