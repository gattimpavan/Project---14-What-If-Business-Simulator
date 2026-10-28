# Project - 14: What-If Business Simulator

**Client / Enterprise:** Mahindra & Mahindra Limited (M&M) — Automotive Sector  
**Domain:** Cross-Functional AI Scenario Analysis, Capacity Feasibility & Strategic What-If Simulation  
**Deployment:** Production Localhost Dashboard (`http://localhost:5014`)  
**Executive Deliverable:** Publication-Grade High-Resolution PDF Report (`report/Mahindra_What_If_Business_Simulator_Report.pdf`)  

---

## 1. Problem Statement

> *"Mahindra & Mahindra Management wants to increase sales by 20% but does not know whether existing employees, inventory, production capacity and logistics can support the additional demand. Build an AI scenario-analysis system that simulates business consequences of different strategic decisions."*

Mahindra & Mahindra's automotive business currently delivers **500,000 vehicles annually** across major manufacturing hubs:
- **Chakan Plant (Pune):** XUV700, XUV400 EV, and high-tech monocoque platforms.
- **Nashik Plant:** Scorpio-N, Thar (3-Door & Thar Roxx).
- **Haridwar Plant:** Bolero Neo and compact utility vehicles.
- **Zaheerabad Plant:** Small commercial vehicles and platform variants.

Management's growth mandate aims to scale sales by **+20% (600,000 units/year, representing an incremental ₹14,500 Crores in gross revenue potential)**. However, cross-functional management is uncertain whether existing physical and human capital can handle this surge without collapsing operational integrity.

---

## 2. Cross-Functional Feasibility Audit: The 4 Operational Pillars

The AI What-If Simulation Engine mathematically connects and evaluates four interlinked pillars:

| Operational Pillar | Baseline (500k Units) | Naive +20% Push (No Intervention) | Critical Failure Point | Recommended Intervention (Scenario E) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Employees & Workforce** | 23,000 operators; 12.0 hrs/qtr OT; 6.2% absenteeism | 23,000 operators; **110.0 hrs/qtr OT**; 20.6% absenteeism; 6.9% scrap | **CRITICAL VIOLATION of Indian Factories Act 1948 (Section 64: max 50 hrs/qtr OT)**; severe fatigue and union strike risk | Transition to **3-Shift 24/7 Operations** + recruit **4,200 trained technicians** (OT stabilized at 14.2 hrs/qtr) |
| **2. Production Capacity** | 520,000 units nameplate (2 shifts); 88.0% OEE | **115.4% capacity load**; maintenance deferred; OEE drops to 82.6% | **Hard physical capacity ceiling** at 520k units; paint shop and robotic welding bottlenecks | **Shift 3 addition + ₹320 Cr debottlenecking CAPEX** (expands effective nameplate to 665,600 units; OEE at 88.0%) |
| **3. Inventory & Supply Chain** | 24.0 Days of Inventory (DOI); 4.2% stockout probability | 24.0 DOI; 4-wk notice; **48.3% stockout probability**; 28k lost units | **Tier-1 long lead times (12-16 weeks)** for microcontrollers (Bosch) and LFP battery packs | **14-week firm PO pre-commitments + 38-day strategic buffer** (financed via ₹2,342 Cr working capital) |
| **4. Logistics & Distribution** | 2.5 days yard dwell; 78% yard saturation; 14% rail | **4.5 days dwell; 96.6% yard saturation**; +38% spot freight premium | **Nationwide car carrier shortage**; plant holding yard saturation blocks factory exit ramps | **Double Indian Railways AFTO rail rakes to 30%** + secure 90% contracted carriers + 3 regional hubs |

---

## 3. Evaluated Strategic Decision Scenarios

The simulator preconfigures and arbitrates five distinct strategic scenarios:

```
[Target Demand: 600,000 Vehicles (+20% Surge) | Revenue Target: ₹87,000 Cr]
│
├── Scenario A: Status Quo (Naive Sales Push)
│   ├── Headcount: +0 | Shifts: 2 Shifts Baseline | CAPEX: ₹0 Cr | DOI: 24 Days | Rail: 14%
│   └── Result: 72.2% Fulfillment (433k units) | Lost Rev: ₹24,202 Cr | Factories Act: VIOLATION | Score: 23/100
│
├── Scenario B: Asset Sweating & Maximum Overtime
│   ├── Headcount: +1,200 | Shifts: 2 Shifts + Max OT | CAPEX: ₹50 Cr | DOI: 20 Days | Rail: 14%
│   └── Result: 81.6% Fulfillment (489k units) | Lost Rev: ₹16,024 Cr | Factories Act: VIOLATION | Score: 33/100
│
├── Scenario C: Capacity Expansion & 3rd Shift Addition
│   ├── Headcount: +4,600 | Shifts: 3 Shifts 24/7 | CAPEX: ₹120 Cr | DOI: 26 Days | Rail: 18%
│   └── Result: 93.9% Fulfillment (563k units) | Lost Rev: ₹5,278 Cr | Factories Act: COMPLIANT | Score: 82/100
│
├── Scenario D: Multi-Modal Rail & Strategic Buffering
│   ├── Headcount: +3,800 | Shifts: 3 Shifts 24/7 | CAPEX: ₹180 Cr | DOI: 35 Days | Rail: 28%
│   └── Result: 99.4% Fulfillment (596k units) | Lost Rev: ₹556 Cr | Factories Act: COMPLIANT | Score: 94/100
│
└── Scenario E: Holistic Agile Transformation (Recommended Board Protocol)
    ├── Headcount: +4,200 | Shifts: Hybrid Agile (3 Shifts + Robotics) | CAPEX: ₹320 Cr | DOI: 38 Days | Rail: 30%
    └── Result: 99.6% Fulfillment (597k units) | EBITDA: ₹16,964 Cr (+₹6,959 Cr Accretion) | Score: 96/100
```

---

## 4. Monte Carlo 1,000 Stochastic Risk Trials

Under **Scenario E**, 1,000 stochastic simulation iterations model real-world external disturbances:
- **Global Semiconductor Delays:** Up to 3-week arrival shocks from European/Asian wafer foundries.
- **Logistics Volatility:** Monsoon highway flooding and road carrier fleet availability fluctuations.
- **Labor Dynamics:** Harvesting-season absenteeism spikes across Maharashtra and Uttarakhand.

### Risk Metrics:
- **P10 (Pessimistic Volume):** 596,472 vehicles fulfilled.
- **P50 (Median Expected Volume):** 597,648 vehicles fulfilled.
- **Probability of Meeting ≥ 95% Target Demand:** **100.0%**.
- **95% Value at Risk (VaR):** **₹973.54 Crores** EBITDA downside under compounded extreme disruptions.

---

## 5. System Architecture & Project Structure

```
Project - 14 What-If Business Simulator/
├── app.py                               # Flask server & REST API (Port 5014)
├── run_project.py                       # Master pipeline runner & simulator orchestrator
├── run_dashboard.bat                    # One-click Windows batch launcher
├── README.md                            # Comprehensive project & problem formulation documentation
│
├── data/
│   ├── generate_mahindra_telemetry.py   # Multi-plant operational & component supply generator
│   ├── mahindra_baseline_operations.csv # 36-month plant telemetry dataset
│   └── mahindra_component_supply.csv    # Tier-1 supplier lead times & buffer parameters
│
├── models/
│   ├── what_if_engine.py                # Core 4-pillar cross-functional constraint simulation engine
│   ├── scenario_optimizer.py            # Strategic scenarios A through E comparative evaluator
│   ├── monte_carlo_simulator.py         # 1,000-run stochastic operational risk simulator
│   └── ai_strategic_advisor.py          # Grounded AI Business Analyst natural language agent
│
├── report/
│   ├── generate_pdf_report.py           # Publication-grade ReportLab PDF compiler
│   └── Mahindra_What_If_Business_Simulator_Report.pdf # 810 KB Executive PDF deliverable
│
├── static/
│   ├── css/style.css                    # Mahindra Twin-Peaks styling, dark executive theme, glassmorphism
│   └── js/app.js                        # Dynamic slider updates, Chart.js graphs, AI terminal
│
└── templates/
    └── index.html                       # Responsive executive web interface
```

---

## 6. How to Run the Dashboard & Verify on Localhost

### Quick Launch via Batch Script:
Double-click `run_dashboard.bat` or run in terminal:
```bash
.\run_dashboard.bat
```

### Direct Python Execution:
```bash
"C:\Users\hp\AppData\Local\Programs\Orange\python.exe" run_project.py
```

### Access URLs:
- **Interactive Web Dashboard:** `http://localhost:5014`
- **One-Click PDF Report Download:** `http://localhost:5014/download-report`
- **Simulate REST API:** `POST http://localhost:5014/api/simulate`
- **Monte Carlo REST API:** `POST http://localhost:5014/api/monte-carlo`
- **AI Business Analyst REST API:** `POST http://localhost:5014/api/ask-ai`

---

## 7. Board Execution Roadmap (180-Day Phased Plan)

- **Phase 1 (Days 1–30):** Issue 14-week advance POs to Bosch & JSW Steel; sign Indian Railways AFTO rake contract; initiate hiring for 4,200 operators; submit DISH regulatory filing.
- **Phase 2 (Days 31–90):** Conduct 4-week vocational assembly training; invest ₹320 Cr in robotic welding lines at Chakan; activate Nagpur & NCR regional holding yards.
- **Phase 3 (Days 91–180):** Transition to full 24/7 3-shift production; scale rail dispatch to 30%; hit 50,000 monthly vehicle run-rate (600,000 annual) with 0 labor overtime violations.

