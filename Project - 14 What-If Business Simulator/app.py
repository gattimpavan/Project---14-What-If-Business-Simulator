"""
Mahindra & Mahindra Ltd. - Executive Decision Intelligence Engine
Flask Application & REST API Server (Port 5014)
Project - 14: What-If Business Simulator

Serves:
- Executive Glassmorphic What-If Decision Dashboard
- Real-Time Cross-Functional Constraint Simulation Engine (4 Pillars)
- 5 Pre-Configured Board Strategic Scenarios (A through E)
- Monte Carlo 1,000 Stochastic Risk Analysis Engine
- Grounded AI Business Analyst Natural Language Terminal
- 180-Day Executive Operational Roadmap
- High-Resolution PDF Report Download (/download-report)
"""

import os
import sys
import json
from flask import Flask, render_template, jsonify, request, send_file

# Add project root to sys.path
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from models.what_if_engine import WhatIfBusinessSimulator
from models.scenario_optimizer import ScenarioOptimizer
from models.monte_carlo_simulator import MonteCarloSimulator
from models.ai_strategic_advisor import AIStrategicAdvisor

app = Flask(__name__, static_folder="static", template_folder="templates")

simulator = WhatIfBusinessSimulator()
optimizer = ScenarioOptimizer()
monte_carlo = MonteCarloSimulator(runs=1000)
advisor = AIStrategicAdvisor()

REPORT_PATH = os.path.join(base_dir, "report", "Mahindra_What_If_Business_Simulator_Report.pdf")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    data = request.get_json() or {}
    try:
        sales_growth_pct = float(data.get("sales_growth_pct", 20.0))
        shift_model = str(data.get("shift_model", "2_shifts"))
        new_hiring_headcount = int(data.get("new_hiring_headcount", 0))
        debottlenecking_capex_cr = float(data.get("debottlenecking_capex_cr", 0.0))
        inventory_buffer_target_days = float(data.get("inventory_buffer_target_days", 24.0))
        supplier_advance_commitment_wks = int(data.get("supplier_advance_commitment_wks", 4))
        rail_logistics_ratio_pct = float(data.get("rail_logistics_ratio_pct", 14.0))
        long_term_carrier_contract_pct = float(data.get("long_term_carrier_contract_pct", 70.0))

        result = simulator.simulate(
            sales_growth_pct=sales_growth_pct,
            shift_model=shift_model,
            new_hiring_headcount=new_hiring_headcount,
            debottlenecking_capex_cr=debottlenecking_capex_cr,
            inventory_buffer_target_days=inventory_buffer_target_days,
            supplier_advance_commitment_wks=supplier_advance_commitment_wks,
            rail_logistics_ratio_pct=rail_logistics_ratio_pct,
            long_term_carrier_contract_pct=long_term_carrier_contract_pct
        )
        return jsonify({"success": True, "simulation": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/scenarios", methods=["GET"])
def api_scenarios():
    growth = float(request.args.get("growth", 20.0))
    scenarios = optimizer.get_all_scenarios(sales_growth_pct=growth)
    return jsonify({"success": True, "scenarios": scenarios})

@app.route("/api/monte-carlo", methods=["POST"])
def api_monte_carlo():
    data = request.get_json() or {}
    try:
        mc_result = monte_carlo.run_simulation(data if data else None)
        return jsonify({"success": True, "monte_carlo": mc_result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/ask-ai", methods=["POST"])
def api_ask_ai():
    data = request.get_json() or {}
    query = data.get("query", "Can existing employees support 20% demand?")
    params = data.get("params", {
        "sales_growth_pct": 20.0,
        "shift_model": "2_shifts",
        "new_hiring_headcount": 0,
        "debottlenecking_capex_cr": 0.0,
        "inventory_buffer_target_days": 24.0,
        "supplier_advance_commitment_wks": 4,
        "rail_logistics_ratio_pct": 14.0,
        "long_term_carrier_contract_pct": 70.0
    })
    response = advisor.answer_query(query, params)
    return jsonify({"success": True, "response": response})

@app.route("/api/roadmap", methods=["GET"])
def api_roadmap():
    roadmap = advisor.get_180_day_roadmap()
    return jsonify({"success": True, "roadmap": roadmap})

@app.route("/download-report")
def download_report():
    if not os.path.exists(REPORT_PATH):
        from report.generate_pdf_report import build_pdf_report
        build_pdf_report(REPORT_PATH)
    return send_file(REPORT_PATH, as_attachment=True, download_name="Mahindra_What_If_Business_Simulator_Report.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5014))
    print(f"Starting Mahindra & Mahindra What-If Business Simulator on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
