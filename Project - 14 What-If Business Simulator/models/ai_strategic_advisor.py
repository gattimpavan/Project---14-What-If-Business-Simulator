"""
Mahindra & Mahindra Ltd. - AI Strategic Advisor & Executive Terminal
Project - 14: What-If Business Simulator

Grounds AI decision intelligence into M&M's cross-functional reality:
- Answers executive inquiries on workforce overtime, line capacity, logistics gridlock, and component buffers.
- Generates C-suite strategic memos, board resolutions, and 180-day operational execution roadmaps.
- Evaluates sensitivity across arbitrary parameter combinations submitted by management.
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

class AIStrategicAdvisor:
    def __init__(self):
        self.simulator = WhatIfBusinessSimulator()

    def generate_executive_memo(self, sim_result):
        """
        Synthesizes a board-level executive memo evaluating the current simulation state.
        """
        d = sim_result["demand"]
        f = sim_result["financials"]
        p = sim_result["plant_metrics"]
        w = sim_result["workforce_metrics"]
        inv = sim_result["inventory_metrics"]
        log = sim_result["logistics_metrics"]
        bottleneck = sim_result["primary_bottleneck"]
        feasibility = sim_result["overall_feasibility"]

        memo = f"""
EXECUTIVE STRATEGIC MEMO: M&M AUTOMOTIVE 20% GROWTH FEASIBILITY AUDIT
CONFIDENTIAL // FOR THE BOARD OF DIRECTORS & EXECUTIVE COMMITTEE

1. EXECUTIVE DIAGNOSIS & BOTTLENECK ARBITRATION
   - Target Sales Demand: {d['target_units']:,} vehicles (+{sim_result['inputs']['sales_growth_pct']}% surge over 500,000 baseline).
   - Fulfilled Volume: {d['fulfilled_units']:,} vehicles ({d['fulfillment_rate_pct']}% Service Level).
   - Unfulfilled Demand Gap: {d['unfulfilled_units']:,} vehicles -> Representing INR {f['lost_revenue_potential_cr']:,.2f} Cr in uncaptured revenue.
   - Primary Enterprise Constraint: [{bottleneck.upper()}].
   - Overall Enterprise Feasibility Status: {feasibility['status']} ({feasibility['score']}/100).

2. CROSS-FUNCTIONAL PILLAR INTEGRITY AUDIT:
   a. Workforce & Industrial Relations:
      - Total Headcount: {w['total_workforce']:,} technicians.
      - Projected Quarterly Overtime: {w['avg_ot_hours_quarterly']} hrs/worker.
      - Regulatory Legal Status: [{w['factories_act_compliance']}] under Indian Factories Act 1948 (Section 64 limit: 50 hrs/qtr).
      - Absenteeism: {w['absenteeism_pct']}% | Assembly Scrap Rate: {w['scrap_rate_pct']}%.

   b. Production & Plant Assets:
      - Effective Nameplate: {p['effective_nameplate_capacity']:,} units/year across Chakan, Nashik, Zaheerabad, and Haridwar.
      - Operating OEE: {p['simulated_oee_pct']}% | Asset Utilization: {p['plant_utilization_pct']}%.

   c. Inventory & Tier-1 Supply Chain:
      - Component Stockout Risk: {inv['stockout_probability_pct']}% probability of line stoppages.
      - Critical Microcontroller & Battery Buffer: {inv['doi_target_days']} Days of Inventory (DOI).
      - Working Capital Buffer Financed: INR {inv['working_capital_buffer_cr']:,.2f} Cr.

   d. Logistics, Yard Operations & Outbound Transport:
      - Factory Yard Dwell Time: {log['yard_dwell_days']} Days (Baseline: 2.5 Days).
      - Finished Vehicle Yard Saturation: {log['yard_saturation_pct']}%.
      - Modal Split: {log['rail_share_pct']}% Indian Railways AFTO Rakes vs Road Car Carriers.

3. FINANCIAL P&L TRANSFORMATION:
   - Realized Gross Revenue: INR {f['gross_revenue_cr']:,.2f} Cr.
   - Total Cost of Goods Sold (COGS): INR {f['cogs_cr']:,.2f} Cr.
   - Operating EBITDA: INR {f['ebitda_cr']:,.2f} Cr ({f['ebitda_margin_pct']}% Margin).
   - Incremental EBITDA over Baseline: +INR {f['incremental_ebitda_cr']:,.2f} Cr.
   - Net Profit After Tax (PAT): INR {f['net_profit_cr']:,.2f} Cr.
   - Return on Investment (ROI): {f['roi_pct']}%.
"""
        return memo.strip()

    def answer_query(self, query_text, current_params):
        """
        AI Business Analyst terminal answering queries based on current simulation state.
        """
        sim_res = self.simulator.simulate(**current_params)
        q = query_text.lower().strip()

        if "employee" in q or "workforce" in q or "overtime" in q or "labor" in q or "factories act" in q:
            w = sim_res["workforce_metrics"]
            status = w["factories_act_compliance"]
            ot = w["avg_ot_hours_quarterly"]
            return {
                "category": "Workforce & Labor Compliance",
                "headline": f"Workforce Status: {status} (OT: {ot} hrs/qtr)",
                "details": f"Under current parameters, total workforce is {w['total_workforce']:,} technicians. With this schedule, workers average {ot} hours of overtime per quarter (statutory Factories Act 1948 maximum is 50.0 hrs/qtr). Fatigue drives absenteeism to {w['absenteeism_pct']}% and scrap defect rates to {w['scrap_rate_pct']}%. To restore compliance, management must transition to a 3-shift model and onboard at least 4,200 additional assembly operators.",
                "kpis": [
                    {"label": "Factories Act Status", "val": status, "alert": status != "COMPLIANT"},
                    {"label": "Quarterly Overtime", "val": f"{ot} hrs/worker", "alert": ot > 50.0},
                    {"label": "Absenteeism Rate", "val": f"{w['absenteeism_pct']}%", "alert": w['absenteeism_pct'] > 8.0},
                    {"label": "Assembly Scrap Rate", "val": f"{w['scrap_rate_pct']}%", "alert": w['scrap_rate_pct'] > 2.5}
                ]
            }

        elif "inventory" in q or "semiconductor" in q or "supplier" in q or "lead time" in q or "stockout" in q:
            inv = sim_res["inventory_metrics"]
            return {
                "category": "Inventory & Supply Chain Feasibility",
                "headline": f"Stockout Risk: {inv['stockout_probability_pct']}% | Buffer: {inv['doi_target_days']} Days DOI",
                "details": f"Tier-1 suppliers (Bosch, Continental, JSW Steel) require 12 to 16 weeks advance commitment for a 20% automotive surge. With {sim_res['inputs']['supplier_advance_commitment_wks']} weeks notice, component stockout risk stands at {inv['stockout_probability_pct']}%, causing an estimated production disruption of {inv['stockout_disruption_units']:,} vehicles. Financing a strategic buffer of 38 days requires INR {inv['working_capital_buffer_cr']:,.2f} Cr working capital.",
                "kpis": [
                    {"label": "Stockout Risk", "val": f"{inv['stockout_probability_pct']}%", "alert": inv['stockout_probability_pct'] > 15.0},
                    {"label": "Days of Inventory", "val": f"{inv['doi_target_days']} Days", "alert": inv['doi_target_days'] < 25.0},
                    {"label": "Disruption Loss", "val": f"{inv['stockout_disruption_units']:,} units", "alert": inv['stockout_disruption_units'] > 5000},
                    {"label": "Working Capital Req.", "val": f"INR {inv['working_capital_buffer_cr']:,.1f} Cr", "alert": False}
                ]
            }

        elif "logistics" in q or "rail" in q or "carrier" in q or "yard" in q or "freight" in q:
            log = sim_res["logistics_metrics"]
            return {
                "category": "Logistics & Outbound Distribution",
                "headline": f"Yard Dwell: {log['yard_dwell_days']} Days | Saturation: {log['yard_saturation_pct']}%",
                "details": f"Road car carrier availability in India is severely constrained. With current dispatch splits ({log['rail_share_pct']}% rail rakes), plant yard dwell time reaches {log['yard_dwell_days']} days against a 2.5-day baseline. Yard saturation is at {log['yard_saturation_pct']}%. Saturation above 100% blocks plant exit ramps. Expanding Indian Railways AFTO rake movements to 30% and locking 90% long-term carrier contracts is vital to avoid gridlock.",
                "kpis": [
                    {"label": "Yard Dwell Time", "val": f"{log['yard_dwell_days']} Days", "alert": log['yard_dwell_days'] > 4.0},
                    {"label": "Yard Saturation", "val": f"{log['yard_saturation_pct']}%", "alert": log['yard_saturation_pct'] > 90.0},
                    {"label": "Rail Rake Share", "val": f"{log['rail_share_pct']}%", "alert": log['rail_share_pct'] < 25.0},
                    {"label": "Logistics Score", "val": f"{log['logistics_health_score']}/100", "alert": log['logistics_health_score'] < 70}
                ]
            }

        elif "capacity" in q or "plant" in q or "oee" in q or "tooling" in q or "chakan" in q:
            p = sim_res["plant_metrics"]
            return {
                "category": "Production & Plant Capacity",
                "headline": f"Plant Utilization: {p['plant_utilization_pct']}% | Operating OEE: {p['simulated_oee_pct']}%",
                "details": f"M&M's rated nameplate capacity under 2 shifts is 520,000 units. Attempting 600,000 units without a 3rd shift or debottlenecking forces utilization to {p['plant_utilization_pct']}%, inducing maintenance deferrals and dropping OEE to {p['simulated_oee_pct']}%. A capital allocation of INR 320 Cr for body-shop robotics and line speed re-balancing unlocks 665,000 unit effective capacity.",
                "kpis": [
                    {"label": "Capacity Utilization", "val": f"{p['plant_utilization_pct']}%", "alert": p['plant_utilization_pct'] > 95.0},
                    {"label": "Effective Nameplate", "val": f"{p['effective_nameplate_capacity']:,} units", "alert": False},
                    {"label": "Operating OEE", "val": f"{p['simulated_oee_pct']}%", "alert": p['simulated_oee_pct'] < 82.0},
                    {"label": "Plant Health Score", "val": f"{p['plant_health_score']}/100", "alert": p['plant_health_score'] < 70}
                ]
            }

        else: # Financial & strategic summary
            f = sim_res["financials"]
            d = sim_res["demand"]
            return {
                "category": "Enterprise Strategic P&L Synthesis",
                "headline": f"EBITDA: INR {f['ebitda_cr']:,.2f} Cr ({f['ebitda_margin_pct']}%) | Fulfillment: {d['fulfillment_rate_pct']}%",
                "details": f"At +{sim_res['inputs']['sales_growth_pct']}% demand surge, M&M realizes INR {f['gross_revenue_cr']:,.2f} Cr from {d['fulfilled_units']:,} vehicles. Net profit after tax reaches INR {f['net_profit_cr']:,.2f} Cr. Unfulfilled backlog stands at {d['unfulfilled_units']:,} vehicles (INR {f['lost_revenue_potential_cr']:,.2f} Cr lost). Primary bottleneck constraining the system is: {sim_res['primary_bottleneck']}.",
                "kpis": [
                    {"label": "Gross Realized Revenue", "val": f"INR {f['gross_revenue_cr']:,.1f} Cr", "alert": False},
                    {"label": "Incremental EBITDA", "val": f"+INR {f['incremental_ebitda_cr']:,.1f} Cr", "alert": f['incremental_ebitda_cr'] < 0},
                    {"label": "Lost Sales Potential", "val": f"INR {f['lost_revenue_potential_cr']:,.1f} Cr", "alert": f['lost_revenue_potential_cr'] > 2000},
                    {"label": "Capital ROI", "val": f"{f['roi_pct']}%", "alert": False}
                ]
            }

    def get_180_day_roadmap(self):
        """
        Returns structured 180-day phased execution milestones for executive decision makers.
        """
        return [
            {
                "phase": "Phase 1: Days 1 - 30",
                "title": "Immediate Contractual Locks & Regulatory Clearance",
                "actions": [
                    "Issue 14-week firm purchase orders to Tier-1 suppliers (Bosch, Continental, JSW Steel) for long-lead microcontrollers and stampings.",
                    "Sign multi-modal freight contracts with Indian Railways (AFTO) securing 28 monthly dedicated auto-rakes.",
                    "Initiate recruitment drive for 4,200 assembly operators across Chakan and Nashik industrial zones.",
                    "Submit 3rd shift operational notices to State Directorate of Industrial Safety & Health (DISH) ensuring Factories Act 1948 compliance."
                ]
            },
            {
                "phase": "Phase 2: Days 31 - 90",
                "title": "Workforce Onboarding & Plant Tooling Debottlenecking",
                "actions": [
                    "Complete 4-week vocational assembly training and robotic cell safety certification for the first batch of 2,500 new technicians.",
                    "Deploy ₹320 Cr debottlenecking CAPEX: install automated robotic spot-welding stations and reduce takt time to 58 seconds at Chakan.",
                    "Establish 3 strategic regional vehicle holding yards (Nagpur, NCR, Bengaluru) to de-congest plant dispatch yards.",
                    "Build up 35-day safety buffer for critical microcontrollers and battery cells."
                ]
            },
            {
                "phase": "Phase 3: Days 91 - 180",
                "title": "Full 3-Shift Commercial Scaling & Equilibrium",
                "actions": [
                    "Activate 24/7 3-shift production schedule across Scorpio-N, XUV700, and Thar lines.",
                    "Scale rail dispatch to 30% of total outbound vehicle movement, stabilizing road carrier freight costs.",
                    "Achieve 50,000 monthly vehicle run-rate (600,000 annualized) with zero Factories Act overtime violations.",
                    "Realize full annual EBITDA accretion of +₹6,958 Cr with 99.6% customer order fulfillment."
                ]
            }
        ]

if __name__ == "__main__":
    advisor = AIStrategicAdvisor()
    res = advisor.simulator.simulate()
    memo = advisor.generate_executive_memo(res)
    print(memo)

