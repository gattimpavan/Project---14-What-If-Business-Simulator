"""
Mahindra & Mahindra Ltd. - AI What-If Scenario Analysis & Constraint Engine
Project - 14: What-If Business Simulator

Simulates the operational and financial consequences of sales growth targets (+20% surge)
across 4 interconnected enterprise pillars:
1. Employees & Workforce (headcount, overtime, absenteeism, scrap, Factories Act 1948 compliance)
2. Inventory & Supply Chain (days of inventory, Tier-1 lead times, stockout risk, working capital)
3. Production & Plant Capacity (nameplate capacity, OEE, shift model, takt time, maintenance)
4. Logistics & Distribution (car carrier fleet, rail rakes, yard dwell, spot freight penalties)
"""

import sys
import math
import numpy as np
import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

class WhatIfBusinessSimulator:
    def __init__(self):
        # Baseline M&M Automotive Enterprise Parameters (Annualized)
        self.baseline_annual_demand = 500000          # units/year (~41,667/month)
        self.baseline_nameplate_capacity = 520000     # units/year (2 shifts, 6 days/wk)
        self.baseline_oee = 0.88                      # 88% Overall Equipment Effectiveness
        self.baseline_workforce_headcount = 23000     # 23,000 direct assembly technicians
        self.baseline_labor_hours_per_unit = 101.2    # Direct labor man-hours per SUV
        self.baseline_avg_selling_price_lakhs = 14.5  # ₹14.5 Lakhs blended ASP per vehicle
        self.baseline_doi = 24.0                      # Days of Inventory (DOI)
        self.baseline_yard_dwell_days = 2.5           # Outbound yard dwell
        self.baseline_carrier_capacity_monthly = 37000 # Car carrier capacity
        self.baseline_rail_share_pct = 14.0           # 14% dispatch via rail rakes
        self.factories_act_max_quarterly_ot = 50.0    # 50 hrs/quarter legal overtime limit
        
    def simulate(self, 
                 sales_growth_pct=20.0,
                 shift_model="2_shifts",              # '2_shifts', '2_shifts_max_ot', '3_shifts', 'hybrid_agile'
                 new_hiring_headcount=0,              # Additional permanent/contract hires
                 debottlenecking_capex_cr=0.0,        # Plant tooling / automation capex in ₹ Cr
                 inventory_buffer_target_days=24.0,   # Target raw material buffer
                 supplier_advance_commitment_wks=4,   # Weeks advance PO notice given to Tier-1
                 rail_logistics_ratio_pct=14.0,       # Outbound rail share (AFTO rakes)
                 long_term_carrier_contract_pct=70.0  # % of car carriers locked on fixed contract
                 ):
        """
        Executes a holistic cross-functional constraint simulation.
        Returns a comprehensive dictionary containing pillar feasibility audits,
        bottleneck diagnostics, financial P&L impact, and risk flags.
        """
        # 1. Demand Sizing
        target_demand_units = int(self.baseline_annual_demand * (1.0 + sales_growth_pct / 100.0))
        target_monthly_demand = target_demand_units / 12.0
        incremental_demand_units = target_demand_units - self.baseline_annual_demand

        # -------------------------------------------------------------
        # PILLAR 1: PRODUCTION & PLANT CAPACITY CONSTRAINT
        # -------------------------------------------------------------
        # Shift configuration capacity multiplier
        shift_capacity_multiplier = {
            "2_shifts": 1.0,
            "2_shifts_max_ot": 1.06,
            "3_shifts": 1.25,        # 3rd shift adds +25% plant operating time
            "hybrid_agile": 1.28     # 3rd shift + automated modular lines
        }.get(shift_model, 1.0)

        # Capex debottlenecking boost: ₹100 Cr yields ~2.5% throughput via robotic cells & takt reduction
        capex_throughput_boost = min(0.12, (debottlenecking_capex_cr / 100.0) * 0.025)
        
        effective_annual_nameplate = self.baseline_nameplate_capacity * shift_capacity_multiplier * (1.0 + capex_throughput_boost)
        
        # OEE degradation if asset is overstrained without planned maintenance windows
        raw_capacity_load = target_demand_units / effective_annual_nameplate
        if raw_capacity_load > 1.02 and shift_model != "hybrid_agile":
            oee_penalty = min(0.12, (raw_capacity_load - 1.0) * 0.35)
        else:
            oee_penalty = 0.0
        simulated_oee = max(0.74, self.baseline_oee - oee_penalty)
        
        plant_achievable_capacity = int(effective_annual_nameplate * (simulated_oee / self.baseline_oee))
        plant_utilization_pct = round((target_demand_units / effective_annual_nameplate) * 100.0, 1)

        # -------------------------------------------------------------
        # PILLAR 2: EMPLOYEES & WORKFORCE CONSTRAINT
        # -------------------------------------------------------------
        total_workforce = self.baseline_workforce_headcount + new_hiring_headcount
        standard_annual_hours_per_worker = 2200.0 # ~44 hrs/wk * 50 weeks
        available_regular_labor_hours = total_workforce * standard_annual_hours_per_worker
        
        # Required labor hours to hit target demand
        required_labor_hours = target_demand_units * self.baseline_labor_hours_per_unit
        
        # Overtime requirement
        labor_hours_deficit = required_labor_hours - available_regular_labor_hours
        if labor_hours_deficit > 0:
            avg_ot_hours_per_worker_annual = labor_hours_deficit / total_workforce
            avg_ot_hours_per_worker_quarterly = avg_ot_hours_per_worker_annual / 4.0
            avg_ot_hours_per_worker_monthly = avg_ot_hours_per_worker_annual / 12.0
        else:
            avg_ot_hours_per_worker_annual = 0.0
            avg_ot_hours_per_worker_quarterly = 0.0
            avg_ot_hours_per_worker_monthly = 0.0

        # Factories Act 1948 Compliance Check (Section 64: Max 50 hrs/quarter OT)
        factories_act_breach = avg_ot_hours_per_worker_quarterly > self.factories_act_max_quarterly_ot
        regulatory_compliance_risk = "CRITICAL VIOLATION" if avg_ot_hours_per_worker_quarterly > 75.0 else (
            "NON-COMPLIANT" if factories_act_breach else "COMPLIANT"
        )

        # Worker fatigue curves: Excessive overtime spikes absenteeism & scrap
        fatigue_factor = max(0.0, avg_ot_hours_per_worker_quarterly - 30.0) / 10.0
        simulated_absenteeism_pct = round(6.2 + (fatigue_factor * 1.8), 2)
        simulated_scrap_rate_pct = round(1.7 + (fatigue_factor * 0.65), 2)
        
        # Max feasible production constrained by workforce:
        effective_active_workforce = total_workforce * (1.0 - simulated_absenteeism_pct / 100.0)
        # Under legal overtime or emergency tolerance (capped at max 60 hrs/quarter OT allowable before total strike/halt)
        max_allowable_labor_hours = effective_active_workforce * (standard_annual_hours_per_worker + (self.factories_act_max_quarterly_ot * 4.0))
        workforce_achievable_units = int(max_allowable_labor_hours / self.baseline_labor_hours_per_unit)

        # -------------------------------------------------------------
        # PILLAR 3: INVENTORY & SUPPLY CHAIN CONSTRAINT
        # -------------------------------------------------------------
        # Tier-1 supplier response curve: Suppliers need advance commitment (12-16 weeks for microcontrollers & castings)
        supplier_lead_time_gap = max(0, 12 - supplier_advance_commitment_wks)
        supplier_surge_capacity_penalty = (supplier_lead_time_gap / 12.0) * 0.22 # up to 22% component deficit
        
        supplier_max_deliverable_units = int(self.baseline_annual_demand * (1.0 + (sales_growth_pct / 100.0) * (1.0 - supplier_surge_capacity_penalty)))
        
        # Buffer stock adequacy
        stockout_probability_pct = round(min(65.0, max(2.5, (1.0 - (supplier_advance_commitment_wks / 14.0)) * 48.0 + (sales_growth_pct - 10.0) * 1.4)), 1)
        if supplier_advance_commitment_wks >= 12 and inventory_buffer_target_days >= 35:
            stockout_probability_pct = round(stockout_probability_pct * 0.2, 1) # Mitigated

        stockout_disruption_loss_units = int(target_demand_units * (stockout_probability_pct / 100.0) * 0.14)
        inventory_achievable_units = max(self.baseline_annual_demand, supplier_max_deliverable_units - stockout_disruption_loss_units)

        # -------------------------------------------------------------
        # PILLAR 4: LOGISTICS & DISTRIBUTION FLEET CONSTRAINT
        # -------------------------------------------------------------
        # Outbound vehicle movement
        monthly_units_to_ship = target_demand_units / 12.0
        rail_monthly_units = monthly_units_to_ship * (rail_logistics_ratio_pct / 100.0)
        road_monthly_units = monthly_units_to_ship - rail_monthly_units
        
        # Car carrier demand (avg 8 cars per road carrier, 3.5 trips/month per carrier)
        carrier_trips_needed = road_monthly_units / 8.0
        carriers_required = carrier_trips_needed / 3.5
        carrier_shortage = max(0.0, carriers_required - (self.baseline_carrier_capacity_monthly / 8.0 / 3.5))
        
        # Yard Dwell Time escalation due to logistics carrier deficit
        logistics_strain_ratio = carriers_required / (self.baseline_carrier_capacity_monthly / 8.0 / 3.5)
        if logistics_strain_ratio > 1.0:
            simulated_yard_dwell_days = round(self.baseline_yard_dwell_days + (logistics_strain_ratio - 1.0) * 12.5, 1)
            yard_saturation_pct = round(min(145.0, 78.0 + (logistics_strain_ratio - 1.0) * 115.0), 1)
        else:
            simulated_yard_dwell_days = round(self.baseline_yard_dwell_days * (1.0 - (rail_logistics_ratio_pct - 14.0) * 0.015), 1)
            yard_saturation_pct = round(max(55.0, 78.0 - (rail_logistics_ratio_pct - 14.0) * 0.8), 1)

        # Severe yard saturation blocks plant exit gates, curtailing plant throughput
        if yard_saturation_pct > 100.0:
            logistics_choke_penalty = (yard_saturation_pct - 100.0) * 0.0075
        else:
            logistics_choke_penalty = 0.0
            
        logistics_achievable_units = int(target_demand_units * (1.0 - logistics_choke_penalty))

        # -------------------------------------------------------------
        # ENTERPRISE CONVERGENCE & BOTTLENECK ARBITRATION
        # -------------------------------------------------------------
        # Actual units produced & fulfilled is the MINIMUM across all 4 operational pillars
        fulfilled_units = min(
            target_demand_units,
            plant_achievable_capacity,
            workforce_achievable_units,
            inventory_achievable_units,
            logistics_achievable_units
        )
        unfulfilled_backlog_units = target_demand_units - fulfilled_units
        fulfillment_service_level_pct = round((fulfilled_units / target_demand_units) * 100.0, 1)

        # Identify Primary Enterprise Bottleneck
        pillar_capacities = {
            "Plant & Tooling Capacity": plant_achievable_capacity,
            "Workforce & Labor Hours": workforce_achievable_units,
            "Inventory & Component Supply": inventory_achievable_units,
            "Logistics & Yard Clearance": logistics_achievable_units
        }
        primary_bottleneck = min(pillar_capacities, key=pillar_capacities.get) if fulfilled_units < target_demand_units else "None (Target Fully Feasible)"

        # -------------------------------------------------------------
        # FINANCIAL P&L & VALUE-AT-STAKE MODELING (INR Crores)
        # -------------------------------------------------------------
        gross_fulfilled_revenue_cr = round((fulfilled_units * self.baseline_avg_selling_price_lakhs * 100000) / 1e7, 2)
        lost_potential_revenue_cr = round((unfulfilled_backlog_units * self.baseline_avg_selling_price_lakhs * 100000) / 1e7, 2)
        
        # Direct COGS: ~70.5% base + scrap penalty
        cogs_rate = 0.705 + (simulated_scrap_rate_pct - 1.7) * 0.009
        total_cogs_cr = round(gross_fulfilled_revenue_cr * cogs_rate, 2)

        # Labor OPEX: Base wages + Overtime (1.5x) + New Hire Onboarding
        base_annual_wage_per_worker = 384000 # ₹3.84 Lakhs/year
        new_hire_training_cost = 45000       # ₹45k one-time per new hire
        
        base_labor_cost_cr = (total_workforce * base_annual_wage_per_worker) / 1e7
        ot_hourly_rate = 280.0 # ₹280/hr
        ot_expenditure_cr = (total_workforce * avg_ot_hours_per_worker_annual * ot_hourly_rate) / 1e7
        hiring_training_cost_cr = (new_hiring_headcount * new_hire_training_cost) / 1e7
        total_labor_cost_cr = round(base_labor_cost_cr + ot_expenditure_cr + hiring_training_cost_cr, 2)

        # Logistics OPEX: Base freight + Spot freight surge + Yard demurrage
        base_freight_per_unit = 28000 # ₹28,000 avg delivery cost per car
        base_freight_cr = (fulfilled_units * base_freight_per_unit) / 1e7
        
        # Spot market premium if road carriers exceed contracted volume
        spot_carrier_volume_ratio = max(0.0, 1.0 - (long_term_carrier_contract_pct / 100.0))
        spot_freight_premium_cr = round(base_freight_cr * spot_carrier_volume_ratio * 0.38, 2)
        yard_demurrage_cr = round(max(0.0, (simulated_yard_dwell_days - 2.5) * 18.5), 2)
        total_logistics_cost_cr = round(base_freight_cr + spot_freight_premium_cr + yard_demurrage_cr, 2)

        # Plant Fixed & Operating Overheads + Shift 3 startup costs
        shift_3_overhead = 180.0 if shift_model in ["3_shifts", "hybrid_agile"] else 0.0
        plant_overhead_cr = round((gross_fulfilled_revenue_cr * 0.062) + shift_3_overhead, 2)

        # Working Capital Interest on Inventory Buffers (assuming 9.5% cost of capital)
        incremental_doi = max(0.0, inventory_buffer_target_days - 24.0)
        daily_cogs_run_rate_cr = total_cogs_cr / 365.0
        working_capital_buffer_cr = round(daily_cogs_run_rate_cr * incremental_doi, 2)
        working_capital_carrying_cost_cr = round(working_capital_buffer_cr * 0.095, 2)

        # Strategic CAPEX (debottlenecking, automation tooling)
        strategic_capex_cr = round(debottlenecking_capex_cr, 2)
        annual_depreciation_cr = round(strategic_capex_cr * 0.15, 2) # 15% straight line

        # EBITDA & Net Profit
        total_opex_cr = round(total_cogs_cr + total_labor_cost_cr + total_logistics_cost_cr + plant_overhead_cr + working_capital_carrying_cost_cr, 2)
        ebitda_cr = round(gross_fulfilled_revenue_cr - total_opex_cr, 2)
        ebitda_margin_pct = round((ebitda_cr / gross_fulfilled_revenue_cr) * 100.0, 2) if gross_fulfilled_revenue_cr > 0 else 0.0
        
        ebit_cr = round(ebitda_cr - annual_depreciation_cr, 2)
        corporate_tax_cr = round(max(0.0, ebit_cr * 0.2517), 2)
        net_profit_cr = round(ebit_cr - corporate_tax_cr, 2)
        net_profit_margin_pct = round((net_profit_cr / gross_fulfilled_revenue_cr) * 100.0, 2) if gross_fulfilled_revenue_cr > 0 else 0.0

        # Incremental vs Baseline Comparison
        baseline_revenue = (self.baseline_annual_demand * self.baseline_avg_selling_price_lakhs * 100000) / 1e7
        baseline_ebitda = baseline_revenue * 0.138 # ~13.8% baseline EBITDA
        incremental_ebitda_cr = round(ebitda_cr - baseline_ebitda, 2)
        
        total_investment_cr = strategic_capex_cr + hiring_training_cost_cr + working_capital_buffer_cr
        roi_pct = round((incremental_ebitda_cr / total_investment_cr) * 100.0, 1) if total_investment_cr > 0 else 0.0

        # -------------------------------------------------------------
        # PILLAR HEALTH SCORES (0 to 100)
        # -------------------------------------------------------------
        plant_health_score = max(0, min(100, int(100 - max(0, plant_utilization_pct - 92.0) * 3.5 - (1.0 - simulated_oee / self.baseline_oee) * 150)))
        workforce_health_score = max(0, min(100, int(100 - (avg_ot_hours_per_worker_quarterly / 50.0) * 45 - (simulated_absenteeism_pct - 6.0) * 6)))
        inventory_health_score = max(0, min(100, int(100 - stockout_probability_pct * 1.2 - max(0, 24 - inventory_buffer_target_days) * 2.5)))
        logistics_health_score = max(0, min(100, int(100 - (yard_saturation_pct - 75.0) * 1.5 - (simulated_yard_dwell_days - 2.5) * 6)))
        
        overall_feasibility_score = int((plant_health_score * 0.3) + (workforce_health_score * 0.25) + (inventory_health_score * 0.25) + (logistics_health_score * 0.2))

        return {
            "inputs": {
                "sales_growth_pct": sales_growth_pct,
                "shift_model": shift_model,
                "new_hiring_headcount": new_hiring_headcount,
                "debottlenecking_capex_cr": debottlenecking_capex_cr,
                "inventory_buffer_target_days": inventory_buffer_target_days,
                "supplier_advance_commitment_wks": supplier_advance_commitment_wks,
                "rail_logistics_ratio_pct": rail_logistics_ratio_pct,
                "long_term_carrier_contract_pct": long_term_carrier_contract_pct
            },
            "demand": {
                "baseline_units": self.baseline_annual_demand,
                "target_units": target_demand_units,
                "incremental_units": incremental_demand_units,
                "fulfilled_units": fulfilled_units,
                "unfulfilled_units": unfulfilled_backlog_units,
                "fulfillment_rate_pct": fulfillment_service_level_pct
            },
            "pillar_capacities": pillar_capacities,
            "primary_bottleneck": primary_bottleneck,
            "plant_metrics": {
                "effective_nameplate_capacity": int(effective_annual_nameplate),
                "simulated_oee_pct": round(simulated_oee * 100, 1),
                "plant_utilization_pct": plant_utilization_pct,
                "plant_health_score": plant_health_score
            },
            "workforce_metrics": {
                "total_workforce": total_workforce,
                "avg_ot_hours_quarterly": round(avg_ot_hours_per_worker_quarterly, 1),
                "avg_ot_hours_monthly": round(avg_ot_hours_per_worker_monthly, 1),
                "factories_act_compliance": regulatory_compliance_risk,
                "absenteeism_pct": simulated_absenteeism_pct,
                "scrap_rate_pct": simulated_scrap_rate_pct,
                "workforce_health_score": workforce_health_score
            },
            "inventory_metrics": {
                "doi_target_days": inventory_buffer_target_days,
                "stockout_probability_pct": stockout_probability_pct,
                "stockout_disruption_units": stockout_disruption_loss_units,
                "working_capital_buffer_cr": working_capital_buffer_cr,
                "inventory_health_score": inventory_health_score
            },
            "logistics_metrics": {
                "yard_dwell_days": simulated_yard_dwell_days,
                "yard_saturation_pct": yard_saturation_pct,
                "rail_share_pct": rail_logistics_ratio_pct,
                "carrier_deficit_units": int(carrier_shortage * 8.0 * 3.5 * 12),
                "logistics_health_score": logistics_health_score
            },
            "financials": {
                "gross_revenue_cr": gross_fulfilled_revenue_cr,
                "lost_revenue_potential_cr": lost_potential_revenue_cr,
                "cogs_cr": total_cogs_cr,
                "labor_cost_cr": total_labor_cost_cr,
                "ot_premium_cr": round(ot_expenditure_cr, 2),
                "logistics_cost_cr": total_logistics_cost_cr,
                "plant_overhead_cr": plant_overhead_cr,
                "total_opex_cr": total_opex_cr,
                "strategic_capex_cr": strategic_capex_cr,
                "ebitda_cr": ebitda_cr,
                "ebitda_margin_pct": ebitda_margin_pct,
                "net_profit_cr": net_profit_cr,
                "net_profit_margin_pct": net_profit_margin_pct,
                "incremental_ebitda_cr": incremental_ebitda_cr,
                "total_investment_cr": round(total_investment_cr, 2),
                "roi_pct": roi_pct
            },
            "overall_feasibility": {
                "score": overall_feasibility_score,
                "status": "HIGHLY FEASIBLE" if overall_feasibility_score >= 80 else (
                    "FEASIBLE WITH MITIGATION" if overall_feasibility_score >= 60 else "CRITICAL BOTTLENECK RISK"
                )
            }
        }

if __name__ == "__main__":
    sim = WhatIfBusinessSimulator()
    print("--- BASELINE FEASIBILITY OF NAIVE +20% PUSH ---")
    res_naive = sim.simulate(sales_growth_pct=20.0, shift_model="2_shifts", new_hiring_headcount=0)
    print(f"Target Demand         : {res_naive['demand']['target_units']:,} units")
    print(f"Fulfilled Units       : {res_naive['demand']['fulfilled_units']:,} units ({res_naive['demand']['fulfillment_rate_pct']}%)")
    print(f"Primary Bottleneck    : {res_naive['primary_bottleneck']}")
    print(f"Workforce Compliance : {res_naive['workforce_metrics']['factories_act_compliance']} (OT: {res_naive['workforce_metrics']['avg_ot_hours_quarterly']} hrs/qtr)")
    print(f"Lost Revenue Potential: INR {res_naive['financials']['lost_revenue_potential_cr']:,.2f} Cr")
    print(f"Overall Feasibility   : {res_naive['overall_feasibility']['status']} ({res_naive['overall_feasibility']['score']}/100)")
