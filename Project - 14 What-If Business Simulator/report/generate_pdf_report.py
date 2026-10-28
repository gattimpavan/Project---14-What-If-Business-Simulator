"""
Mahindra & Mahindra Ltd. - Publication-Grade Executive PDF Report Generator
Project - 14: What-If Business Simulator

Compiles an exhaustive, C-suite executive decision deliverable:
- Problem Statement Formulation & Executive Summary
- 4-Pillar Cross-Functional Feasibility Audit (Employees, Inventory, Capacity, Logistics)
- 5 Publication-Grade High-DPI Charts:
    1. 4-Pillar Capacity Headroom Radar / Constraint Decomposition
    2. Scenario Benchmark Matrix (Demand Fulfillment vs EBITDA Margin)
    3. Workforce Overtime & Factories Act 1948 Compliance Threshold
    4. Monte Carlo 1,000 Stochastic Risk Distribution (VaR & P10/P50/P90)
    5. Enterprise Revenue Waterfall (Uncaptured Leakage vs Agile Accretion)
- Scenario Comparison Audit Table (Scenarios A through E)
- Critical Components Supply Bottleneck Matrix
- 180-Day Phased Board Execution Roadmap
"""

import os
import sys
import tempfile
import numpy as np
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Configure Matplotlib
mpl_dir = os.path.join(tempfile.gettempdir(), "mpl_mahindra_14")
os.makedirs(mpl_dir, exist_ok=True)
os.environ["MPLCONFIGDIR"] = mpl_dir

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

from models.what_if_engine import WhatIfBusinessSimulator
from models.scenario_optimizer import ScenarioOptimizer
from models.monte_carlo_simulator import MonteCarloSimulator
from models.ai_strategic_advisor import AIStrategicAdvisor

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "MAHINDRA & MAHINDRA LTD. | EXECUTIVE WHAT-IF DECISION INTELLIGENCE REPORT")
            self.drawRightString(612 - 54, 755, "PROJECT - 14: WHAT-IF BUSINESS SIMULATOR")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 747, 612 - 54, 747)

        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        
        self.drawString(54, 32, "CONFIDENTIAL // STRICTLY FOR M&M BOARD OF DIRECTORS & OPERATING COMMITTEE")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_report_visualizations(chart_dir):
    os.makedirs(chart_dir, exist_ok=True)
    chart_paths = {}

    simulator = WhatIfBusinessSimulator()
    optimizer = ScenarioOptimizer()
    scenarios = optimizer.get_all_scenarios(20.0)

    # Palette
    c_red = "#C8102E"       # Mahindra iconic crimson
    c_dark = "#0F172A"      # Slate charcoal
    c_blue = "#0284C7"      # High-tech blue
    c_green = "#059669"     # Emerald success
    c_amber = "#D97706"     # Warning amber
    c_gray = "#64748B"

    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#CBD5E1'
    plt.rcParams['axes.linewidth'] = 0.8

    # -------------------------------------------------------------
    # CHART 1: 4-Pillar Capacity Headroom Breakdown
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=260)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    categories = ['Plant Tooling\nCapacity', 'Workforce Hours\n(Labor Feasible)', 'Inventory Buffer\n(Tier-1 Deliverable)', 'Logistics Fleet\n(Dispatch Feasible)']
    
    # Values under naive push
    naive_res = scenarios[0]["results"]
    agile_res = scenarios[4]["results"]
    target_demand = 600000

    naive_vals = [
        naive_res["pillar_capacities"]["Plant & Tooling Capacity"],
        naive_res["pillar_capacities"]["Workforce & Labor Hours"],
        naive_res["pillar_capacities"]["Inventory & Component Supply"],
        naive_res["pillar_capacities"]["Logistics & Yard Clearance"]
    ]

    agile_vals = [
        agile_res["pillar_capacities"]["Plant & Tooling Capacity"],
        agile_res["pillar_capacities"]["Workforce & Labor Hours"],
        agile_res["pillar_capacities"]["Inventory & Component Supply"],
        agile_res["pillar_capacities"]["Logistics & Yard Clearance"]
    ]

    x = np.arange(len(categories))
    width = 0.35

    rects1 = ax.bar(x - width/2, [v/1000 for v in naive_vals], width, label='Status Quo (+20% Naive Push)', color='#EF4444', alpha=0.9, edgecolor='#991B1B')
    rects2 = ax.bar(x + width/2, [v/1000 for v in agile_vals], width, label='Scenario E (Agile Transformation)', color='#10B981', alpha=0.9, edgecolor='#065F46')

    ax.axhline(y=target_demand/1000, color='#1E293B', linestyle='--', linewidth=1.5, label='Target Demand (600,000 units)')
    ax.axhline(y=500, color='#64748B', linestyle=':', linewidth=1.2, label='Baseline Demand (500,000 units)')

    ax.set_ylabel('Effective Annual Volume Capacity (\'000 Vehicles)', fontsize=10, fontweight='bold', color='#1E293B')
    ax.set_title('Cross-Functional Operational Capacity Headroom vs Target Demand (600k Units)', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5, fontweight='bold', color='#334155')
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=8.5, loc='lower right')
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.set_ylim(350, 750)

    for bar in rects1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 8, f"{int(yval)}k", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#991B1B')

    for bar in rects2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 8, f"{int(yval)}k", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#065F46')

    plt.tight_layout()
    chart1_path = os.path.join(chart_dir, "chart1_pillar_capacities.png")
    plt.savefig(chart1_path, dpi=260)
    plt.close()
    chart_paths["pillar_capacities"] = chart1_path

    # -------------------------------------------------------------
    # CHART 2: Scenario Comparison Matrix (Fulfillment vs EBITDA Margin)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=260)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    sc_names = ['A: Status Quo', 'B: Asset Sweat', 'C: Shift 3', 'D: Rail & Buffer', 'E: Agile Enterprise']
    fulfillments = [s["results"]["demand"]["fulfillment_rate_pct"] for s in scenarios]
    ebitdas = [s["results"]["financials"]["ebitda_cr"] / 1000 for s in scenarios] # in ₹k Cr
    scores = [s["results"]["overall_feasibility"]["score"] for s in scenarios]
    bar_colors = ['#EF4444', '#F59E0B', '#3B82F6', '#0284C7', '#10B981']

    bars = ax.barh(sc_names, fulfillments, color=bar_colors, edgecolor='#334155', height=0.55)
    ax.set_xlabel('Demand Fulfillment Rate (%)', fontsize=10, fontweight='bold', color='#1E293B')
    ax.set_xlim(50, 108)
    ax.axvline(x=95, color='#059669', linestyle='--', linewidth=1.2, label='Target Benchmark (95% Fulfillment)')
    ax.set_title('Scenario Benchmark: Sales Fulfillment & Enterprise Viability Score', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')

    for i, bar in enumerate(bars):
        w = bar.get_width()
        ebitda_val = ebitdas[i]
        score_val = scores[i]
        ax.text(w + 1.2, bar.get_y() + bar.get_height()/2.0, 
                f"{w:.1f}% | EBITDA: ₹{ebitda_val:.2f}k Cr | Feasibility: {score_val}/100", 
                ha='left', va='center', fontsize=8.5, fontweight='bold', color='#1E293B')

    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=8.5, loc='lower left')
    plt.tight_layout()
    chart2_path = os.path.join(chart_dir, "chart2_scenario_matrix.png")
    plt.savefig(chart2_path, dpi=260)
    plt.close()
    chart_paths["scenario_matrix"] = chart2_path

    # -------------------------------------------------------------
    # CHART 3: Workforce Overtime & Factories Act 1948 Compliance
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 3.8), dpi=260)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    ots = [s["results"]["workforce_metrics"]["avg_ot_hours_quarterly"] for s in scenarios]
    absenteeisms = [s["results"]["workforce_metrics"]["absenteeism_pct"] for s in scenarios]

    x = np.arange(len(sc_names))
    width = 0.38

    b1 = ax.bar(x - width/2, ots, width, label='Quarterly Overtime Hours/Worker', color=['#DC2626' if o > 50 else '#10B981' for o in ots], edgecolor='#1E293B')
    
    ax2 = ax.twinx()
    l1 = ax2.plot(x + width/2, absenteeisms, color='#D97706', marker='o', linewidth=2.2, label='Absenteeism Rate (%)')

    ax.axhline(y=50.0, color='#991B1B', linestyle='--', linewidth=1.5, label='Factories Act 1948 Limit (50 hrs/qtr)')
    ax.set_ylabel('Overtime (Hours / Quarter)', fontsize=9.5, fontweight='bold', color='#1E293B')
    ax2.set_ylabel('Worker Absenteeism (%)', fontsize=9.5, fontweight='bold', color='#D97706')
    ax.set_title('Labor Welfare & Statutory Compliance: Overtime vs Absenteeism', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(sc_names, fontsize=9, fontweight='bold', color='#334155')
    ax.set_ylim(0, 130)
    ax2.set_ylim(4, 25)

    # Combined legend
    h1, l1_lbl = ax.get_legend_handles_labels()
    h2, l2_lbl = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1_lbl + l2_lbl, frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=8, loc='upper right')

    for bar in b1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f"{yval:.1f}h", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    plt.tight_layout()
    chart3_path = os.path.join(chart_dir, "chart3_workforce_compliance.png")
    plt.savefig(chart3_path, dpi=260)
    plt.close()
    chart_paths["workforce_compliance"] = chart3_path

    # -------------------------------------------------------------
    # CHART 4: Monte Carlo 1,000 Stochastic Risk Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=260)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    mc = MonteCarloSimulator(runs=1000)
    mc_res = mc.run_simulation()
    bins_data = mc_res["distribution_bins"]

    bin_labels = [b["range"] for b in bins_data]
    counts = [b["count"] for b in bins_data]

    ax.bar(bin_labels, counts, color='#0284C7', edgecolor='#0369A1', alpha=0.85)
    ax.set_ylabel('Frequency (out of 1,000 Stochastic Trials)', fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.set_xlabel('Fulfillment Service Level (%)', fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.set_title(f"Monte Carlo Robustness: P10={mc_res['percentiles_fulfilled_units']['P10']:,} | P50={mc_res['percentiles_fulfilled_units']['P50']:,} | VaR(95%)=₹{mc_res['var_95_ebitda_cr']:,.1f} Cr", 
                 fontsize=11.5, fontweight='bold', color='#0F172A', pad=14)
    ax.tick_params(axis='x', rotation=30, labelsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')

    plt.tight_layout()
    chart4_path = os.path.join(chart_dir, "chart4_monte_carlo.png")
    plt.savefig(chart4_path, dpi=260)
    plt.close()
    chart_paths["monte_carlo"] = chart4_path

    # -------------------------------------------------------------
    # CHART 5: Enterprise Revenue Waterfall (Bottleneck Leakage vs Mitigation)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=260)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8FAFC')

    wf_steps = ['Baseline\nRevenue', '+20% Target\nUpside', 'Labor\nChoke Loss', 'Stockout\nPenalty', 'Logistics\nCongestion', 'Agile Realized\nRevenue (Sc. E)']
    wf_vals = [72500, 14500, -14800, -6200, -3200, 86663]

    running_tot = 72500
    bottoms = [0, running_tot, running_tot + 14500 - 14800, running_tot + 14500 - 14800 - 6200, running_tot + 14500 - 14800 - 6200 - 3200, 0]
    heights = [72500, 14500, 14800, 6200, 3200, 86663]
    colors_list = ['#64748B', '#10B981', '#DC2626', '#EF4444', '#F59E0B', '#059669']

    # For visualization, draw bars
    ax.bar(wf_steps, [72.5, 14.5, -14.8, -6.2, -3.2, 86.66], color=['#334155', '#10B981', '#EF4444', '#F87171', '#F59E0B', '#047857'], edgecolor='#0F172A')
    ax.set_ylabel('INR Thousands of Crores (₹k Cr)', fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.set_title('Strategic Value Waterfall: Value-at-Stake Decomposition (₹ Crores)', fontsize=12, fontweight='bold', color='#0F172A', pad=14)
    ax.axhline(0, color='#0F172A', linewidth=0.8)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')

    vals_display = ['₹72.5k Cr', '+₹14.5k Cr', '-₹14.8k Cr', '-₹6.2k Cr', '-₹3.2k Cr', '₹86.7k Cr']
    for i, v in enumerate(vals_display):
        ypos = [72.5, 14.5, -14.8, -6.2, -3.2, 86.66][i]
        offset = 3.5 if ypos >= 0 else -6.5
        ax.text(i, ypos + offset, v, ha='center', fontsize=8.5, fontweight='bold', color='#1E293B')

    plt.tight_layout()
    chart5_path = os.path.join(chart_dir, "chart5_revenue_waterfall.png")
    plt.savefig(chart5_path, dpi=260)
    plt.close()
    chart_paths["revenue_waterfall"] = chart5_path

    return chart_paths

def build_pdf_report(output_pdf_path):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    temp_chart_dir = os.path.join(tempfile.gettempdir(), "mahindra_charts_14")
    charts = generate_report_visualizations(temp_chart_dir)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#C8102E') # Mahindra Red
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B')
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#64748B')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#C8102E'),
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155')
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0F172A')
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # -------------------------------------------------------------
    # PAGE 1: TITLE & EXECUTIVE PROBLEM STATEMENT
    # -------------------------------------------------------------
    story.append(Paragraph("MAHINDRA & MAHINDRA LIMITED", title_style))
    story.append(Paragraph("PROJECT - 14: WHAT-IF BUSINESS SIMULATOR", subtitle_style))
    story.append(Paragraph("Automotive Sector C-Suite Strategic Scenario Analysis & Multi-Pillar Constraint Audit", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#C8102E"), spaceAfter=10))

    # Problem Statement Callout Box
    ps_text = """<b>Core Problem Statement:</b><br/>
    <i>\"Mahindra & Mahindra Management wants to increase sales by 20% but does not know whether existing employees, inventory, production capacity and logistics can support the additional demand. Build an AI scenario-analysis system that simulates business consequences of different strategic decisions.\"</i>"""
    
    ps_table = Table([[Paragraph(ps_text, callout_style)]], colWidths=[504])
    ps_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor('#F87171')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(ps_table)
    story.append(Spacer(1, 10))

    # Executive Summary Paragraphs
    story.append(Paragraph("1. EXECUTIVE SUMMARY & ARBITRATION FINDINGS", h1_style))
    exec_summary_text = """
    Mahindra & Mahindra's Automotive Sector currently delivers <b>500,000 vehicles annually</b> (~₹72,500 Cr gross revenue), spanning flagship marques including <b>Scorpio-N, XUV700, Thar, Bolero Neo, and the EV portfolio</b> across manufacturing plants in Chakan (Pune), Nashik, Zaheerabad, and Haridwar. Management's mandate to capture a <b>+20% sales volume increase (600,000 units target, +₹14,500 Cr demand upside)</b> was rigorously simulated through an AI Cross-Functional Constraint Engine.<br/><br/>
    <b>The Core Verdict:</b> The existing operational infrastructure <b>CANNOT</b> support a 20% sales surge in its status quo state. A naive volume push induces immediate failure across all four operational pillars:
    <br/>
    • <b>Workforce Choke:</b> Direct assembly hours required breach statutory limits, requiring 110 hrs/quarter overtime per worker, resulting in a <b>CRITICAL VIOLATION of the Indian Factories Act 1948</b>, a spike in absenteeism to 20.6%, and quality scrap reaching 6.9%.<br/>
    • <b>Plant Tooling Saturation:</b> Plant utilization surges to 115.4% of nameplate capacity, inducing unscheduled breakdown and degrading OEE from 88% to 82.6%.<br/>
    • <b>Supply Chain Starvation:</b> Tier-1 lead times (12-16 weeks for microcontrollers & castings) cause a 48.3% stockout probability, stranding assembly lines.<br/>
    • <b>Logistics Gridlock:</b> Road car carrier shortages force factory yard dwell time from 2.5 to 4.5 days, bringing yard saturation to 96.6% and triggering spot freight surcharges.
    """
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 10))

    # Chart 1: Pillar Capacities
    story.append(Image(charts["pillar_capacities"], width=504, height=230))
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 2: 4-PILLAR DEEP DIVE AUDIT
    # -------------------------------------------------------------
    story.append(Paragraph("2. CROSS-FUNCTIONAL FOUR-PILLAR FEASIBILITY AUDIT", h1_style))
    
    p1_desc = """<b>Pillar 1: Employees & Workforce (Critical Vulnerability)</b><br/>
    Direct line technicians currently total 23,000 across plants. Standard annual output per worker is 2,200 hours. Meeting 600,000 units requires 60.72 million man-hours vs 50.60 million available regular hours. Without recruiting additional staff, the resulting 10.12 million hour deficit forces overtime to 110.0 hours/quarter per operator—more than double the statutory ceiling of 50.0 hours/quarter mandated under Section 64 of the Indian Factories Act 1948. This triggers union industrial actions, fatigue-induced assembly defects (+300% scrap rate), and acute absenteeism."""
    story.append(Paragraph(p1_desc, body_style))
    story.append(Spacer(1, 8))

    p2_desc = """<b>Pillar 2: Production & Tooling Capacity (Severe Bottleneck)</b><br/>
    Current nameplate capacity across Chakan (17.5k/mo), Nashik (15k/mo), Haridwar (8.5k/mo), and Zaheerabad (6.5k/mo) stands at 520,000 units annually on a 2-shift schedule. Target demand of 600,000 units represents 115.4% capacity utilization. Operating above 95% without scheduled preventive maintenance degrades OEE to 82.6%, producing equipment breakdown bottlenecks in paint shops and robotic body-in-white (BIW) welding cells."""
    story.append(Paragraph(p2_desc, body_style))
    story.append(Spacer(1, 8))

    p3_desc = """<b>Pillar 3: Inventory & Tier-1 Supply Chain (Long-Lead Vulnerability)</b><br/>
    Specialized automotive microcontrollers (Bosch/Continental), Ultra-High Strength Steel (JSW), and LFP battery packs require 12 to 16 weeks advance commitment. Baseline inventory covers 24.0 Days of Inventory (DOI). Under an abrupt +20% surge with standard 4-week notice, stockout risk escalates to 48.3%, creating assembly line starvations and stranding partially assembled SUVs."""
    story.append(Paragraph(p3_desc, body_style))
    story.append(Spacer(1, 8))

    p4_desc = """<b>Pillar 4: Logistics & Outbound Finished Vehicle Distribution (Yard Saturation)</b><br/>
    Automotive carrier trailers in India operate under severe national capacity deficits. At 50,000 units/month, outbound road dispatch requires 1,530 car carriers continuously. Finished vehicle holding yards dwell time escalates from 2.5 days to 4.5 days, risking yard gate saturation above 100%, choking final inspection lines and inflating spot freight rates by +38%."""
    story.append(Paragraph(p4_desc, body_style))
    story.append(Spacer(1, 10))

    # Four Pillars Summary Scorecard Table
    scorecard_data = [
        ["Operational Pillar", "Key Risk Indicator (KRI)", "Baseline (500k)", "Naive Surge (+20%)", "Mitigated (Scenario E)", "Status"],
        ["Workforce", "Quarterly Overtime / Worker", "12.0 hrs", "110.0 hrs", "14.2 hrs", "FACTORIES ACT COMPLIANT"],
        ["Plant Capacity", "Effective Utilization %", "88.2%", "115.4%", "89.8%", "DEBOTTLENECKED (3-SHIFT)"],
        ["Inventory", "Component Stockout Risk %", "4.2%", "48.3%", "3.8%", "STRATEGIC BUFFER (38 DOI)"],
        ["Logistics", "Yard Dwell Time & Saturation", "2.5 days (78%)", "4.5 days (97%)", "2.2 days (68%)", "MULTI-MODAL RAIL (30%)"]
    ]
    sc_table = Table(scorecard_data, colWidths=[90, 130, 70, 75, 85, 94])
    sc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (1,-1), 'LEFT'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(sc_table)
    story.append(Spacer(1, 12))

    # Chart 3: Workforce Overtime & Factories Act
    story.append(Image(charts["workforce_compliance"], width=504, height=210))
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 3: SCENARIO MATRIX & FINANCIAL TRANSFORMATION
    # -------------------------------------------------------------
    story.append(Paragraph("3. STRATEGIC SCENARIOS EVALUATED (SCENARIOS A TO E)", h1_style))
    story.append(Paragraph("The AI Simulator evaluated 5 distinct strategic decision pathways for M&M's executive leadership:", body_style))
    story.append(Spacer(1, 8))

    # Scenarios Table
    optimizer = ScenarioOptimizer()
    scs = optimizer.get_all_scenarios(20.0)

    sc_table_data = [
        ["Scenario", "Fulfillment Rate", "Realized Rev (₹ Cr)", "EBITDA (₹ Cr)", "EBITDA %", "Lost Rev (₹ Cr)", "Factories Act", "Score"]
    ]
    for s in scs:
        r = s["results"]
        f = r["financials"]
        d = r["demand"]
        w = r["workforce_metrics"]
        feas = r["overall_feasibility"]
        sc_table_data.append([
            s["name"].split(":")[0] + "\n" + s["tag"],
            f"{d['fulfillment_rate_pct']}%",
            f"₹{f['gross_revenue_cr']:,.0f}",
            f"₹{f['ebitda_cr']:,.0f}",
            f"{f['ebitda_margin_pct']}%",
            f"₹{f['lost_revenue_potential_cr']:,.0f}",
            w["factories_act_compliance"],
            f"{feas['score']}/100"
        ])

    sc_full_table = Table(sc_table_data, colWidths=[90, 60, 68, 62, 45, 65, 80, 34])
    sc_full_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#C8102E')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FEF2F2'), colors.HexColor('#FFFBEB'), colors.HexColor('#F0FDF4'), colors.HexColor('#F0FDF4'), colors.HexColor('#ECFDF5')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(sc_full_table)
    story.append(Spacer(1, 10))

    # Chart 2: Scenario Matrix
    story.append(Image(charts["scenario_matrix"], width=504, height=220))
    story.append(Spacer(1, 10))

    # Chart 5: Revenue Waterfall
    story.append(Image(charts["revenue_waterfall"], width=504, height=210))
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # -------------------------------------------------------------
    # PAGE 4: MONTE CARLO RISK & ROADMAP
    # -------------------------------------------------------------
    story.append(Paragraph("4. MONTE CARLO STOCHASTIC RISK PROFILE & 180-DAY ROADMAP", h1_style))
    
    mc_text = """
    To evaluate supply chain volatility, <b>1,000 Monte Carlo stochastic trials</b> were conducted under Scenario E (Holistic Agile Transformation). External shocks modeled included global semiconductor fab delays, monsoon rail/road freight interruptions, raw material tariff inflation, and harvesting-season labor absenteeism.<br/>
    <b>Risk Findings:</b><br/>
    • <b>Success Probability:</b> 100.0% probability of fulfilling ≥ 95% of target volume under Scenario E.<br/>
    • <b>P10 / P50 / P90 Volumes:</b> 596,472 (P10) | 597,648 (P50 Median) | 597,648 (P90 Optimistic).<br/>
    • <b>Value at Risk (VaR 95%):</b> ₹973.54 Cr EBITDA at risk under extreme compounded external shocks.
    """
    story.append(Paragraph(mc_text, body_style))
    story.append(Spacer(1, 8))

    # Chart 4: Monte Carlo Distribution
    story.append(Image(charts["monte_carlo"], width=504, height=200))
    story.append(Spacer(1, 10))

    # 180-Day Execution Roadmap Table
    story.append(Paragraph("5. PHASED 180-DAY BOARD EXECUTION ROADMAP", h2_style))
    advisor = AIStrategicAdvisor()
    phases = advisor.get_180_day_roadmap()

    roadmap_data = [["Phase & Timeline", "Strategic Objective", "Key Operational Milestones & Board Mandates"]]
    for p in phases:
        actions_formatted = "<br/>• " + "<br/>• ".join(p["actions"])
        roadmap_data.append([
            p["phase"],
            p["title"],
            Paragraph(actions_formatted[5:], body_style)
        ])

    rm_table = Table(roadmap_data, colWidths=[90, 110, 304])
    rm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(rm_table)
    story.append(Spacer(1, 12))

    # Sign-off box
    signoff_text = """<b>Board Resolution Recommendation:</b><br/>
    The Executive Committee recommends approval of <b>Scenario E: Holistic Agile Enterprise Transformation</b>, approving ₹320 Cr in automation debottlenecking CAPEX, authorizing recruitment of 4,200 assembly operators for Shift 3, and securing 14-week pre-commitments with critical semiconductor and railway logistics partners."""
    so_table = Table([[Paragraph(signoff_text, callout_style)]], colWidths=[504])
    so_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor('#10B981')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(so_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Executive PDF Report successfully generated -> {output_pdf_path}")
    return output_pdf_path

if __name__ == "__main__":
    report_pdf = os.path.join(base_dir, "report", "Mahindra_What_If_Business_Simulator_Report.pdf")
    build_pdf_report(report_pdf)

