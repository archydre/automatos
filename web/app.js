/**
 * Lógica da Interface Gráfica Minimalista da Máquina de Turing.
 * Sincroniza a fita mecânica e o diagrama de estados SVG vetorial.
 */

const appState = {
  activeLang: "anbncn",
  languagesInfo: {},
  simulation: null,
  currentStepIndex: 0,
  isPlaying: false,
  playTimer: null,
  speedMs: 300,
};

// Elementos DOM
const elements = {
  btnLangAnBnCn: document.getElementById("btn-lang-anbncn"),
  btnLangWW: document.getElementById("btn-lang-ww"),
  inputWord: document.getElementById("input-word"),
  btnLoad: document.getElementById("btn-load"),
  presetsContainer: document.getElementById("presets-container"),
  
  // Fita
  tapeTrack: document.getElementById("tape-track"),
  tapeViewport: document.getElementById("tape-viewport"),
  badgeDirection: document.getElementById("badge-direction"),
  headTag: document.getElementById("head-tag"),
  
  // Controles
  btnReset: document.getElementById("btn-reset"),
  btnPrev: document.getElementById("btn-prev"),
  btnPlay: document.getElementById("btn-play"),
  btnNext: document.getElementById("btn-next"),
  btnEnd: document.getElementById("btn-end"),
  playIcon: document.getElementById("play-icon"),
  playText: document.getElementById("play-text"),
  speedSlider: document.getElementById("speed-slider"),
  speedVal: document.getElementById("speed-val"),
  
  // Telemetria
  metricStatus: document.getElementById("metric-status"),
  metricState: document.getElementById("metric-state"),
  metricSymbol: document.getElementById("metric-symbol"),
  metricStep: document.getElementById("metric-step"),
  metricTransition: document.getElementById("metric-transition"),
  
  // Abas e Tabelas
  tbodyTransitions: document.getElementById("tbody-transitions"),
  traceList: document.getElementById("trace-list"),
  tabButtons: document.querySelectorAll(".btn-tab[data-tab]"),
};

// Inicialização
document.addEventListener("DOMContentLoaded", async () => {
  AutomataDiagram.init("diagram-container");
  setupEventListeners();
  await fetchAppInfo();
  selectLanguage("anbncn");
});

function setupEventListeners() {
  // Troca de linguagem
  elements.btnLangAnBnCn.addEventListener("click", () => selectLanguage("anbncn"));
  elements.btnLangWW.addEventListener("click", () => selectLanguage("ww"));
  elements.btnLangWW.addEventListener("click", () => selectLanguage("ww"));

  // Carregar e simular
  elements.btnLoad.addEventListener("click", () => {
    const word = elements.inputWord.value.trim();
    runSimulation(appState.activeLang, word);
  });

  elements.inputWord.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const word = elements.inputWord.value.trim();
      runSimulation(appState.activeLang, word);
    }
  });

  // Controles de reprodução
  elements.btnReset.addEventListener("click", () => goToStep(0));
  elements.btnPrev.addEventListener("click", () => {
    pause();
    goToStep(appState.currentStepIndex - 1);
  });
  elements.btnNext.addEventListener("click", () => {
    pause();
    goToStep(appState.currentStepIndex + 1);
  });
  elements.btnEnd.addEventListener("click", () => {
    if (appState.simulation && appState.simulation.trace) {
      pause();
      goToStep(appState.simulation.trace.length - 1);
    }
  });
  elements.btnPlay.addEventListener("click", togglePlay);

  // Controle de velocidade
  elements.speedSlider.addEventListener("input", (e) => {
    appState.speedMs = parseInt(e.target.value);
    elements.speedVal.textContent = `${appState.speedMs}ms`;
    if (appState.isPlaying) {
      pause();
      play();
    }
  });

  // Abas
  elements.tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      elements.tabButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      document.querySelectorAll(".tab-panel").forEach((c) => c.classList.add("hidden"));
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) targetPanel.classList.remove("hidden");
    });
  });

  window.addEventListener("resize", () => {
    renderCurrentStep();
  });
}

// Busca metadados da API
async function fetchAppInfo() {
  try {
    const res = await fetch("/api/info");
    const data = await res.json();
    data.languages.forEach((lang) => {
      appState.languagesInfo[lang.id] = lang;
    });
  } catch (err) {
    console.error("Erro ao carregar informações da MT:", err);
  }
}

// Seleciona a linguagem ativa
function selectLanguage(langId) {
  appState.activeLang = langId;
  pause();

  if (langId === "anbncn") {
    elements.btnLangAnBnCn.classList.add("active");
    elements.btnLangWW.classList.remove("active");
  } else {
    elements.btnLangWW.classList.add("active");
    elements.btnLangAnBnCn.classList.remove("active");
  }

  // Renderiza o diagrama SVG da linguagem
  AutomataDiagram.render(langId);

  const langData = appState.languagesInfo[langId];
  if (!langData) return;

  renderPresets(langData.presets);
  renderTransitionsTable(langData.transitions);

  if (langData.presets && langData.presets.length > 0) {
    elements.inputWord.value = langData.presets[0].word;
    runSimulation(langId, langData.presets[0].word);
  }
}

function renderPresets(presets) {
  elements.presetsContainer.innerHTML = "";
  presets.forEach((preset) => {
    const chip = document.createElement("button");
    chip.className = `preset-chip ${preset.expected ? "valid" : "invalid"}`;
    chip.textContent = preset.label;
    chip.addEventListener("click", () => {
      elements.inputWord.value = preset.word;
      runSimulation(appState.activeLang, preset.word);
    });
    elements.presetsContainer.appendChild(chip);
  });
}

async function runSimulation(langId, word) {
  pause();
  try {
    const res = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lang: langId, word: word })
    });
    const data = await res.json();
    if (data.error) {
      alert("Erro na simulação: " + data.error);
      return;
    }
    appState.simulation = data;
    renderTraceList(data.trace);
    goToStep(0);
  } catch (err) {
    console.error("Falha ao comunicar com a API:", err);
  }
}

function goToStep(index) {
  if (!appState.simulation || !appState.simulation.trace) return;
  const maxIdx = appState.simulation.trace.length - 1;
  const targetIdx = Math.max(0, Math.min(index, maxIdx));
  appState.currentStepIndex = targetIdx;
  renderCurrentStep();

  if (targetIdx === maxIdx && appState.isPlaying) {
    pause();
  }
}

function renderCurrentStep() {
  if (!appState.simulation || !appState.simulation.trace) return;
  const snapshot = appState.simulation.trace[appState.currentStepIndex];
  if (!snapshot) return;

  const totalSteps = appState.simulation.trace.length - 1;

  // Atualiza métricas na barra com nome amigável para estados de parada
  let stateDisplay = snapshot.state;
  if (snapshot.state === "q_accept" || snapshot.state === "qa") {
    stateDisplay = "q_accept (Aceitação)";
  } else if (snapshot.state === "q_reject" || snapshot.state === "qr") {
    stateDisplay = "q_reject (Rejeição)";
  }

  if (elements.metricState) elements.metricState.textContent = stateDisplay;
  if (elements.metricSymbol) elements.metricSymbol.textContent = snapshot.read_symbol === "_" ? "⊔ (branco)" : `'${snapshot.read_symbol}'`;
  if (elements.metricStep) elements.metricStep.textContent = `${snapshot.step_num} / ${totalSteps}`;
  if (elements.metricTransition) elements.metricTransition.textContent = snapshot.message;

  if (elements.headTag) elements.headTag.textContent = `[${snapshot.state}]`;

  // Resolução comentada do passo atual
  const didacticEl = document.getElementById("didactic-comment");
  const intentEl = document.getElementById("meta-intent");
  const ruleEl = document.getElementById("meta-rule");
  const stepBadgeEl = document.getElementById("step-badge-counter");

  if (didacticEl) {
    didacticEl.textContent = snapshot.explanation || snapshot.message;
  }
  if (intentEl) {
    intentEl.textContent = snapshot.intent || "Executando transição";
  }
  if (ruleEl) {
    ruleEl.textContent = snapshot.formal_rule || snapshot.message;
  }
  if (stepBadgeEl) {
    stepBadgeEl.textContent = `[Passo #${snapshot.step_num}]`;
  }

  if (elements.badgeDirection) {
    if (snapshot.transition) {
      const dirMap = { R: "Direita (R)", L: "Esquerda (L)", S: "Parado (S)" };
      elements.badgeDirection.textContent = dirMap[snapshot.transition.direction] || snapshot.transition.direction;
    } else {
      elements.badgeDirection.textContent = "-";
    }
  }

  // Atualiza o Status textual (HTML nativo sem badge CSS)
  if (elements.metricStatus) {
    if (!snapshot.halted) {
      elements.metricStatus.innerHTML = "<b>EXECUTANDO</b>";
    } else if (snapshot.accepted) {
      elements.metricStatus.innerHTML = "<b style='color:#008800;'>PALAVRA ACEITA</b>";
    } else {
      elements.metricStatus.innerHTML = "<b style='color:#cc0000;'>PALAVRA REJEITADA</b>";
    }
  }

  // Renderiza a fita mecânica
  renderTape(snapshot.tape_dict);

  // Ilumina o Diagrama de Estados do Autômato (Grafo SVG)
  AutomataDiagram.highlight(snapshot.state, snapshot.read_symbol, snapshot.transition);

  // Destaca linha na tabela e histórico
  highlightTransitionRow(snapshot.state, snapshot.read_symbol);
  highlightTraceItem(appState.currentStepIndex);

  // Atualiza botões
  if (elements.btnPrev) elements.btnPrev.disabled = appState.currentStepIndex === 0;
  if (elements.btnReset) elements.btnReset.disabled = appState.currentStepIndex === 0;
  if (elements.btnNext) elements.btnNext.disabled = appState.currentStepIndex === totalSteps;
  if (elements.btnEnd) elements.btnEnd.disabled = appState.currentStepIndex === totalSteps;
}

function renderTape(tapeDict) {
  elements.tapeTrack.innerHTML = "";

  const headPos = tapeDict.head;
  const cells = tapeDict.cells;

  const minPos = tapeDict.min_pos - 7;
  const maxPos = tapeDict.max_pos + 7;

  const cellsMap = {};
  cells.forEach((c) => {
    cellsMap[c.pos] = c.symbol;
  });

  const cellWidth = 50; // px
  const cellGap = 4;    // px
  const cellPitch = cellWidth + cellGap;

  let headElemIndex = 0;
  let counter = 0;

  for (let p = minPos; p <= maxPos; p++) {
    const sym = cellsMap[p] !== undefined ? cellsMap[p] : tapeDict.blank_symbol;
    const isHead = p === headPos;

    if (isHead) {
      headElemIndex = counter;
    }

    const cellDiv = document.createElement("div");
    cellDiv.className = `tape-cell ${isHead ? "is-head" : ""} ${sym === "_" ? "blank" : ""}`;

    const posSpan = document.createElement("span");
    posSpan.className = "cell-index";
    posSpan.textContent = p;

    const symSpan = document.createElement("span");
    symSpan.className = "cell-char";
    symSpan.textContent = sym === "_" ? "⊔" : sym;

    cellDiv.appendChild(posSpan);
    cellDiv.appendChild(symSpan);
    elements.tapeTrack.appendChild(cellDiv);

    counter++;
  }

  // Mantém a célula sob o cabeçote exatamente centralizada
  const viewportWidth = elements.tapeViewport.offsetWidth || 800;
  const centerOffset = viewportWidth / 2;
  const headCenterPos = headElemIndex * cellPitch + cellWidth / 2;
  const translateX = centerOffset - headCenterPos;

  elements.tapeTrack.style.transform = `translateX(${translateX}px)`;
}

function togglePlay() {
  if (appState.isPlaying) {
    pause();
  } else {
    play();
  }
}

function play() {
  if (!appState.simulation || !appState.simulation.trace) return;
  const totalSteps = appState.simulation.trace.length - 1;
  if (appState.currentStepIndex >= totalSteps) {
    goToStep(0);
  }
  appState.isPlaying = true;
  if (elements.playIcon) elements.playIcon.textContent = "";
  elements.playText.textContent = "Pausar";

  appState.playTimer = setInterval(() => {
    if (appState.currentStepIndex < totalSteps) {
      goToStep(appState.currentStepIndex + 1);
    } else {
      pause();
    }
  }, appState.speedMs);
}

function pause() {
  appState.isPlaying = false;
  if (elements.playIcon) elements.playIcon.textContent = "";
  elements.playText.textContent = "Reproduzir";
  if (appState.playTimer) {
    clearInterval(appState.playTimer);
    appState.playTimer = null;
  }
}

function renderTransitionsTable(transitions) {
  elements.tbodyTransitions.innerHTML = "";
  transitions.forEach((tr) => {
    const row = document.createElement("tr");
    row.dataset.state = tr.from_state;
    row.dataset.read = tr.read_symbol;

    const dirSymbol = tr.direction === "R" ? "R" : tr.direction === "L" ? "L" : "S";

    row.innerHTML = `
      <td>${tr.from_state}</td>
      <td>'${tr.read_symbol === "_" ? "⊔" : tr.read_symbol}'</td>
      <td>${tr.to_state}</td>
      <td>'${tr.write_symbol === "_" ? "⊔" : tr.write_symbol}'</td>
      <td>${dirSymbol}</td>
      <td><code>δ(${tr.from_state}, '${tr.read_symbol}') = (${tr.to_state}, '${tr.write_symbol}', ${tr.direction})</code></td>
    `;
    elements.tbodyTransitions.appendChild(row);
  });
}

function highlightTransitionRow(state, readSymbol) {
  const rows = elements.tbodyTransitions.querySelectorAll("tr");
  rows.forEach((r) => {
    if (r.dataset.state === state && r.dataset.read === readSymbol) {
      r.classList.add("active-transition");
    } else {
      r.classList.remove("active-transition");
    }
  });
}

function renderTraceList(trace) {
  elements.traceList.innerHTML = "";
  trace.forEach((snap, idx) => {
    const item = document.createElement("div");
    item.className = "trace-line";
    item.dataset.index = idx;

    const statusBadge = snap.halted
      ? snap.accepted
        ? "<span style='color: #10b981; font-weight: bold;'>[ACEITA]</span>"
        : "<span style='color: #ef4444; font-weight: bold;'>[REJEITADA]</span>"
      : "";

    item.innerHTML = `
      <div><strong>#${snap.step_num}</strong> ${snap.message}</div>
      <div>q=${snap.state}, pos=${snap.head_pos} ${statusBadge}</div>
    `;

    item.addEventListener("click", () => {
      pause();
      goToStep(idx);
    });

    elements.traceList.appendChild(item);
  });
}

function highlightTraceItem(index) {
  const items = elements.traceList.querySelectorAll(".trace-line");
  items.forEach((item) => {
    if (parseInt(item.dataset.index) === index) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });
}
