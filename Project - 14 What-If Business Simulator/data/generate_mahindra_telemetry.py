"""
Mahindra & Mahindra Ltd. (M&M) - Operational Telemetry Generator
Project - 14: What-If Business Simulator

Synthesizes high-fidelity enterprise operational and financial telemetry for M&M's
Automotive Sector across 5 major manufacturing facilities and flagship vehicle lines:
- Plants: Chakan (Pune), Nashik, Zaheerabad, Haridwar, Kandivali
- Vehicle Lines: Scorpio-N, XUV700, Thar (3D/Roxx), Bolero Neo, XUV400 / EV Series
- Time Horizon: 24 Historical Months + 12-Month Baseline Projections
- 4 Operational Pillars:
    1. Employees & Workforce (Headcount, Overtime, Absenteeism, Scrap Rate)
    2. Inventory & Supply Chain (Raw materials, Days of Inventory, Stockout Risk, Tier-1 Lead times)
    3. Production & Tooling Capacity (Nameplate, OEE, Line Takt Time, Shift Configuration)
    4. Logistics & Distribution (Yard Dwell Time, Car Carriers, Indian Railways Auto-Rakes, Freight Costs)
"""

import os
import numpy as np
import pandas as pd

def generate_mahindra_operational_data(output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)

    np.random.seed(42)

    # 1. Monthly Telemetry Generation (36 Months: 2024 to 2026)
    dates = pd.date_range(start="2024-01-01", periods=36, freq="MS")
    plants = [
        {"name": "Chakan Plant (Pune)", "models": ["XUV700", "XUV400 EV"], "capacity": 17500, "workforce_base": 8800},
        {"name": "Nashik Plant", "models": ["Scorpio-N", "Thar"], "capacity": 15000, "workforce_base": 7200},
        {"name": "Haridwar Plant", "models": ["Bolero Neo"], "capacity": 8500, "workforce_base": 3900},
        {"name": "Zaheerabad Plant", "models": ["Small Commercial & Bolero Maxi"], "capacity": 6500, "workforce_base": 3100},
    ]

    records = []
    
    for dt in dates:
        month_idx = (dt.year - 2024) * 12 + dt.month
        # Seasonal trend: Festive surge in Q3 (Oct-Nov)
        festive_factor = 1.22 if dt.month in [10, 11] else (1.08 if dt.month in [1, 3] else 1.0)
        organic_trend = 1.0 + (month_idx * 0.007) # steady ~8% annual organic growth

        for plant in plants:
            plant_name = plant["name"]
            cap_monthly = plant["capacity"]
            wf_base = plant["workforce_base"]

            for model in plant["models"]:
                # Baseline demand per model
                base_demand = (cap_monthly / len(plant["models"])) * 0.88 * festive_factor * organic_trend
                noise = np.random.normal(0, base_demand * 0.04)
                demand = int(np.clip(base_demand + noise, cap_monthly * 0.4, cap_monthly * 1.08))

                # Effective production constrained by capacity (max 95% OEE without overtime)
                max_normal_prod = int((cap_monthly / len(plant["models"])) * 0.94)
                if demand <= max_normal_prod:
                    produced = demand
                    overtime_hours = np.random.uniform(4.0, 12.0)
                else:
                    # Straining capacity
                    strained_cap = int(max_normal_prod * 1.04) # push overtime
                    produced = min(demand, strained_cap)
                    overtime_hours = np.random.uniform(18.0, 32.0) # excessive overtime

                capacity_utilization = round((produced / (cap_monthly / len(plant["models"]))) * 100, 2)
                
                # Workforce dynamics
                absenteeism = round(5.2 + (0.12 * overtime_hours) + np.random.uniform(-0.5, 0.8), 2)
                scrap_rate = round(1.6 + (0.08 * (overtime_hours / 10.0)**1.5) + np.random.uniform(-0.2, 0.3), 2)
                active_workers = int(wf_base / len(plant["models"]) * (1 - absenteeism / 100.0))

                # Inventory Dynamics
                # Normal target buffer is 24 days of inventory (DOI)
                demand_ratio = produced / max_normal_prod
                inventory_doi = round(max(8.0, 24.0 - (demand_ratio - 1.0) * 22.0 + np.random.uniform(-1.5, 1.5)), 1)
                stockout_incidents = int(max(0, np.random.poisson(lam=max(0.2, (24.0 - inventory_doi) * 0.35))))

                # Logistics Dynamics
                # Outbound finished vehicle carriers & railway rakes
                dispatched = produced
                yard_dwell_days = round(2.5 + max(0, (demand_ratio - 0.92) * 8.0) + np.random.uniform(-0.3, 0.4), 2)
                carrier_utilization = round(min(100.0, 84.0 + (demand_ratio - 0.85) * 25.0 + np.random.uniform(-2.0, 3.0)), 1)
                rail_share_pct = round(14.0 + np.random.uniform(-1.5, 2.0), 1)

                # Financial Dynamics (INR Crores)
                # Average Selling Price: XUV700 ~21L, Scorpio-N ~18L, Thar ~15L, Bolero ~9.5L, EV ~19.5L
                asp_lookup = {
                    "XUV700": 21.5,
                    "XUV400 EV": 19.8,
                    "Scorpio-N": 18.2,
                    "Thar": 15.6,
                    "Bolero Neo": 9.8,
                    "Small Commercial & Bolero Maxi": 7.4
                }
                unit_asp_lakhs = asp_lookup.get(model, 14.5)
                gross_revenue_cr = round((produced * unit_asp_lakhs * 100000) / 1e7, 2)
                
                # Direct COGS: ~71% of revenue
                cogs_ratio = 0.705 + (scrap_rate - 1.6) * 0.008
                cogs_cr = round(gross_revenue_cr * cogs_ratio, 2)

                # Labor Cost (including overtime premium 1.5x)
                base_worker_wage_monthly = 32000 # INR per month
                ot_rate_per_hr = 300
                total_labor_cr = round((active_workers * (base_worker_wage_monthly + overtime_hours * ot_rate_per_hr)) / 1e7, 2)

                # Logistics Cost (Inbound + Outbound freight ~4.2% of rev + yard congestion demurrage)
                freight_cr = round(gross_revenue_cr * 0.042 + (yard_dwell_days * 0.08), 2)

                # Plant Overhead & Fixed OPEX
                plant_overhead_cr = round(gross_revenue_cr * 0.065, 2)

                # Total EBITDA
                ebitda_cr = round(gross_revenue_cr - (cogs_cr + total_labor_cr + freight_cr + plant_overhead_cr), 2)
                ebitda_margin_pct = round((ebitda_cr / gross_revenue_cr) * 100, 2) if gross_revenue_cr > 0 else 0.0

                records.append({
                    "date": dt.strftime("%Y-%m-%d"),
                    "year": dt.year,
                    "month": dt.month,
                    "plant": plant_name,
                    "model": model,
                    "demand_units": demand,
                    "produced_units": produced,
                    "dispatched_units": dispatched,
                    "unfulfilled_backlog_units": max(0, demand - produced),
                    "capacity_utilization_pct": capacity_utilization,
                    "active_workforce": active_workers,
                    "overtime_hours_per_worker": round(overtime_hours, 1),
                    "absenteeism_pct": absenteeism,
                    "scrap_rate_pct": scrap_rate,
                    "inventory_days_of_supply": inventory_doi,
                    "stockout_incidents": stockout_incidents,
                    "yard_dwell_days": yard_dwell_days,
                    "carrier_utilization_pct": carrier_utilization,
                    "rail_share_pct": rail_share_pct,
                    "unit_asp_lakhs": unit_asp_lakhs,
                    "gross_revenue_cr": gross_revenue_cr,
                    "cogs_cr": cogs_cr,
                    "labor_cost_cr": total_labor_cr,
                    "logistics_cost_cr": freight_cr,
                    "plant_overhead_cr": plant_overhead_cr,
                    "ebitda_cr": ebitda_cr,
                    "ebitda_margin_pct": ebitda_margin_pct
                })

    df_monthly = pd.DataFrame(records)
    monthly_csv = os.path.join(output_dir, "mahindra_baseline_operations.csv")
    df_monthly.to_csv(monthly_csv, index=False)
    print(f"Generated {len(df_monthly)} operational telemetry rows -> {monthly_csv}")

    # 2. Critical Component Supply & Tier-1 Lead Times
    components = [
        {
            "component_category": "Semiconductor ECUs & Microcontrollers",
            "tier1_supplier": "Bosch India / Continental",
            "current_buffer_days": 18,
            "min_safe_buffer_days": 35,
            "lead_time_weeks": 16,
            "max_supplier_capacity_surge_pct": 12.0,
            "cost_per_vehicle_inr": 48500,
            "bottleneck_criticality": "EXTREME",
            "risk_description": "Global fab allocation constraints; 20% auto surge requires 14-week advance reservation."
        },
        {
            "component_category": "Ultra-High Strength Steel (UHSS) Body Panels",
            "tier1_supplier": "JSW Steel / Tata Steel",
            "current_buffer_days": 26,
            "min_safe_buffer_days": 30,
            "lead_time_weeks": 6,
            "max_supplier_capacity_surge_pct": 25.0,
            "cost_per_vehicle_inr": 112000,
            "bottleneck_criticality": "MEDIUM",
            "risk_description": "Domestic stamping presses at 88% capacity. Stamping tooling calibration needed for Thar/XUV700."
        },
        {
            "component_category": "Lithium Iron Phosphate (LFP) Battery Packs & Cells",
            "tier1_supplier": "Farasis / LG Chem (Imported)",
            "current_buffer_days": 21,
            "min_safe_buffer_days": 40,
            "lead_time_weeks": 12,
            "max_supplier_capacity_surge_pct": 15.0,
            "cost_per_vehicle_inr": 380000,
            "bottleneck_criticality": "HIGH",
            "risk_description": "Customs clearance & sea transit through Nhava Sheva port subject to container dwell delays."
        },
        {
            "component_category": "Automatic Transmissions & Transfer Cases",
            "tier1_supplier": "Aisin / DSI / Mahindra Powertrain",
            "current_buffer_days": 22,
            "min_safe_buffer_days": 28,
            "lead_time_weeks": 8,
            "max_supplier_capacity_surge_pct": 18.0,
            "cost_per_vehicle_inr": 135000,
            "bottleneck_criticality": "HIGH",
            "risk_description": "Torque converter matching precision machining bottlenecks for 4WD Thar & Scorpio-N."
        },
        {
            "component_category": "Wiring Harnesses & Modular Electrics",
            "tier1_supplier": "Motherson Sumi Systems Ltd (MSSL)",
            "current_buffer_days": 15,
            "min_safe_buffer_days": 25,
            "lead_time_weeks": 4,
            "max_supplier_capacity_surge_pct": 20.0,
            "cost_per_vehicle_inr": 28500,
            "bottleneck_criticality": "MEDIUM",
            "risk_description": "Labor intensive assembly in Pune/Noida; rapid scalable if overtime approved."
        },
        {
            "component_category": "Castings, Crankshafts & Engine Blocks",
            "tier1_supplier": "Bharat Forge / Mahindra Foundry",
            "current_buffer_days": 28,
            "min_safe_buffer_days": 30,
            "lead_time_weeks": 5,
            "max_supplier_capacity_surge_pct": 30.0,
            "cost_per_vehicle_inr": 64000,
            "bottleneck_criticality": "LOW",
            "risk_description": "In-house casting facilities have 25% surplus headroom at Zaheerabad & Igatpuri."
        },
        {
            "component_category": "Automotive Car Carriers & Railway Rakes",
            "tier1_supplier": "TCI Supply Chain / IVC / Indian Railways (AFTO)",
            "current_buffer_days": 3,
            "min_safe_buffer_days": 7,
            "lead_time_weeks": 3,
            "max_supplier_capacity_surge_pct": 8.0,
            "cost_per_vehicle_inr": 24000,
            "bottleneck_criticality": "CRITICAL",
            "risk_description": "Severe national shortage of 8-car trailer carriers. Over +10% surge induces yard gridlock."
        }
    ]

    df_components = pd.DataFrame(components)
    comp_csv = os.path.join(output_dir, "mahindra_component_supply.csv")
    df_components.to_csv(comp_csv, index=False)
    print(f"Generated {len(df_components)} critical supply component categories -> {comp_csv}")

    return monthly_csv, comp_csv

if __name__ == "__main__":
    generate_mahindra_operational_data()

