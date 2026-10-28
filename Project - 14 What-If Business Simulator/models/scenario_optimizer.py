"""
Mahindra & Mahindra Ltd. - Strategic Scenario Optimizer
Project - 14: What-If Business Simulator

Compares 5 Distinct Executive Decision Scenarios for M&M's +20% Sales Growth Target:
1. Scenario A: Status Quo Naive Push (Do nothing, push sales targets)
2. Scenario B: Sweat the Assets & Maximum Overtime (Overtime push, spot logistics)
3. Scenario C: Capacity Expansion & 3rd Shift Addition (Shift 3 + 4,600 hires)
4. Scenario D: Multi-Modal Logistics & Supply Buffering (Rail logistics + VMI buffer)
5. Scenario E: Holistic Agile Enterprise Transformation (Recommended Board Protocol)
"""

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from models.what_if_engine import WhatIfBusinessSimulator

class ScenarioOptimizer:
    def __init__(self):
        self.simulator = WhatIfBusinessSimulator()
        
    def get_all_scenarios(self, sales_growth_pct=20.0):
        """
        Runs and returns 5 benchmark strategic decision scenarios.
        """
        scenarios = [
            {
                "id": "scenario_a",
                "name": "Scenario A: Status Quo (Naive Sales Push)",
                "tag": "High Risk / Choke Failure",
                "badge_class": "badge-danger",
                "description": "Mandates a 20% sales volume increase across dealers without operational investments, hiring, or supply chain advance commitments.",
                "params": {
                    "sales_growth_pct": sales_growth_pct,
                    "shift_model": "2_shifts",
                    "new_hiring_headcount": 0,
                    "debottlenecking_capex_cr": 0.0,
                    "inventory_buffer_target_days": 24.0,
                    "supplier_advance_commitment_wks": 4,
                    "rail_logistics_ratio_pct": 14.0,
                    "long_term_carrier_contract_pct": 70.0
                }
            },
            {
                "id": "scenario_b",
                "name": "Scenario B: Asset Sweating & Overtime Push",
                "tag": "Regulatory & Quality Hazard",
                "badge_class": "badge-warning",
                "description": "Attempts to achieve +20% demand by running double shifts with maximum overtime and buying spot trucking capacity.",
                "params": {
                    "sales_growth_pct": sales_growth_pct,
                    "shift_model": "2_shifts_max_ot",
                    "new_hiring_headcount": 1200,
                    "debottlenecking_capex_cr": 50.0,
                    "inventory_buffer_target_days": 20.0,
                    "supplier_advance_commitment_wks": 6,
                    "rail_logistics_ratio_pct": 14.0,
                    "long_term_carrier_contract_pct": 50.0
                }
            },
            {
                "id": "scenario_c",
                "name": "Scenario C: Shift 3 Addition & Plant Hiring",
                "tag": "Operationally Viable",
                "badge_class": "badge-info",
                "description": "Transitions Chakan and Nashik plants to a 3-shift 24-hour manufacturing cycle, recruiting 4,600 shop-floor technicians.",
                "params": {
                    "sales_growth_pct": sales_growth_pct,
                    "shift_model": "3_shifts",
                    "new_hiring_headcount": 4600,
                    "debottlenecking_capex_cr": 120.0,
                    "inventory_buffer_target_days": 26.0,
                    "supplier_advance_commitment_wks": 8,
                    "rail_logistics_ratio_pct": 18.0,
                    "long_term_carrier_contract_pct": 75.0
                }
            },
            {
                "id": "scenario_d",
                "name": "Scenario D: Multi-Modal Rail & Strategic Buffering",
                "tag": "Resilience Focused",
                "badge_class": "badge-primary",
                "description": "Prioritizes supply chain buffering (35 days DOI) and shifts finished SUV transport to dedicated Indian Railways auto-rakes (28% rail).",
                "params": {
                    "sales_growth_pct": sales_growth_pct,
                    "shift_model": "3_shifts",
                    "new_hiring_headcount": 3800,
                    "debottlenecking_capex_cr": 180.0,
                    "inventory_buffer_target_days": 35.0,
                    "supplier_advance_commitment_wks": 12,
                    "rail_logistics_ratio_pct": 28.0,
                    "long_term_carrier_contract_pct": 85.0
                }
            },
            {
                "id": "scenario_e",
                "name": "Scenario E: Holistic Agile Transformation (Recommended)",
                "tag": "Optimal Board Protocol",
                "badge_class": "badge-success",
                "description": "Synergistic execution: 3rd shift with 4,200 trained technicians, ₹320 Cr robotic automation, 14-wk Tier-1 pre-commitments, and 30% rail transport.",
                "params": {
                    "sales_growth_pct": sales_growth_pct,
                    "shift_model": "hybrid_agile",
                    "new_hiring_headcount": 4200,
                    "debottlenecking_capex_cr": 320.0,
                    "inventory_buffer_target_days": 38.0,
                    "supplier_advance_commitment_wks": 14,
                    "rail_logistics_ratio_pct": 30.0,
                    "long_term_carrier_contract_pct": 90.0
                }
            }
        ]

        evaluated_scenarios = []
        for sc in scenarios:
            result = self.simulator.simulate(**sc["params"])
            sc_data = {
                "id": sc["id"],
                "name": sc["name"],
                "tag": sc["tag"],
                "badge_class": sc["badge_class"],
                "description": sc["description"],
                "params": sc["params"],
                "results": result
            }
            evaluated_scenarios.append(sc_data)

        return evaluated_scenarios

if __name__ == "__main__":
    opt = ScenarioOptimizer()
    scs = opt.get_all_scenarios(20.0)
    print("=" * 80)
    print(" MAHINDRA & MAHINDRA - 5 STRATEGIC SCENARIOS EVALUATED (+20% SURGE)")
    print("=" * 80)
    for s in scs:
        r = s["results"]
        print(f"[{s['name']}]")
        print(f"  Fulfillment: {r['demand']['fulfilled_units']:,} / {r['demand']['target_units']:,} ({r['demand']['fulfillment_rate_pct']}%)")
        print(f"  Bottleneck : {r['primary_bottleneck']}")
        print(f"  EBITDA     : INR {r['financials']['ebitda_cr']:,.2f} Cr ({r['financials']['ebitda_margin_pct']}%) | Incremental: +INR {r['financials']['incremental_ebitda_cr']:,.2f} Cr")
        print(f"  Feasibility: {r['overall_feasibility']['status']} ({r['overall_feasibility']['score']}/100)")
        print("-" * 80)
