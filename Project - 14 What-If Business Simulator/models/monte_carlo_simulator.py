"""
Mahindra & Mahindra Ltd. - Monte Carlo Operational Risk Simulator
Project - 14: What-If Business Simulator

Performs 1,000 stochastic simulation trials evaluating external and internal operational shocks:
1. Semiconductor & Global Supply Chain Shocks (Fab delays, port congestion)
2. Labor Absenteeism & Union Dynamics (Festive / seasonal agricultural harvesting absenteeism)
3. Logistics Volatility & Severe Weather Disruptions (Monsoon transit logjams)
4. Raw Material Input Price Volatility (Automotive grade steel & LFP cell pricing)
"""

import os
import sys
import numpy as np

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from models.what_if_engine import WhatIfBusinessSimulator

class MonteCarloSimulator:
    def __init__(self, runs=1000, seed=42):
        self.runs = runs
        self.seed = seed
        self.simulator = WhatIfBusinessSimulator()

    def run_simulation(self, base_params=None):
        """
        Executes stochastic runs around the specified decision scenario parameters.
        """
        if base_params is None:
            base_params = {
                "sales_growth_pct": 20.0,
                "shift_model": "hybrid_agile",
                "new_hiring_headcount": 4200,
                "debottlenecking_capex_cr": 320.0,
                "inventory_buffer_target_days": 38.0,
                "supplier_advance_commitment_wks": 14,
                "rail_logistics_ratio_pct": 30.0,
                "long_term_carrier_contract_pct": 90.0
            }

        np.random.seed(self.seed)
        
        fulfilled_units_list = []
        ebitda_list = []
        fulfillment_pct_list = []
        net_profit_list = []

        # Target demand
        target_demand = int(self.simulator.baseline_annual_demand * (1.0 + base_params["sales_growth_pct"] / 100.0))

        for _ in range(self.runs):
            # Stochastic shocks:
            # 1. Lead time variance: shock to supplier advance commitment (-3 to +1 weeks)
            stochastic_advance = max(2, int(base_params["supplier_advance_commitment_wks"] + np.random.choice([0, -1, -2, -3, 1], p=[0.45, 0.25, 0.15, 0.10, 0.05])))
            
            # 2. Logistics road speed shock: carrier availability fluctuation (-10% to +5%)
            carrier_contract_shock = max(30.0, min(100.0, base_params["long_term_carrier_contract_pct"] + np.random.normal(0, 4.0)))
            
            # 3. Rail logistics fulfillment variance (freight corridor availability)
            rail_shock = max(10.0, min(50.0, base_params["rail_logistics_ratio_pct"] + np.random.normal(0, 2.5)))

            # Run deterministic core with stochastic perturbation
            res = self.simulator.simulate(
                sales_growth_pct=base_params["sales_growth_pct"],
                shift_model=base_params["shift_model"],
                new_hiring_headcount=base_params["new_hiring_headcount"],
                debottlenecking_capex_cr=base_params["debottlenecking_capex_cr"],
                inventory_buffer_target_days=base_params["inventory_buffer_target_days"],
                supplier_advance_commitment_wks=stochastic_advance,
                rail_logistics_ratio_pct=rail_shock,
                long_term_carrier_contract_pct=carrier_contract_shock
            )

            # Additional random noise in raw material costs & unexpected tooling maintenance
            cogs_noise_factor = np.random.normal(1.0, 0.015) # +/- 1.5% inflation noise
            sim_ebitda = res["financials"]["ebitda_cr"] * (1.0 - (cogs_noise_factor - 1.0) * 2.2)

            fulfilled_units_list.append(res["demand"]["fulfilled_units"])
            fulfillment_pct_list.append(res["demand"]["fulfillment_rate_pct"])
            ebitda_list.append(sim_ebitda)
            net_profit_list.append(res["financials"]["net_profit_cr"])

        arr_fulfilled = np.array(fulfilled_units_list)
        arr_pct = np.array(fulfillment_pct_list)
        arr_ebitda = np.array(ebitda_list)
        arr_np = np.array(net_profit_list)

        # Percentiles
        p10_units = int(np.percentile(arr_fulfilled, 10))
        p50_units = int(np.percentile(arr_fulfilled, 50))
        p90_units = int(np.percentile(arr_fulfilled, 90))

        p10_ebitda = round(float(np.percentile(arr_ebitda, 10)), 2)
        p50_ebitda = round(float(np.percentile(arr_ebitda, 50)), 2)
        p90_ebitda = round(float(np.percentile(arr_ebitda, 90)), 2)

        # Probability of meeting >= 95% target demand
        prob_success_pct = round(float(np.mean(arr_pct >= 95.0) * 100.0), 1)

        # Value at Risk (VaR 95%): difference between median EBITDA and 5th percentile EBITDA
        p05_ebitda = float(np.percentile(arr_ebitda, 5))
        var_95_ebitda_cr = round(max(0.0, p50_ebitda - p05_ebitda), 2)

        # Histogram data for charts
        hist_counts, bin_edges = np.histogram(arr_pct, bins=12)
        distribution_bins = []
        for i in range(len(hist_counts)):
            distribution_bins.append({
                "range": f"{round(bin_edges[i], 1)}% - {round(bin_edges[i+1], 1)}%",
                "count": int(hist_counts[i])
            })

        return {
            "runs": self.runs,
            "target_demand_units": target_demand,
            "percentiles_fulfilled_units": {"P10": p10_units, "P50": p50_units, "P90": p90_units},
            "percentiles_ebitda_cr": {"P10": p10_ebitda, "P50": p50_ebitda, "P90": p90_ebitda},
            "prob_meeting_95pct_demand": prob_success_pct,
            "var_95_ebitda_cr": var_95_ebitda_cr,
            "mean_fulfillment_pct": round(float(np.mean(arr_pct)), 1),
            "distribution_bins": distribution_bins
        }

if __name__ == "__main__":
    mc = MonteCarloSimulator(runs=1000)
    print("Running 1,000 Monte Carlo Stochastic Simulations on Recommended Scenario...")
    mc_res = mc.run_simulation()
    print(f"P10 Units Fulfilled: {mc_res['percentiles_fulfilled_units']['P10']:,}")
    print(f"P50 Units Fulfilled: {mc_res['percentiles_fulfilled_units']['P50']:,}")
    print(f"P90 Units Fulfilled: {mc_res['percentiles_fulfilled_units']['P90']:,}")
    print(f"Probability >= 95% Fulfillment: {mc_res['prob_meeting_95pct_demand']}%")
    print(f"Expected Median EBITDA: INR {mc_res['percentiles_ebitda_cr']['P50']:,.2f} Cr")
    print(f"95% Value at Risk (VaR): INR {mc_res['var_95_ebitda_cr']:,.2f} Cr")

