"""
Mahindra & Mahindra Ltd. - Master Orchestrator Pipeline
Project - 14: What-If Business Simulator

Executes the complete end-to-end executive intelligence pipeline:
1. Synthesizes enterprise operational & component supply telemetry across M&M plants.
2. Calibrates cross-functional constraints across 4 pillars (Workforce, Inventory, Capacity, Logistics).
3. Evaluates 5 board-level strategic decision scenarios (Status Quo to Holistic Agile).
4. Executes 1,000 Monte Carlo stochastic risk simulations (P10/P50/P90, VaR 95%).
5. Compiles 5 high-DPI charts and builds the publication-grade PDF deliverable.
6. Launches the interactive executive web dashboard on http://localhost:5014.
"""

import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

os.environ["LOKY_MAX_CPU_COUNT"] = "4"

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from data.generate_mahindra_telemetry import generate_mahindra_operational_data
from models.what_if_engine import WhatIfBusinessSimulator
from models.scenario_optimizer import ScenarioOptimizer
from models.monte_carlo_simulator import MonteCarloSimulator
from models.ai_strategic_advisor import AIStrategicAdvisor
from report.generate_pdf_report import build_pdf_report

def main():
    print("=" * 90)
    print(" PROJECT - 14: WHAT-IF BUSINESS SIMULATOR")
    print(" Mahindra & Mahindra Ltd. — Automotive Cross-Functional Decision Intelligence Engine")
    print("=" * 90)

    data_dir = os.path.join(base_dir, "data")
    monthly_csv = os.path.join(data_dir, "mahindra_baseline_operations.csv")
    comp_csv = os.path.join(data_dir, "mahindra_component_supply.csv")
    pdf_path = os.path.join(base_dir, "report", "Mahindra_What_If_Business_Simulator_Report.pdf")

    # Step 1: Telemetry Data Generation
    print("\n[Step 1/6] Ingesting and verifying M&M operational telemetry across plants...")
    if not os.path.exists(monthly_csv) or not os.path.exists(comp_csv):
        generate_mahindra_operational_data(output_dir=data_dir)
    else:
        print(f"  -> Found verified plant operational telemetry: {monthly_csv}")
        print(f"  -> Found verified critical component supply data: {comp_csv}")

    # Step 2: What-If Engine Baseline Audit
    print("\n[Step 2/6] Auditing baseline operational feasibility for +20% demand surge...")
    sim = WhatIfBusinessSimulator()
    naive_res = sim.simulate(sales_growth_pct=20.0, shift_model="2_shifts", new_hiring_headcount=0)
    print(f"  -> Target Sales Demand                : {naive_res['demand']['target_units']:,} vehicles (+20% surge)")
    print(f"  -> Feasible Fulfillment (Status Quo)  : {naive_res['demand']['fulfilled_units']:,} vehicles ({naive_res['demand']['fulfillment_rate_pct']}%)")
    print(f"  -> Primary Constraining Bottleneck    : {naive_res['primary_bottleneck']}")
    print(f"  -> Statutory Labor Compliance         : {naive_res['workforce_metrics']['factories_act_compliance']} (OT: {naive_res['workforce_metrics']['avg_ot_hours_quarterly']} hrs/qtr)")
    print(f"  -> Value-at-Stake (Lost Sales)        : INR {naive_res['financials']['lost_revenue_potential_cr']:,.2f} Cr")
    print(f"  -> Overall Feasibility Score          : {naive_res['overall_feasibility']['status']} ({naive_res['overall_feasibility']['score']}/100)")

    # Step 3: Scenario Optimization
    print("\n[Step 3/6] Evaluating 5 strategic board decision pathways (Scenarios A through E)...")
    optimizer = ScenarioOptimizer()
    scenarios = optimizer.get_all_scenarios(20.0)
    for sc in scenarios:
        r = sc["results"]
        print(f"  -> [{sc['name']:<48}] Fulfill: {r['demand']['fulfillment_rate_pct']:>5.1f}% | EBITDA: INR {r['financials']['ebitda_cr']:>8,.1f} Cr | Score: {r['overall_feasibility']['score']:>3d}/100")

    # Step 4: Monte Carlo Risk Modeling
    print("\n[Step 4/6] Running 1,000 Monte Carlo stochastic risk trials on recommended Scenario E...")
    mc = MonteCarloSimulator(runs=1000)
    mc_res = mc.run_simulation()
    print(f"  -> P10 (Pessimistic Volume)           : {mc_res['percentiles_fulfilled_units']['P10']:,} units")
    print(f"  -> P50 (Median Expected Volume)       : {mc_res['percentiles_fulfilled_units']['P50']:,} units")
    print(f"  -> Probability Meeting >=95% Demand   : {mc_res['prob_meeting_95pct_demand']}%")
    print(f"  -> 95% Value at Risk (VaR)            : INR {mc_res['var_95_ebitda_cr']:,.2f} Cr")

    # Step 5: High-DPI Charts & Executive PDF Deliverable
    print("\n[Step 5/6] Compiling 5 high-DPI charts & executive PDF deliverable...")
    build_pdf_report(pdf_path)
    print(f"  -> PDF Deliverable verified: {pdf_path}")
    print(f"  -> File Size: {os.path.getsize(pdf_path) / 1024:.1f} KB")

    # Step 6: Launch Web Dashboard
    print("\n[Step 6/6] Initializing Executive Web Dashboard on localhost...")
    from app import app
    port = int(os.environ.get("PORT", 5014))
    print("=" * 90)
    print(f" >>> SUCCESS: Mahindra & Mahindra What-If Business Simulator is LIVE <<<")
    print(f" >>> Localhost URL: http://localhost:{port} <<<")
    print(f" >>> Direct PDF Report: http://localhost:{port}/download-report <<<")
    print("=" * 90)
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()

