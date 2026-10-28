/**
 * Mahindra & Mahindra - What-If Business Simulator (Project 14)
 * Client-Side Controller & Real-Time Visualization Engine
 */

document.addEventListener("DOMContentLoaded", () => {
  // UI Elements
  const sliderGrowth = document.getElementById("slider-growth");
  const valGrowth = document.getElementById("val-growth");

  const selectShift = document.getElementById("select-shift");

  const sliderHiring = document.getElementById("slider-hiring");
  const valHiring = document.getElementById("val-hiring");

  const sliderCapex = document.getElementById("slider-capex");
  const valCapex = document.getElementById("val-capex");

  const sliderDoi = document.getElementById("slider-doi");
  const valDoi = document.getElementById("val-doi");

  const sliderLeadtime = document.getElementById("slider-leadtime");
  const valLeadtime = document.getElementById("val-leadtime");

  const sliderRail = document.getElementById("slider-rail");
  const valRail = document.getElementById("val-rail");

  const sliderCarrier = document.getElementById("slider-carrier");
  const valCarrier = document.getElementById("val-carrier");

  const btnRecalculate = document.getElementById("btn-recalculate");

  // Presets
  const btnNaive = document.getElementById("btn-preset-naive");
  const btnSweat = document.getElementById("btn-preset-sweat");
  const btnAgile = document.getElementById("btn-preset-agile");

  // Tabs
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  // AI elements
  const aiChips = document.querySelectorAll(".ai-chip");
  const aiInput = document.getElementById("ai-query-input");
  const btnSubmitAi = document.getElementById("btn-submit-ai");

  // Chart instance
  let mcChart = null;

  // Initialize
  setupEventListeners();
  loadScenariosTable();
  triggerSimulation();
  runMonteCarlo();

  function getControlsPayload() {
    return {
      sales_growth_pct: parseFloat(sliderGrowth.value),
      shift_model: selectShift.value,
      new_hiring_headcount: parseInt(sliderHiring.value),
      debottlenecking_capex_cr: parseFloat(sliderCapex.value),
      inventory_buffer_target_days: parseFloat(sliderDoi.value),
      supplier_advance_commitment_wks: parseInt(sliderLeadtime.value),
      rail_logistics_ratio_pct: parseFloat(sliderRail.value),
      long_term_carrier_contract_pct: parseFloat(sliderCarrier.value)
    };
  }

  function setControlsValues(p) {
    sliderGrowth.value = p.sales_growth_pct;
    valGrowth.textContent = `+${p.sales_growth_pct.toFixed(1)}%`;

    selectShift.value = p.shift_model;

    sliderHiring.value = p.new_hiring_headcount;
    valHiring.textContent = `+${p.new_hiring_headcount.toLocaleString()}`;

    sliderCapex.value = p.debottlenecking_capex_cr;
    valCapex.textContent = `₹${p.debottlenecking_capex_cr} Cr`;

    sliderDoi.value = p.inventory_buffer_target_days;
    valDoi.textContent = `${p.inventory_buffer_target_days} Days`;

    sliderLeadtime.value = p.supplier_advance_commitment_wks;
    valLeadtime.textContent = `${p.supplier_advance_commitment_wks} Weeks`;

    sliderRail.value = p.rail_logistics_ratio_pct;
    valRail.textContent = `${p.rail_logistics_ratio_pct.toFixed(1)}%`;

    sliderCarrier.value = p.long_term_carrier_contract_pct;
    valCarrier.textContent = `${p.long_term_carrier_contract_pct}%`;
  }

  function setupEventListeners() {
    // Slider live text feedback
    sliderGrowth.addEventListener("input", (e) => {
      valGrowth.textContent = `+${parseFloat(e.target.value).toFixed(1)}%`;
      debouncedSimulate();
    });

    sliderHiring.addEventListener("input", (e) => {
      valHiring.textContent = `+${parseInt(e.target.value).toLocaleString()}`;
      debouncedSimulate();
    });

    sliderCapex.addEventListener("input", (e) => {
      valCapex.textContent = `₹${e.target.value} Cr`;
      debouncedSimulate();
    });

    sliderDoi.addEventListener("input", (e) => {
      valDoi.textContent = `${e.target.value} Days`;
      debouncedSimulate();
    });

    sliderLeadtime.addEventListener("input", (e) => {
      valLeadtime.textContent = `${e.target.value} Weeks`;
      debouncedSimulate();
    });

    sliderRail.addEventListener("input", (e) => {
      valRail.textContent = `${parseFloat(e.target.value).toFixed(1)}%`;
      debouncedSimulate();
    });

    sliderCarrier.addEventListener("input", (e) => {
      valCarrier.textContent = `${e.target.value}%`;
      debouncedSimulate();
    });

    selectShift.addEventListener("change", () => {
      debouncedSimulate();
    });

    btnRecalculate.addEventListener("click", () => {
      triggerSimulation();
    });

    // Presets
    btnNaive.addEventListener("click", () => {
      setActivePreset(btnNaive);
      setControlsValues({
        sales_growth_pct: 20.0,
        shift_model: "2_shifts",
        new_hiring_headcount: 0,
        debottlenecking_capex_cr: 0.0,
        inventory_buffer_target_days: 24.0,
        supplier_advance_commitment_wks: 4,
        rail_logistics_ratio_pct: 14.0,
        long_term_carrier_contract_pct: 70.0
      });
      triggerSimulation();
    });

    btnSweat.addEventListener("click", () => {
      setActivePreset(btnSweat);
      setControlsValues({
        sales_growth_pct: 20.0,
        shift_model: "2_shifts_max_ot",
        new_hiring_headcount: 1200,
        debottlenecking_capex_cr: 50.0,
        inventory_buffer_target_days: 20.0,
        supplier_advance_commitment_wks: 6,
        rail_logistics_ratio_pct: 14.0,
        long_term_carrier_contract_pct: 50.0
      });
      triggerSimulation();
    });

    btnAgile.addEventListener("click", () => {
      setActivePreset(btnAgile);
      setControlsValues({
        sales_growth_pct: 20.0,
        shift_model: "hybrid_agile",
        new_hiring_headcount: 4200,
        debottlenecking_capex_cr: 320.0,
        inventory_buffer_target_days: 38.0,
        supplier_advance_commitment_wks: 14,
        rail_logistics_ratio_pct: 30.0,
        long_term_carrier_contract_pct: 90.0
      });
      triggerSimulation();
    });

    // Tab buttons
    tabBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        tabBtns.forEach(b => b.classList.remove("active"));
        tabContents.forEach(c => c.classList.remove("active"));
        btn.classList.add("active");
        const targetId = btn.getAttribute("data-tab");
        document.getElementById(targetId).classList.add("active");
      });
    });

    // AI chips
    aiChips.forEach(chip => {
      chip.addEventListener("click", () => {
        const query = chip.getAttribute("data-q");
        aiInput.value = query;
        submitAIQuery(query);
      });
    });

    btnSubmitAi.addEventListener("click", () => {
      const q = aiInput.value.trim();
      if (q) submitAIQuery(q);
    });

    aiInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        const q = aiInput.value.trim();
        if (q) submitAIQuery(q);
      }
    });

    // Re-run Monte Carlo
    const btnRunMc = document.getElementById("btn-run-mc");
    if (btnRunMc) {
      btnRunMc.addEventListener("click", () => {
        runMonteCarlo();
      });
    }
  }

  function setActivePreset(activeBtn) {
    [btnNaive, btnSweat, btnAgile].forEach(b => b.classList.remove("active"));
    activeBtn.classList.add("active");
  }

  let debounceTimer = null;
  function debouncedSimulate() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      triggerSimulation();
    }, 250);
  }

  async function triggerSimulation() {
    const payload = getControlsPayload();
    try {
      const resp = await fetch("/api/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (data.success) {
        updateUIWithSimulation(data.simulation);
      }
    } catch (err) {
      console.error("Simulation request failed", err);
    }
  }

  function updateUIWithSimulation(res) {
    const d = res.demand;
    const f = res.financials;
    const w = res.workforce_metrics;
    const p = res.plant_metrics;
    const inv = res.inventory_metrics;
    const log = res.logistics_metrics;
    const feas = res.overall_feasibility;

    // Header KPIs
    document.getElementById("kpi-fulfill-val").textContent = `${d.fulfillment_rate_pct}%`;
    document.getElementById("kpi-fulfill-sub").textContent = `${d.fulfilled_units.toLocaleString()} / ${d.target_units.toLocaleString()} Units`;
    
    const kpiBadge = document.getElementById("kpi-fulfill-badge");
    if (d.fulfillment_rate_pct >= 95) {
      kpiBadge.className = "kpi-badge badge-success";
      kpiBadge.textContent = "OPTIMAL";
    } else if (d.fulfillment_rate_pct >= 85) {
      kpiBadge.className = "kpi-badge badge-warning";
      kpiBadge.textContent = "PARTIAL";
    } else {
      kpiBadge.className = "kpi-badge badge-danger";
      kpiBadge.textContent = "CHOKE RISK";
    }

    document.getElementById("kpi-bottleneck-val").textContent = res.primary_bottleneck;
    document.getElementById("kpi-bottleneck-sub").textContent = `Deficit: ${d.unfulfilled_units.toLocaleString()} units`;

    document.getElementById("kpi-revenue-val").textContent = `₹${Math.round(f.gross_revenue_cr).toLocaleString()} Cr`;
    document.getElementById("kpi-lost-rev-sub").textContent = `Lost Opp.: ₹${Math.round(f.lost_revenue_potential_cr).toLocaleString()} Cr`;

    document.getElementById("kpi-ebitda-val").textContent = `₹${Math.round(f.ebitda_cr).toLocaleString()} Cr`;
    document.getElementById("kpi-ebitda-sub").textContent = `Margin: ${f.ebitda_margin_pct}% (Inc: ${f.incremental_ebitda_cr >= 0 ? '+' : ''}₹${Math.round(f.incremental_ebitda_cr)} Cr)`;

    document.getElementById("kpi-ot-val").textContent = `${w.avg_ot_hours_quarterly} hrs/qtr`;
    const compBadge = document.getElementById("kpi-compliance-badge");
    if (w.factories_act_compliance === "COMPLIANT") {
      compBadge.className = "kpi-badge badge-success";
      compBadge.textContent = "COMPLIANT";
    } else {
      compBadge.className = "kpi-badge badge-danger";
      compBadge.textContent = "VIOLATION";
    }

    // Overall Score
    const overallBadge = document.getElementById("overall-status-badge");
    overallBadge.textContent = `FEASIBILITY: ${feas.score}/100`;
    overallBadge.className = feas.score >= 80 ? "kpi-badge badge-success" : (feas.score >= 60 ? "kpi-badge badge-warning" : "kpi-badge badge-danger");

    // Pillar 1: Workforce
    setPillarCard(
      "workforce",
      w.workforce_health_score,
      {
        "m-wf-headcount": w.total_workforce.toLocaleString(),
        "m-wf-ot": `${w.avg_ot_hours_quarterly} hrs/qtr`,
        "m-wf-absent": `${w.absenteeism_pct}% / ${w.scrap_rate_pct}%`,
        "m-wf-factories": w.factories_act_compliance
      }
    );

    // Pillar 2: Plant
    setPillarCard(
      "plant",
      p.plant_health_score,
      {
        "m-plant-cap": `${p.effective_nameplate_capacity.toLocaleString()} units`,
        "m-plant-util": `${p.plant_utilization_pct}%`,
        "m-plant-oee": `${p.simulated_oee_pct}%`,
        "m-plant-capex": `₹${f.strategic_capex_cr} Cr Invested`
      }
    );

    // Pillar 3: Inventory
    setPillarCard(
      "inventory",
      inv.inventory_health_score,
      {
        "m-inv-doi": `${inv.doi_target_days} Days`,
        "m-inv-risk": `${inv.stockout_probability_pct}%`,
        "m-inv-lead": `${res.inputs.supplier_advance_commitment_wks} Weeks`,
        "m-inv-wc": `₹${Math.round(inv.working_capital_buffer_cr).toLocaleString()} Cr`
      }
    );

    // Pillar 4: Logistics
    setPillarCard(
      "logistics",
      log.logistics_health_score,
      {
        "m-log-dwell": `${log.yard_dwell_days} Days`,
        "m-log-sat": `${log.yard_saturation_pct}%`,
        "m-log-rail": `${log.rail_share_pct.toFixed(1)}% Share`,
        "m-log-carrier": `${res.inputs.long_term_carrier_contract_pct}% Dedicated`
      }
    );
  }

  function setPillarCard(pillarName, score, metrics) {
    const badge = document.getElementById(`p-score-${pillarName}`);
    const fill = document.getElementById(`p-fill-${pillarName}`);
    
    badge.textContent = `${score}/100`;
    badge.className = `pillar-score-badge ${score >= 80 ? 'badge-success' : (score >= 60 ? 'badge-warning' : 'badge-danger')}`;
    
    fill.style.width = `${score}%`;
    fill.style.background = score >= 80 ? '#10B981' : (score >= 60 ? '#F59E0B' : '#EF4444');

    for (const [elemId, val] of Object.entries(metrics)) {
      const el = document.getElementById(elemId);
      if (el) el.textContent = val;
    }
  }

  async function loadScenariosTable() {
    try {
      const resp = await fetch("/api/scenarios?growth=20.0");
      const data = await resp.json();
      if (data.success) {
        const tbody = document.getElementById("scenarios-table-body");
        tbody.innerHTML = "";
        data.scenarios.forEach(sc => {
          const r = sc.results;
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>
              <strong>${sc.name}</strong><br/>
              <span class="kpi-badge ${sc.badge_class}" style="font-size: 0.65rem;">${sc.tag}</span>
            </td>
            <td>${sc.params.shift_model.replace('_', ' ').toUpperCase()}</td>
            <td><strong>${r.demand.fulfilled_units.toLocaleString()}</strong></td>
            <td><span class="kpi-badge ${r.demand.fulfillment_rate_pct >= 90 ? 'badge-success' : 'badge-danger'}">${r.demand.fulfillment_rate_pct}%</span></td>
            <td>₹${Math.round(r.financials.gross_revenue_cr).toLocaleString()} Cr</td>
            <td>₹${Math.round(r.financials.ebitda_cr).toLocaleString()} Cr (${r.financials.ebitda_margin_pct}%)</td>
            <td style="color: #FCA5A5;">${r.primary_bottleneck}</td>
            <td><strong style="color: ${r.overall_feasibility.score >= 80 ? '#34D399' : '#F87171'};">${r.overall_feasibility.score}/100</strong></td>
          `;
          tbody.appendChild(tr);
        });
      }
    } catch (e) {
      console.error("Failed to load scenarios", e);
    }
  }

  async function runMonteCarlo() {
    try {
      const payload = getControlsPayload();
      const resp = await fetch("/api/monte-carlo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (data.success) {
        const mc = data.monte_carlo;
        document.getElementById("mc-p10").textContent = `${mc.percentiles_fulfilled_units.P10.toLocaleString()} Units`;
        document.getElementById("mc-p50").textContent = `${mc.percentiles_fulfilled_units.P50.toLocaleString()} Units`;
        document.getElementById("mc-prob").textContent = `${mc.prob_meeting_95pct_demand}%`;
        document.getElementById("mc-var").textContent = `₹${mc.var_95_ebitda_cr.toLocaleString()} Cr`;

        renderMonteCarloChart(mc.distribution_bins);
      }
    } catch (e) {
      console.error("Failed to run Monte Carlo", e);
    }
  }

  function renderMonteCarloChart(bins) {
    const ctx = document.getElementById("monteCarloChart");
    if (!ctx) return;

    const labels = bins.map(b => b.range);
    const counts = bins.map(b => b.count);

    if (mcChart) {
      mcChart.destroy();
    }

    mcChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Simulation Frequency (1,000 Runs)",
          data: counts,
          backgroundColor: "rgba(2, 132, 199, 0.65)",
          borderColor: "#0284C7",
          borderWidth: 1.5,
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#9CA3AF", font: { size: 10 } }
          },
          y: {
            grid: { color: "rgba(75, 85, 99, 0.2)" },
            ticks: { color: "#9CA3AF", font: { size: 10 } }
          }
        }
      }
    });
  }

  async function submitAIQuery(query) {
    const payload = {
      query: query,
      params: getControlsPayload()
    };
    try {
      const resp = await fetch("/api/ask-ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (data.success) {
        const r = data.response;
        document.getElementById("ai-resp-category").textContent = r.category;
        document.getElementById("ai-resp-title").textContent = r.headline;
        document.getElementById("ai-resp-body").textContent = r.details;

        const kpisContainer = document.getElementById("ai-resp-kpis");
        kpisContainer.innerHTML = "";
        r.kpis.forEach(k => {
          const item = document.createElement("div");
          item.className = "ai-kpi-item";
          item.innerHTML = `
            <div class="ai-kpi-lbl">${k.label}</div>
            <div class="ai-kpi-val" style="color: ${k.alert ? '#F87171' : '#34D399'};">${k.val}</div>
          `;
          kpisContainer.appendChild(item);
        });
      }
    } catch (e) {
      console.error("AI query failed", e);
    }
  }
});

