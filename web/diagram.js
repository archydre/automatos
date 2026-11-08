/**
 * Renderizador Interativo do Diagrama Visual de Estados da Máquina de Turing (Grafo SVG).
 * Destaque animado com fluxo de corrente nas arestas, pulso nos nós e inspeção por clique/hover.
 */

const AutomataDiagram = {
  svgContainer: null,
  activeLang: null,
  nodeTooltips: {
    anbncn: {
      q0: "q0: Marca o próximo 'a' com 'X' ou inicia verificação final",
      q1: "q1: Varre à direita procurando o 'b' correspondente",
      q2: "q2: Varre à direita procurando o 'c' correspondente",
      q3: "q3: Rebobina à esquerda até o último 'X'",
      q5: "q5: Valida se todos os 'b's foram pareados (Ys)",
      q6: "q6: Valida se todos os 'c's foram pareados (Zs)",
      q_accept: "qa: Palavra Aceita! (Pertence a L)",
      q_reject: "qr: Palavra Rejeitada (Travamento)",
    },
    ww: {
      q0: "q0: Lê o primeiro símbolo ou aceita cadeia vazia ε",
      q_seek_right: "q_sr: Varre à direita procurando o fim da cadeia",
      q_mark_right: "q_mr: Marca o símbolo extremo direito correspondente",
      q_seek_left: "q_sl: Rebobina à esquerda buscando o último marcado",
      q_mark_left: "q_ml: Avança e detecta o ponto médio exato",
      q_stage2_rewind_start: "q_rw: Rebobina até o início para iniciar o casamento",
      q_match_loop: "q_lp: Lê o próximo símbolo da metade esquerda (0=A, 1=B)",
      q_match_find_C: "q_f0: Busca o '0' correspondente na metade direita (C)",
      q_match_find_D: "q_f1: Busca o '1' correspondente na metade direita (D)",
      q_match_rewind: "q_bk: Rebobina para o próximo símbolo não consumido",
      q_verify_all_matched: "q_vf: Confere se todos os símbolos da direita foram validados",
      q_accept: "qa: Palavra Aceita! (w1 == w2)",
      q_reject: "qr: Palavra Rejeitada (w1 != w2 ou ímpar)",
    }
  },

  init(containerId) {
    this.svgContainer = document.getElementById(containerId);
  },

  render(langId) {
    if (!this.svgContainer) return;
    this.activeLang = langId;

    if (langId === "anbncn") {
      this.svgContainer.innerHTML = this.getAnBnCnSvg();
    } else {
      this.svgContainer.innerHTML = this.getWWSvg();
    }

    this.attachInteractivity();
  },

  attachInteractivity() {
    const tooltipEl = document.getElementById("diagram-tooltip");
    const nodes = this.svgContainer.querySelectorAll(".diagram-node");

    nodes.forEach(node => {
      const nodeId = node.dataset.node;
      const text = (this.nodeTooltips[this.activeLang] && this.nodeTooltips[this.activeLang][nodeId]) || nodeId;

      node.addEventListener("mouseenter", () => {
        if (tooltipEl) {
          tooltipEl.textContent = text;
          tooltipEl.classList.add("visible");
        }
      });

      node.addEventListener("mouseleave", () => {
        if (tooltipEl) {
          tooltipEl.classList.remove("visible");
        }
      });

      node.addEventListener("click", () => {
        if (tooltipEl) {
          tooltipEl.textContent = `[Selecionado] ${text}`;
          tooltipEl.classList.add("visible");
        }
      });
    });
  },

  highlight(state, readSymbol, transition) {
    if (!this.svgContainer) return;

    // Remove destaque anterior
    this.svgContainer.querySelectorAll(".node-active").forEach(el => el.classList.remove("node-active"));
    this.svgContainer.querySelectorAll(".edge-active").forEach(el => el.classList.remove("edge-active"));
    this.svgContainer.querySelectorAll(".edge-label-active").forEach(el => el.classList.remove("edge-label-active"));

    // Destaca o nó do estado atual
    const nodeEl = this.svgContainer.querySelector(`[data-node="${state}"]`);
    if (nodeEl) {
      nodeEl.classList.add("node-active");
    }

    // Se houver transição disparada, destaca a aresta com fluxo animado
    if (state && readSymbol) {
      const edgeKey = `${state}__${readSymbol}`;
      const edgeEl = this.svgContainer.querySelector(`[data-edge~="${edgeKey}"]`) ||
                     this.svgContainer.querySelector(`[data-edge="${edgeKey}"]`);
      if (edgeEl) {
        edgeEl.classList.add("edge-active");
      }
      const labelEl = this.svgContainer.querySelector(`[data-edge-label~="${edgeKey}"]`) ||
                      this.svgContainer.querySelector(`[data-edge-label="${edgeKey}"]`);
      if (labelEl) {
        labelEl.classList.add("edge-label-active");
      }
    }

    // Atualiza tooltip flutuante
    const tooltipEl = document.getElementById("diagram-tooltip");
    if (tooltipEl && state) {
      const desc = (this.nodeTooltips[this.activeLang] && this.nodeTooltips[this.activeLang][state]) || state;
      tooltipEl.textContent = desc;
      tooltipEl.classList.add("visible");
    }
  },

  getAnBnCnSvg() {
    return `
      <svg viewBox="0 0 940 395" class="automaton-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="23" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#374151"/>
          </marker>
          <marker id="arrow-active" viewBox="0 0 10 10" refX="23" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#dc2626"/>
          </marker>
        </defs>

        <!-- ARESTAS / TRANSIÇÕES -->
        <!-- q0 -> q1 (lê 'a') -->
        <path d="M 112,130 Q 190,65 288,75" class="diagram-edge" data-edge="q0__a" marker-end="url(#arrow)"/>
        <text x="190" y="58" class="diagram-label" data-edge-label="q0__a">a → X, R</text>

        <!-- q1 loop (lê 'a' ou 'Y') -->
        <path d="M 300,53 C 280,24 340,24 320,53" class="diagram-edge" data-edge="q1__a q1__Y" marker-end="url(#arrow)"/>
        <text x="310" y="14" class="diagram-label" data-edge-label="q1__a q1__Y">a/a, R ; Y/Y, R</text>

        <!-- q1 -> q2 (lê 'b') -->
        <path d="M 332,75 L 538,75" class="diagram-edge" data-edge="q1__b" marker-end="url(#arrow)"/>
        <text x="435" y="65" class="diagram-label" data-edge-label="q1__b">b → Y, R</text>

        <!-- q2 loop (lê 'b' ou 'Z') -->
        <path d="M 550,53 C 530,24 590,24 570,53" class="diagram-edge" data-edge="q2__b q2__Z" marker-end="url(#arrow)"/>
        <text x="560" y="14" class="diagram-label" data-edge-label="q2__b q2__Z">b/b, R ; Z/Z, R</text>

        <!-- q2 -> q3 (lê 'c') -->
        <path d="M 545,93 Q 480,185 332,195" class="diagram-edge" data-edge="q2__c" marker-end="url(#arrow)"/>
        <text x="460" y="150" class="diagram-label" data-edge-label="q2__c">c → Z, L</text>

        <!-- q3 loop (lê a, b, Y, Z) -->
        <path d="M 300,217 C 280,248 340,248 320,217" class="diagram-edge" data-edge="q3__a q3__b q3__Y q3__Z" marker-end="url(#arrow)"/>
        <text x="310" y="262" class="diagram-label" data-edge-label="q3__a q3__b q3__Y q3__Z">a, b, Y, Z → L</text>

        <!-- q3 -> q0 (lê 'X') -->
        <path d="M 288,195 Q 185,200 112,150" class="diagram-edge" data-edge="q3__X" marker-end="url(#arrow)"/>
        <text x="195" y="200" class="diagram-label" data-edge-label="q3__X">X → X, R</text>

        <!-- q0 -> q5 (lê 'Y' - início da verificação) -->
        <path d="M 95,160 C 105,290 230,290 378,290" class="diagram-edge" data-edge="q0__Y" marker-end="url(#arrow)"/>
        <text x="210" y="278" class="diagram-label" data-edge-label="q0__Y">Y → Y, R</text>

        <!-- q5 loop (lê 'Y') -->
        <path d="M 390,312 C 370,345 430,345 410,312" class="diagram-edge" data-edge="q5__Y" marker-end="url(#arrow)"/>
        <text x="400" y="362" class="diagram-label" data-edge-label="q5__Y">Y → Y, R</text>

        <!-- q5 -> q6 (lê 'Z') -->
        <path d="M 422,290 L 598,290" class="diagram-edge" data-edge="q5__Z" marker-end="url(#arrow)"/>
        <text x="510" y="278" class="diagram-label" data-edge-label="q5__Z">Z → Z, R</text>

        <!-- q6 loop (lê 'Z') -->
        <path d="M 610,312 C 590,345 650,345 630,312" class="diagram-edge" data-edge="q6__Z" marker-end="url(#arrow)"/>
        <text x="620" y="362" class="diagram-label" data-edge-label="q6__Z">Z → Z, R</text>

        <!-- q6 -> q_accept (lê '_') -->
        <path d="M 642,290 L 805,290" class="diagram-edge" data-edge="q6___" marker-end="url(#arrow)"/>
        <text x="725" y="278" class="diagram-label" data-edge-label="q6___">_ → _, S</text>

        <!-- NÓS (ESTADOS) -->
        <!-- q0 (Inicial) -->
        <g class="diagram-node" data-node="q0" transform="translate(90, 140)">
          <path d="M -30,0 L -5,0" stroke="#1f2937" stroke-width="2" marker-end="url(#arrow)" class="initial-arrow"/>
          <circle r="22" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q0</text>
        </g>

        <!-- q1 -->
        <g class="diagram-node" data-node="q1" transform="translate(310, 75)">
          <circle r="22" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q1</text>
        </g>

        <!-- q2 -->
        <g class="diagram-node" data-node="q2" transform="translate(560, 75)">
          <circle r="22" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q2</text>
        </g>

        <!-- q3 -->
        <g class="diagram-node" data-node="q3" transform="translate(310, 195)">
          <circle r="22" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q3</text>
        </g>

        <!-- q5 -->
        <g class="diagram-node" data-node="q5" transform="translate(400, 290)">
          <circle r="22" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q5</text>
        </g>

        <!-- q6 -->
        <g class="diagram-node" data-node="q6" transform="translate(620, 290)">
          <circle r="22" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q6</text>
        </g>

        <!-- q_accept (Final) -->
        <g class="diagram-node accept-node" data-node="q_accept" transform="translate(830, 290)">
          <circle r="25" class="node-circle-outer" />
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">qa</text>
        </g>
      </svg>
    `;
  },

  getWWSvg() {
    return `
      <svg viewBox="0 0 960 365" class="automaton-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow-ww" viewBox="0 0 10 10" refX="23" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#475569"/>
          </marker>
          <marker id="arrow" viewBox="0 0 10 10" refX="23" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#374151"/>
          </marker>
          <marker id="arrow-active" viewBox="0 0 10 10" refX="23" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#dc2626"/>
          </marker>
        </defs>

        <!-- ARESTAS FASE 1 -->
        <path d="M 95,165 Q 150,75 225,75" class="diagram-edge" data-edge="q0__0 q0__1" marker-end="url(#arrow-ww)"/>
        <text x="150" y="95" class="diagram-label" data-edge-label="q0__0 q0__1">0/1 → A/B, R</text>

        <path d="M 70,200 Q 120,335 840,335 Q 865,335 870,205" class="diagram-edge" data-edge="q0___" marker-end="url(#arrow-ww)"/>
        <text x="450" y="325" class="diagram-label" data-edge-label="q0___">ε: _ → _, S</text>

        <path d="M 275,75 L 435,75" class="diagram-edge" data-edge="q_seek_right___ q_seek_right__C q_seek_right__D q_seek_right__0 q_seek_right__1" marker-end="url(#arrow-ww)"/>
        <text x="355" y="65" class="diagram-label" data-edge-label="q_seek_right___">_,C,D → L</text>

        <path d="M 460,98 L 460,155" class="diagram-edge" data-edge="q_mark_right__0 q_mark_right__1" marker-end="url(#arrow-ww)"/>
        <text x="475" y="130" class="diagram-label" data-edge-label="q_mark_right__0">0/1 → C/D, L</text>

        <path d="M 435,180 L 275,180" class="diagram-edge" data-edge="q_seek_left__A q_seek_left__B q_seek_left__0 q_seek_left__1" marker-end="url(#arrow-ww)"/>
        <text x="355" y="170" class="diagram-label" data-edge-label="q_seek_left__A">A,B → R</text>

        <path d="M 250,155 L 250,98" class="diagram-edge" data-edge="q_mark_left__0 q_mark_left__1" marker-end="url(#arrow-ww)"/>
        <text x="185" y="130" class="diagram-label" data-edge-label="q_mark_left__0">0/1 → A/B, R</text>

        <path d="M 250,205 L 250,250" class="diagram-edge" data-edge="q_mark_left__C q_mark_left__D" marker-end="url(#arrow-ww)"/>
        <text x="175" y="230" class="diagram-label" data-edge-label="q_mark_left__C">C,D → L (Meio!)</text>

        <!-- ARESTAS FASE 2 -->
        <path d="M 275,275 L 415,275" class="diagram-edge" data-edge="q_stage2_rewind_start___ q_stage2_rewind_start__A q_stage2_rewind_start__B" marker-end="url(#arrow-ww)"/>
        <text x="345" y="265" class="diagram-label" data-edge-label="q_stage2_rewind_start___">_ → _, R</text>

        <path d="M 460,265 Q 525,200 595,200" class="diagram-edge" data-edge="q_match_loop__A q_match_loop__*" marker-end="url(#arrow-ww)"/>
        <text x="515" y="205" class="diagram-label" data-edge-label="q_match_loop__A">A → *, R</text>

        <path d="M 450,290 Q 525,325 595,280" class="diagram-edge" data-edge="q_match_loop__B" marker-end="url(#arrow-ww)"/>
        <text x="515" y="320" class="diagram-label" data-edge-label="q_match_loop__B">B → *, R</text>

        <path d="M 640,210 Q 695,210 730,235" class="diagram-edge" data-edge="q_match_find_C__C q_match_find_D__D q_match_find_C__A q_match_find_C__B q_match_find_C__#" marker-end="url(#arrow-ww)"/>
        <text x="665" y="205" class="diagram-label" data-edge-label="q_match_find_C__C">C/D → #, L</text>

        <path d="M 730,250 Q 585,250 460,275" class="diagram-edge" data-edge="q_match_rewind__* q_match_rewind__# q_match_rewind__A q_match_rewind__B q_match_rewind__C q_match_rewind__D" marker-end="url(#arrow-ww)"/>
        <text x="605" y="265" class="diagram-label" data-edge-label="q_match_rewind__*">* → *, R</text>

        <path d="M 450,255 Q 565,115 725,115" class="diagram-edge" data-edge="q_match_loop__#" marker-end="url(#arrow-ww)"/>
        <text x="585" y="105" class="diagram-label" data-edge-label="q_match_loop__#"># → #, R</text>

        <path d="M 770,120 Q 865,120 875,155" class="diagram-edge" data-edge="q_verify_all_matched___ q_verify_all_matched__#" marker-end="url(#arrow-ww)"/>
        <text x="820" y="115" class="diagram-label" data-edge-label="q_verify_all_matched___">_ → _, S</text>

        <!-- NÓS -->
        <g class="diagram-node" data-node="q0" transform="translate(70, 180)">
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q0</text>
        </g>

        <g class="diagram-node" data-node="q_seek_right" transform="translate(250, 75)">
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_sr</text>
        </g>

        <g class="diagram-node" data-node="q_mark_right" transform="translate(460, 75)">
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_mr</text>
        </g>

        <g class="diagram-node" data-node="q_seek_left" transform="translate(460, 180)">
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_sl</text>
        </g>

        <g class="diagram-node" data-node="q_mark_left" transform="translate(250, 180)">
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_ml</text>
        </g>

        <g class="diagram-node" data-node="q_stage2_rewind_start" transform="translate(250, 275)">
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_rw</text>
        </g>

        <g class="diagram-node" data-node="q_match_loop" transform="translate(440, 275)">
          <circle r="20" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_lp</text>
        </g>

        <g class="diagram-node" data-node="q_match_find_C" transform="translate(620, 210)">
          <circle r="18" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_f0</text>
        </g>

        <g class="diagram-node" data-node="q_match_find_D" transform="translate(620, 280)">
          <circle r="18" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_f1</text>
        </g>

        <g class="diagram-node" data-node="q_match_rewind" transform="translate(750, 245)">
          <circle r="18" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_bk</text>
        </g>

        <g class="diagram-node" data-node="q_verify_all_matched" transform="translate(750, 120)">
          <circle r="18" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">q_vf</text>
        </g>

        <g class="diagram-node accept-node" data-node="q_accept" transform="translate(880, 180)">
          <circle r="24" class="node-circle-outer" />
          <circle r="19" class="node-circle" />
          <text text-anchor="middle" dy="5" class="node-text">qa</text>
        </g>
      </svg>
    `;
  }
};
