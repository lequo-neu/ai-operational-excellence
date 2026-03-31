# Prompt Engineering Playbook for Operational Excellence

## Introduction

This playbook provides reusable prompt templates and context engineering strategies for maximizing AI effectiveness in pharmaceutical operations. Designed for non-technical users to leverage AI agents for operational analysis and decision support.

## Core Principles

### 1. Clarity
Be specific about what you want. Vague prompts yield vague results.

**Bad:** "Analyze the data"  
**Good:** "Identify the top 3 processes with highest defect rates and recommend root cause investigation priorities"

### 2. Context
Provide relevant background information and constraints.

**Components:**
- Role definition
- Current situation
- Historical context
- Constraints/limitations
- Success criteria

### 3. Structure
Use consistent formats for repeatable tasks.

**Template:**
```
Role: [Who the AI should act as]
Context: [Relevant background]
Task: [Specific action required]
Constraints: [Limitations, requirements]
Output Format: [How to present results]
```

## Use Case Templates

### Use Case 1: Process Bottleneck Analysis

```
Role: Senior Process Engineer with Lean Six Sigma Black Belt certification

Context:
- Manufacturing site: [Site Name]
- Product line: [Product Line]
- Time period: [Date Range]
- Current OEE: [X%]
- Target OEE: [Y%]

Task:
1. Analyze cycle time data across all process steps
2. Identify bottlenecks using 1.5x threshold above mean
3. Calculate impact on overall throughput
4. Rank by severity and improvement potential

Constraints:
- Must consider GxP compliance requirements
- Capital budget limited to $200K
- Implementation timeline: Q2 2026

Output Format:
- Table with process, cycle time, bottleneck score, impact
- Top 3 recommendations with ROI estimates
- Implementation roadmap (Gantt chart)
```

### Use Case 2: Quality Investigation

```
Role: Quality Assurance Specialist conducting root cause analysis

Context:
- Quality event: [Description]
- Affected batches: [Batch IDs]
- Defect type: [Defect Category]
- Detection point: [Process Step]

Task:
1. Perform Pareto analysis on defect distribution
2. Correlate defects with process parameters (temperature, humidity, operator, equipment)
3. Apply 5 Whys methodology
4. Generate Ishikawa (fishbone) diagram data

Constraints:
- Investigation deadline: [Date]
- Must follow CAPA procedure SOP-QA-001
- Requires statistical significance (p<0.05)

Output Format:
- Executive summary (1 page)
- Statistical analysis results
- Root cause hypothesis
- Preventive action recommendations
- Risk assessment (severity × probability)
```

### Use Case 3: Cost Optimization

```
Role: Operations Finance Analyst focused on cost reduction

Context:
- Current operational cost: $[X]M annually
- Cost breakdown: [Material 60%, Labor 25%, Overhead 15%]
- Savings target: 10% ($[Y]M)
- Timeframe: 12 months

Task:
1. Identify top cost drivers using Pareto principle
2. Benchmark against industry standards
3. Analyze cost variance by site and product line
4. Propose cost reduction initiatives

Constraints:
- No impact on product quality or compliance
- Avoid headcount reduction
- Must be sustainable long-term

Output Format:
- Cost waterfall chart
- Initiative portfolio (quick wins vs. strategic projects)
- Implementation plan with milestones
- Risk mitigation strategies
```

### Use Case 4: Predictive Maintenance

```
Role: Reliability Engineer implementing predictive maintenance

Context:
- Equipment portfolio: [X] critical assets
- Current maintenance strategy: Time-based PM
- Unplanned downtime cost: $[Y]K per hour
- Equipment age: [Range]

Task:
1. Analyze failure patterns and MTBF (Mean Time Between Failures)
2. Identify equipment with high failure risk
3. Calculate optimal PM intervals
4. Prioritize condition monitoring investments

Constraints:
- Budget: $150K for monitoring systems
- Implementation: Phased over 6 months
- No production disruption

Output Format:
- Equipment criticality matrix
- Failure mode analysis
- PM optimization plan
- ROI calculation (NPV, payback period)
```

### Use Case 5: Capacity Planning

```
Role: Supply Chain Planner conducting capacity analysis

Context:
- Current production capacity: [X] units/month
- Demand forecast: [Y] units/month (12-month horizon)
- Capacity utilization: [Z%]
- Lead time for capacity expansion: 6 months

Task:
1. Analyze current capacity utilization by product line
2. Identify constraints and theoretical maximum capacity
3. Model demand scenarios (base, optimistic, pessimistic)
4. Recommend capacity expansion timing and magnitude

Constraints:
- Capital approval process: 3 months
- Regulatory submission for major changes: 6 months
- Inventory carrying cost: 15% annually

Output Format:
- Capacity utilization dashboard
- Scenario analysis table
- Decision tree for expansion timing
- Financial impact assessment
```

## Context Engineering Templates

### Template 1: Operational KPI Analysis

```python
PROMPT_TEMPLATE = """
You are an Operations Analytics Specialist at {company_name}.

**Objective:** {analysis_objective}

**Data Context:**
- Dataset: {record_count} operational records
- Time Period: {start_date} to {end_date}
- Processes: {process_list}
- Sites: {site_list}

**Current Performance:**
- Cycle Time: {current_cycle_time} minutes (Target: {target_cycle_time})
- Defect Rate: {current_defects} DPMO (Target: {target_dpmo})
- OEE: {current_oee}% (Target: {target_oee}%)

**Analysis Requirements:**
1. {requirement_1}
2. {requirement_2}
3. {requirement_3}

**Constraints:**
- Compliance: {compliance_requirements}
- Budget: {budget_limit}
- Timeline: {deadline}

**Deliverable:**
{output_format}

Provide your analysis below:
"""
```

### Template 2: Root Cause Investigation

```python
INVESTIGATION_PROMPT = """
You are conducting a root cause analysis for a quality deviation.

**Deviation Details:**
- Deviation ID: {deviation_id}
- Product: {product_name}
- Batch: {batch_id}
- Description: {deviation_description}
- Severity: {severity_level}

**Data Available:**
- Process parameters: {parameter_data}
- Environmental conditions: {environmental_data}
- Equipment logs: {equipment_data}
- Material certifications: {material_data}

**Investigation Framework:**
- Apply Ishikawa (6M): Man, Machine, Material, Method, Measurement, Mother Nature
- Use 5 Whys technique
- Statistical correlation analysis

**Regulatory Requirements:**
- Follow FDA 21 CFR 211.192 (Production record review)
- Document per CAPA SOP-QA-001
- Timeline: Investigation within {days} days

**Expected Output:**
1. Probable root cause
2. Contributing factors
3. CAPA recommendations
4. Risk assessment
5. Verification plan

Begin investigation:
"""
```

## Advanced Techniques

### 1. Chain-of-Thought Prompting

Encourage step-by-step reasoning:

```
Analyze this bottleneck. Think through this step-by-step:

Step 1: Calculate the average cycle time for each process
Step 2: Compare against overall mean to identify outliers
Step 3: Assess resource utilization during bottleneck periods
Step 4: Determine root cause category (capacity, variability, dependency)
Step 5: Recommend specific interventions

Show your reasoning at each step.
```

### 2. Few-Shot Learning

Provide examples of desired output:

```
Analyze the following processes and categorize improvement opportunities:

Example 1:
Process: Filling
Cycle Time: 120 min
Utilization: 95%
Assessment: Capacity-constrained, requires additional line
Priority: HIGH

Example 2:
Process: Packaging
Cycle Time: 45 min
Utilization: 60%
Assessment: Inefficient workflow, needs lean optimization
Priority: MEDIUM

Now analyze:
Process: Quality Control
Cycle Time: 180 min
Utilization: 85%
Assessment: [Your analysis]
Priority: [Your prioritization]
```

### 3. Role Prompting with Constraints

```
You are a pharmaceutical manufacturing expert reviewing a proposed process change.

Evaluate this change considering:
- GMP compliance (FDA 21 CFR Part 211)
- Patient safety impact
- Cost-benefit analysis
- Implementation feasibility
- Change control requirements

Be conservative. If uncertain, recommend additional validation studies.

Proposed Change: [Description]

Your evaluation:
```

### 4. Multi-Perspective Analysis

```
Analyze this scenario from multiple stakeholder perspectives:

1. Quality Assurance:
   - Compliance implications?
   - Validation requirements?
   - Risk to product quality?

2. Operations:
   - Impact on throughput?
   - Training needs?
   - Operational complexity?

3. Finance:
   - Capital requirements?
   - Operating cost impact?
   - ROI timeline?

4. Regulatory Affairs:
   - Submission requirements?
   - Regulatory risk?
   - Post-approval changes?

Scenario: [Description]

Provide perspectives:
```

## Common Pitfalls & Solutions

### Pitfall 1: Ambiguous Instructions
**Problem:** "Make the process better"  
**Solution:** "Reduce cycle time by 20% while maintaining quality"

### Pitfall 2: Missing Context
**Problem:** "Why are defects high?"  
**Solution:** "Defects increased 30% since operator rotation change on 2/1/26. Analyze correlation with training records and process parameters."

### Pitfall 3: Unrealistic Expectations
**Problem:** "Solve all our problems"  
**Solution:** "Prioritize top 3 improvement opportunities based on impact and feasibility"

### Pitfall 4: No Success Criteria
**Problem:** "Analyze the data"  
**Solution:** "Identify root causes with >0.5 correlation coefficient and >95% confidence"

### Pitfall 5: Ignoring Constraints
**Problem:** "Optimize the process"  
**Solution:** "Optimize within GMP guidelines, $50K budget, and 30-day timeline"

## Best Practices Checklist

Before submitting a prompt:
- [ ] Is the role/perspective clearly defined?
- [ ] Have I provided sufficient context?
- [ ] Are the requirements specific and measurable?
- [ ] Have I stated constraints and limitations?
- [ ] Is the desired output format specified?
- [ ] Have I included relevant data or references?
- [ ] Is the success criteria clear?
- [ ] Have I considered regulatory/compliance needs?

## Performance Optimization Tips

### Tip 1: Iterative Refinement
Start broad, then narrow based on initial results.

**Iteration 1:** "Analyze quality data"  
**Iteration 2:** "Focus on Oncology product line defects"  
**Iteration 3:** "Specifically analyze Filling process defects in Oncology"

### Tip 2: Break Complex Tasks
Divide large analyses into sequential steps.

```
Task 1: Data validation and cleaning
Task 2: Descriptive statistics by category
Task 3: Correlation analysis
Task 4: Root cause hypothesis generation
Task 5: Recommendation prioritization
```

### Tip 3: Request Explanations
Always ask "why" to build understanding.

```
Not just: "What is the bottleneck?"
But also: "Why is this a bottleneck? What factors contribute?"
```

### Tip 4: Validate Outputs
Request confidence levels and data sources.

```
For each recommendation, provide:
- Confidence level (high/medium/low)
- Supporting data points
- Assumptions made
- Potential risks
```

## AI Office Hours: Common Questions

### Q1: "How do I get started with AI for my role?"
**A:** Start with Use Case Template that matches your function. Customize with your specific data and constraints.

### Q2: "What if the AI gives incorrect results?"
**A:** Always validate critical recommendations with SMEs. Use AI as decision support, not decision maker.

### Q3: "How do I provide feedback to improve AI performance?"
**A:** Use the feedback form in the dashboard. Specify what was wrong and what you expected.

### Q4: "Can AI replace my expertise?"
**A:** No. AI accelerates analysis and surfaces insights, but domain expertise is essential for validation and implementation.

### Q5: "What data should I not share with AI?"
**A:** Patient identifiable information (PII), trade secrets, proprietary formulations, and competitive intelligence.

## Training Exercises

### Exercise 1: Prompt Crafting
Take a vague request and improve it using the templates above.

**Vague:** "Look at the production data"  
**Improved:** [Your enhanced prompt]

### Exercise 2: Context Addition
Add context to make this prompt actionable:

**Incomplete:** "Find the problem in Quality Control"  
**Complete:** [Your contextualized prompt]

### Exercise 3: Output Specification
Define exactly what output format you need:

**Ambiguous:** "Tell me about the results"  
**Precise:** [Your specified format]

## Resources

### Internal
- AI Governance Guidelines: `/docs/AI_GOVERNANCE.md`
- SOP-AI-001: AI System Usage Procedures
- Training Portal: [Internal Link]

### External
- Prompt Engineering Guide: promptingguide.ai
- OpenAI Best Practices: platform.openai.com/docs/guides/prompt-engineering
- Anthropic Claude Documentation: docs.anthropic.com

## Support

**AI Enablement Team**  
- Email: ai-enablement@vertex.com
- Slack: #ai-office-hours
- Office Hours: Tuesdays 2-3 PM EST

**Quick Reference Card**  
Download printable prompt template: [Link]

---

**Version:** 1.0  
**Last Updated:** February 2026  
**Next Review:** May 2026
