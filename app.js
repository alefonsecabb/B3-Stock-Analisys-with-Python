/* ─── B3 Stock Analysis — app.js ────────────────────────────────────────── */

const COLORS = {
  green:  '#26a69a',
  red:    '#ef5350',
  yellow: '#ffca28',
  accent: '#4fc3f7',
  ma20:   '#ffa726',
  ma50:   '#ab47bc',
  ma200:  '#42a5f5',
  bg:     '#1e1e2e',
  grid:   '#2e2e3e',
  text:   '#cdd6f4',
};

const PALETTE = [
  '#4fc3f7','#26a69a','#ffa726','#ef5350','#ab47bc',
  '#66bb6a','#ffca28','#78909c','#ec407a','#26c6da',
];

const state = {
  cotacoes:    {},   // { TICKER: [{date, open, high, low, close, volume, MA20, MA50, MA200}] }
  fundamentals: [],
  metadata:    {},
  selectedTicker:  'PETR4',
  selectedPeriod:  '6M',
  normalizedTickers: [],
  showMA:   { 20: false, 50: true, 200: false },
  showGraham: true,
  chartMode:  'candlestick',
  tableSortCol: 'Graham_Upside_pct',
  tableSortAsc: false,
};


// ── Boot ──────────────────────────────────────────────────────────────────────

async function init() {
  try {
    const [cotacoesRaw, fundamentals, metadata] = await Promise.all([
      fetch('data/cotacoes.json').then(r => r.json()),
      fetch('data/fundamentals.json').then(r => r.json()),
      fetch('data/metadata.json').then(r => r.json()),
    ]);

    // Group cotacoes by ticker
    state.cotacoes = cotacoesRaw.reduce((acc, row) => {
      (acc[row.ticker] = acc[row.ticker] || []).push(row);
      return acc;
    }, {});

    state.fundamentals = fundamentals;
    state.metadata = metadata;
    state.normalizedTickers = metadata.tickers.slice(0, 3);

    renderMetadata();
    buildTickerPills();
    buildNormalizedSelectors();
    buildFundamentalCards();
    buildComparisonTable();
    populateSectorFilter();
    bindEvents();
    updateChart();
  } catch (err) {
    console.error('Erro ao carregar dados:', err);
    document.getElementById('last-updated-text').textContent =
      'Erro ao carregar dados. Rode generate_data.py localmente.';
  }
}

document.addEventListener('DOMContentLoaded', init);


// ── Metadata ──────────────────────────────────────────────────────────────────

function renderMetadata() {
  const { last_updated } = state.metadata;
  if (!last_updated) return;
  const formatted = dayjs(last_updated).format('DD/MM/YYYY HH:mm') + ' UTC';
  document.getElementById('last-updated-text').textContent = 'Atualizado em ' + formatted;
}


// ── Ticker pills (candlestick mode) ──────────────────────────────────────────

function buildTickerPills() {
  const container = document.getElementById('ticker-pills');
  container.innerHTML = '';
  state.metadata.tickers.forEach(ticker => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm' + (ticker === state.selectedTicker ? ' active' : '');
    btn.textContent = ticker;
    btn.dataset.ticker = ticker;
    btn.addEventListener('click', () => {
      state.selectedTicker = ticker;
      document.querySelectorAll('#ticker-pills .btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateChart();
    });
    container.appendChild(btn);
  });
}


// ── Normalized selectors (multi-select) ──────────────────────────────────────

function buildNormalizedSelectors() {
  const container = document.getElementById('normalized-selectors');
  container.innerHTML = '';
  state.metadata.tickers.forEach((ticker, i) => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm' + (state.normalizedTickers.includes(ticker) ? ' active' : '');
    btn.textContent = ticker;
    btn.style.setProperty('--bs-btn-active-bg', PALETTE[i % PALETTE.length]);
    btn.dataset.ticker = ticker;
    btn.addEventListener('click', () => {
      if (state.normalizedTickers.includes(ticker)) {
        if (state.normalizedTickers.length === 1) return; // manter pelo menos 1
        state.normalizedTickers = state.normalizedTickers.filter(t => t !== ticker);
        btn.classList.remove('active');
      } else {
        state.normalizedTickers.push(ticker);
        btn.classList.add('active');
      }
      updateChart();
    });
    container.appendChild(btn);
  });
}


// ── Period filter ─────────────────────────────────────────────────────────────

function filterByPeriod(rows, period) {
  if (!rows || rows.length === 0) return rows;
  const today = new Date();
  let cutoff;
  if (period === '1M')  cutoff = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
  else if (period === '3M')  cutoff = new Date(today.getFullYear(), today.getMonth() - 3, today.getDate());
  else if (period === '6M')  cutoff = new Date(today.getFullYear(), today.getMonth() - 6, today.getDate());
  else if (period === 'YTD') cutoff = new Date(today.getFullYear(), 0, 1);
  else if (period === '1A')  cutoff = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());
  else return rows; // Max
  return rows.filter(r => new Date(r.date) >= cutoff);
}


// ── Chart update ──────────────────────────────────────────────────────────────

function updateChart() {
  if (state.chartMode === 'candlestick') {
    renderCandlestick();
  } else {
    renderNormalized();
  }
  updateStatCards();
}


function renderCandlestick() {
  const rows = filterByPeriod(state.cotacoes[state.selectedTicker] || [], state.selectedPeriod);
  if (rows.length === 0) return;

  const dates   = rows.map(r => r.date);
  const opens   = rows.map(r => r.open);
  const highs   = rows.map(r => r.high);
  const lows    = rows.map(r => r.low);
  const closes  = rows.map(r => r.close);
  const volumes = rows.map(r => r.volume);

  const traces = [
    {
      type: 'candlestick',
      x: dates, open: opens, high: highs, low: lows, close: closes,
      name: state.selectedTicker,
      increasing: { line: { color: COLORS.green }, fillcolor: COLORS.green },
      decreasing: { line: { color: COLORS.red   }, fillcolor: COLORS.red   },
      xaxis: 'x', yaxis: 'y',
    },
    {
      type: 'bar',
      x: dates, y: volumes,
      name: 'Volume',
      marker: { color: rows.map((r, i) => i > 0 && r.close >= rows[i-1].close ? COLORS.green : COLORS.red), opacity: 0.5 },
      xaxis: 'x', yaxis: 'y2',
      showlegend: false,
    },
  ];

  // Moving averages
  const maConfig = [
    { key: 'MA20',  color: COLORS.ma20,  label: 'MA 20'  },
    { key: 'MA50',  color: COLORS.ma50,  label: 'MA 50'  },
    { key: 'MA200', color: COLORS.ma200, label: 'MA 200' },
  ];
  maConfig.forEach(({ key, color, label }) => {
    const maNum = parseInt(key.replace('MA', ''));
    traces.push({
      type: 'scatter', mode: 'lines',
      x: dates, y: rows.map(r => r[key]),
      name: label,
      line: { color, width: 1.5 },
      visible: state.showMA[maNum],
      xaxis: 'x', yaxis: 'y',
    });
  });

  // Graham VI line (shape)
  const fund = state.fundamentals.find(f => f.ticker === state.selectedTicker);
  const shapes = [];
  const annotations = [];
  if (state.showGraham && fund && fund.Graham_VI) {
    shapes.push({
      type: 'line', xref: 'paper', x0: 0, x1: 1,
      yref: 'y', y0: fund.Graham_VI, y1: fund.Graham_VI,
      line: { color: COLORS.yellow, width: 1.5, dash: 'dash' },
    });
    annotations.push({
      xref: 'paper', x: 0.01,
      yref: 'y', y: fund.Graham_VI,
      text: `VI Graham: R$ ${fmtNum(fund.Graham_VI, 2)}`,
      showarrow: false,
      font: { color: COLORS.yellow, size: 11 },
      bgcolor: 'rgba(30,30,46,0.85)',
      borderpad: 3,
    });
  }

  const layout = candlestickLayout(shapes, annotations);
  Plotly.react('chart-container', traces, layout, { responsive: true, displayModeBar: false });
}


function candlestickLayout(shapes, annotations) {
  return {
    paper_bgcolor: COLORS.bg,
    plot_bgcolor:  COLORS.bg,
    font: { color: COLORS.text, size: 12 },
    margin: { l: 60, r: 20, t: 15, b: 35 },
    xaxis: {
      type: 'date',
      gridcolor: COLORS.grid,
      linecolor: COLORS.grid,
      tickfont: { size: 11 },
      rangeslider: { visible: false },
    },
    yaxis: {
      title: 'Preço (R$)',
      gridcolor: COLORS.grid,
      linecolor: COLORS.grid,
      tickfont: { size: 11 },
      domain: [0.25, 1],
      tickprefix: 'R$ ',
    },
    yaxis2: {
      title: 'Volume',
      gridcolor: 'transparent',
      linecolor: COLORS.grid,
      tickfont: { size: 10 },
      domain: [0, 0.20],
      showgrid: false,
    },
    legend: { orientation: 'h', y: 1.05, x: 0, font: { size: 11 } },
    shapes,
    annotations,
    hovermode: 'x unified',
    hoverlabel: { bgcolor: '#252535', bordercolor: COLORS.grid, font: { color: COLORS.text } },
  };
}


function renderNormalized() {
  const traces = [];
  state.normalizedTickers.forEach((ticker, i) => {
    const rows = filterByPeriod(state.cotacoes[ticker] || [], state.selectedPeriod);
    if (rows.length === 0) return;
    const base = rows[0].close;
    traces.push({
      type: 'scatter', mode: 'lines',
      x: rows.map(r => r.date),
      y: rows.map(r => ((r.close / base) - 1) * 100),
      name: ticker,
      line: { color: PALETTE[i % PALETTE.length], width: 2 },
    });
  });

  const layout = {
    paper_bgcolor: COLORS.bg,
    plot_bgcolor:  COLORS.bg,
    font: { color: COLORS.text, size: 12 },
    margin: { l: 60, r: 20, t: 15, b: 35 },
    xaxis: { type: 'date', gridcolor: COLORS.grid, linecolor: COLORS.grid },
    yaxis: {
      title: 'Retorno (%)',
      gridcolor: COLORS.grid,
      linecolor: COLORS.grid,
      ticksuffix: '%',
      zeroline: true,
      zerolinecolor: '#6b6b8a',
    },
    legend: { orientation: 'h', y: 1.05, font: { size: 11 } },
    hovermode: 'x unified',
    hoverlabel: { bgcolor: '#252535', bordercolor: COLORS.grid, font: { color: COLORS.text } },
    shapes: [{
      type: 'line', xref: 'paper', x0: 0, x1: 1,
      yref: 'y', y0: 0, y1: 0,
      line: { color: '#6b6b8a', width: 1, dash: 'dot' },
    }],
  };

  Plotly.react('chart-container', traces, layout, { responsive: true, displayModeBar: false });
}


// ── Stat cards ────────────────────────────────────────────────────────────────

function updateStatCards() {
  const ticker = state.chartMode === 'candlestick' ? state.selectedTicker : null;
  const rows = ticker ? filterByPeriod(state.cotacoes[ticker] || [], state.selectedPeriod) : [];

  if (!ticker || rows.length === 0) {
    ['stat-price','stat-var','stat-vol'].forEach(id => {
      document.getElementById(id).textContent = '—';
    });
    return;
  }

  const last  = rows[rows.length - 1];
  const first = rows[0];

  // Cotação
  document.getElementById('stat-price').textContent = 'R$ ' + fmtNum(last.close, 2);
  document.getElementById('stat-ticker-name').textContent = ticker;

  // Variação
  const varPct = ((last.close - first.close) / first.close) * 100;
  const varEl  = document.getElementById('stat-var');
  varEl.textContent = (varPct >= 0 ? '+' : '') + fmtNum(varPct, 2) + '%';
  varEl.className = 'stat-value ' + (varPct >= 0 ? 'stat-positive' : 'stat-negative');

  // Período label
  document.getElementById('stat-period-label').textContent =
    `De ${fmtDate(first.date)} a ${fmtDate(last.date)}`;

  // Volume médio
  const avgVol = rows.reduce((s, r) => s + (r.volume || 0), 0) / rows.length;
  document.getElementById('stat-vol').textContent = fmtVol(avgVol);
}


// ── Fundamental cards ─────────────────────────────────────────────────────────

function buildFundamentalCards() {
  renderFundCards(getSortedFundamentals());
}

function getSortedFundamentals() {
  let data = [...state.fundamentals];
  const sectorFilter = document.getElementById('sector-select')?.value || '';
  if (sectorFilter) data = data.filter(f => f.Setor === sectorFilter);

  const col = state.tableSortCol;
  data.sort((a, b) => {
    const av = a[col] ?? (state.tableSortAsc ? Infinity : -Infinity);
    const bv = b[col] ?? (state.tableSortAsc ? Infinity : -Infinity);
    return state.tableSortAsc ? av - bv : bv - av;
  });
  return data;
}

function renderFundCards(data) {
  const grid = document.getElementById('fund-cards-grid');
  grid.innerHTML = '';
  data.forEach(f => {
    const col = document.createElement('div');
    col.className = 'col-12 col-sm-6 col-lg-4 col-xl-3';
    col.innerHTML = buildCardHTML(f);
    col.querySelector('.btn-ver-grafico').addEventListener('click', () => {
      // Troca para aba gráfica e seleciona o ticker
      document.getElementById('grafico-tab').click();
      state.selectedTicker = f.ticker;
      document.querySelectorAll('#ticker-pills .btn').forEach(b => {
        b.classList.toggle('active', b.dataset.ticker === f.ticker);
      });
      // Garante modo candlestick
      document.getElementById('mode-candle').checked = true;
      state.chartMode = 'candlestick';
      toggleChartMode();
      updateChart();
    });
    grid.appendChild(col);
  });
}

function buildCardHTML(f) {
  const upside      = f.Graham_Upside_pct;
  const upsideClass = upside === null ? 'neutral' : upside > 15 ? 'positive' : upside < -15 ? 'negative' : 'neutral';
  const upsideText  = upside !== null ? (upside > 0 ? '+' : '') + fmtNum(upside, 1) + '%' : 'N/D';

  const plClass  = f['P/L'] !== null ? (f['P/L'] < 10 ? 'green' : f['P/L'] > 25 ? 'red' : 'yellow') : '';
  const roeClass = f.ROE   !== null ? (f.ROE * 100 > 15 ? 'green' : f.ROE * 100 > 10 ? 'yellow' : 'red') : '';
  const dyClass  = f.DY_pct !== null ? (f.DY_pct > 5 ? 'green' : f.DY_pct > 3 ? 'yellow' : 'red') : '';

  const minMax = `${fmtBRL(f.Min_52_sem)} / ${fmtBRL(f.Max_52_sem)}`;

  return `
    <div class="fund-card">
      <div class="d-flex justify-content-between align-items-start mb-1">
        <span class="card-ticker">${f.ticker}</span>
        <span class="card-price">R$ ${fmtNum(f.Cotacao, 2)}</span>
      </div>
      <div class="card-sector">${f.Setor || '—'} · 52s: ${minMax}</div>

      <div class="metric-grid">
        <div class="metric-item ${plClass}">
          <div class="m-label">P/L</div>
          <div class="m-value">${f['P/L'] !== null ? fmtNum(f['P/L'], 1) : 'N/D'}</div>
        </div>
        <div class="metric-item">
          <div class="m-label">P/VP</div>
          <div class="m-value">${f['P/VP'] !== null ? fmtNum(f['P/VP'], 2) : 'N/D'}</div>
        </div>
        <div class="metric-item ${roeClass}">
          <div class="m-label">ROE</div>
          <div class="m-value">${f.ROE !== null ? fmtNum(f.ROE * 100, 1) + '%' : 'N/D'}</div>
        </div>
        <div class="metric-item ${dyClass}">
          <div class="m-label">Div. Yield</div>
          <div class="m-value">${f.DY_pct !== null ? fmtNum(f.DY_pct, 2) + '%' : 'N/D'}</div>
        </div>
      </div>

      <div class="graham-section">
        <div class="g-label"><i class="bi bi-bullseye me-1"></i>Fórmula de Graham</div>
        <div class="d-flex justify-content-between align-items-center">
          <span class="graham-vi">VI = R$ ${f.Graham_VI !== null ? fmtNum(f.Graham_VI, 2) : 'N/D'}</span>
          <span class="upside-badge ${upsideClass}">${upsideText}</span>
        </div>
        <div style="font-size:0.75rem;color:#8b8fa8;margin-top:0.2rem;">
          LPA R$${f.LPA !== null ? fmtNum(f.LPA, 2) : '—'} · VPA R$${f.VPA !== null ? fmtNum(f.VPA, 2) : '—'}
        </div>
      </div>

      <button class="btn btn-sm btn-outline-secondary w-100 btn-ver-grafico" style="font-size:0.8rem;">
        <i class="bi bi-candlestick me-1"></i>Ver Gráfico
      </button>
    </div>
  `;
}


// ── Comparison table ──────────────────────────────────────────────────────────

function buildComparisonTable() {
  renderTable(getSortedFundamentals());
}

function renderTable(data) {
  const tbody = document.getElementById('fund-table-body');
  tbody.innerHTML = '';
  data.forEach(f => {
    const upside = f.Graham_Upside_pct;
    const uClass = upside === null ? '' : upside > 0 ? 'stat-positive' : 'stat-negative';
    tbody.insertAdjacentHTML('beforeend', `
      <tr>
        <td class="table-ticker">${f.ticker}</td>
        <td>R$ ${fmtNum(f.Cotacao, 2)}</td>
        <td>${f['P/L'] !== null ? fmtNum(f['P/L'], 1) : '—'}</td>
        <td>${f['P/VP'] !== null ? fmtNum(f['P/VP'], 2) : '—'}</td>
        <td>${f.ROE !== null ? fmtNum(f.ROE * 100, 1) + '%' : '—'}</td>
        <td>${f.DY_pct !== null ? fmtNum(f.DY_pct, 2) + '%' : '—'}</td>
        <td>${f.Graham_VI !== null ? 'R$ ' + fmtNum(f.Graham_VI, 2) : '—'}</td>
        <td class="${uClass}">${upside !== null ? (upside > 0 ? '+' : '') + fmtNum(upside, 1) + '%' : '—'}</td>
      </tr>
    `);
  });
}


// ── Sector filter ─────────────────────────────────────────────────────────────

function populateSectorFilter() {
  const sectors = [...new Set(state.fundamentals.map(f => f.Setor).filter(Boolean))].sort();
  const sel = document.getElementById('sector-select');
  sectors.forEach(s => {
    const opt = document.createElement('option');
    opt.value = opt.textContent = s;
    sel.appendChild(opt);
  });
}


// ── Table sort ────────────────────────────────────────────────────────────────

function bindTableSort() {
  document.querySelectorAll('.comparison-table thead th[data-col]').forEach(th => {
    th.addEventListener('click', () => {
      const col = th.dataset.col;
      if (state.tableSortCol === col) {
        state.tableSortAsc = !state.tableSortAsc;
      } else {
        state.tableSortCol = col;
        state.tableSortAsc = false;
      }
      document.querySelectorAll('.comparison-table thead th').forEach(h => h.classList.remove('sorted'));
      th.classList.add('sorted');
      const sorted = getSortedFundamentals();
      renderFundCards(sorted);
      renderTable(sorted);
    });
  });
}


// ── Chart mode toggle ─────────────────────────────────────────────────────────

function toggleChartMode() {
  const mode = document.querySelector('input[name="chartMode"]:checked').value;
  state.chartMode = mode;
  const isCandlestick = mode === 'candlestick';
  document.getElementById('candlestick-ticker-row').classList.toggle('d-none', !isCandlestick);
  document.getElementById('normalized-ticker-row').classList.toggle('d-none', isCandlestick);
  document.getElementById('ma-toggles').classList.toggle('d-none', !isCandlestick);
  document.getElementById('graham-toggle-wrap').classList.toggle('d-none', !isCandlestick);
  document.getElementById('stat-cards').classList.toggle('d-none', !isCandlestick);
}


// ── Events ────────────────────────────────────────────────────────────────────

function bindEvents() {
  // Chart mode radio
  document.querySelectorAll('input[name="chartMode"]').forEach(radio => {
    radio.addEventListener('change', () => { toggleChartMode(); updateChart(); });
  });

  // Period buttons
  document.getElementById('period-btns').addEventListener('click', e => {
    const btn = e.target.closest('[data-period]');
    if (!btn) return;
    state.selectedPeriod = btn.dataset.period;
    document.querySelectorAll('#period-btns .btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    updateChart();
  });

  // MA checkboxes
  document.querySelectorAll('[data-ma]').forEach(cb => {
    cb.addEventListener('change', () => {
      state.showMA[parseInt(cb.dataset.ma)] = cb.checked;
      updateChart();
    });
  });

  // Graham toggle
  document.getElementById('toggle-graham').addEventListener('change', e => {
    state.showGraham = e.target.checked;
    updateChart();
  });

  // Sort select (fundamental tab)
  document.getElementById('sort-select').addEventListener('change', e => {
    state.tableSortCol = e.target.value;
    state.tableSortAsc = false;
    const sorted = getSortedFundamentals();
    renderFundCards(sorted);
    renderTable(sorted);
  });

  // Sector select
  document.getElementById('sector-select').addEventListener('change', () => {
    const sorted = getSortedFundamentals();
    renderFundCards(sorted);
    renderTable(sorted);
  });

  // Table sort headers
  bindTableSort();

  // Theme toggle
  document.getElementById('theme-toggle').addEventListener('click', () => {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-bs-theme') === 'dark';
    html.setAttribute('data-bs-theme', isDark ? 'light' : 'dark');
    document.getElementById('theme-toggle').innerHTML =
      isDark ? '<i class="bi bi-moon-stars-fill"></i>' : '<i class="bi bi-sun-fill"></i>';
  });
}


// ── Formatting helpers ────────────────────────────────────────────────────────

function fmtNum(v, decimals = 2) {
  if (v === null || v === undefined) return '—';
  return Number(v).toLocaleString('pt-BR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function fmtBRL(v) {
  if (v === null || v === undefined) return '—';
  return 'R$ ' + fmtNum(v, 2);
}

function fmtVol(v) {
  if (!v) return '—';
  if (v >= 1e6) return fmtNum(v / 1e6, 1) + 'M';
  if (v >= 1e3) return fmtNum(v / 1e3, 0) + 'K';
  return String(Math.round(v));
}

function fmtDate(dateStr) {
  if (!dateStr) return '—';
  const [y, m, d] = dateStr.split('-');
  return `${d}/${m}/${y}`;
}
