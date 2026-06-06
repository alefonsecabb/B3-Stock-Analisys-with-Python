# Análise de Carteira de Ações B3

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-26a69a?style=for-the-badge&logo=github)](https://alefonsecabb.github.io/B3-Stock-Analisys-with-Python/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](OneDrive/Documents/Projeto_Analise_Mercado/notebooks/Analise_Mercado_Python.ipynb)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/alefonsecabb/B3-Stock-Analisys-with-Python/actions)
[![License](https://img.shields.io/badge/Licença-MIT-yellow?style=for-the-badge)](LICENSE)

> Dashboard interativo para análise técnica e fundamentalista de ações da B3 — desenvolvido com Python, Plotly.js e Bootstrap, com atualização automática diária via GitHub Actions.

---

## Sobre o Projeto

Este projeto combina **engenharia de dados**, **análise financeira** e **desenvolvimento web** para construir uma plataforma de monitoramento de carteira de ações da Bolsa de Valores do Brasil (B3).

O sistema busca automaticamente cotações históricas (via [yfinance](https://github.com/ranaroussi/yfinance)) e indicadores fundamentalistas (via [fundamentus](https://github.com/fundamentus/fundamentus)), processa os dados em Python e os disponibiliza em um site interativo hospedado no GitHub Pages — sem custos e sem servidor.

**Pontos de destaque para o portfólio:**
- Pipeline de dados automatizado com GitHub Actions (atualização diária)
- Gráfico de candlestick interativo com médias móveis e preço alvo
- Cálculo da **Fórmula de Graham** para estimativa de valor intrínseco
- Design profissional com dark theme, totalmente responsivo

---

## Carteira Analisada

| Ticker | Empresa | Setor |
|--------|---------|-------|
| BBAS3 | Banco do Brasil | Intermediários Financeiros |
| ABEV3 | Ambev | Bebidas |
| B3SA3 | B3 S.A. | Serviços Financeiros Diversos |
| GGBR4 | Gerdau | Siderurgia e Metalurgia |
| ITSA4 | Itaúsa | Intermediários Financeiros |
| PETR4 | Petrobras | Petróleo, Gás e Biocombustíveis |
| RENT3 | Localiza | Exploração de Rodovias |
| SUZB3 | Suzano | Papel e Celulose |
| VALE3 | Vale | Mineração |
| WEGE3 | WEG | Máquinas e Equipamentos |

---

## Metodologia

### Análise Técnica (Visão Gráfica)

Os preços são plotados como **candlesticks** — cada vela representa um dia de negociação com abertura, máxima, mínima e fechamento. Complementando:

- **Médias Móveis**: MA 20, MA 50 e MA 200 dias para identificar tendências
- **Volume**: subplot abaixo do gráfico para confirmar movimentos
- **Preço Alvo Graham**: linha horizontal com o valor intrínseco estimado

### Análise Fundamentalista

Indicadores-chave exibidos por ativo:

| Indicador | Descrição |
|-----------|-----------|
| **P/L** | Preço / Lucro — quanto o mercado paga por R$1 de lucro |
| **P/VP** | Preço / Valor Patrimonial — quanto paga pelo patrimônio contábil |
| **ROE** | Retorno sobre Patrimônio Líquido (eficiência de gestão) |
| **Div. Yield** | Dividend Yield — retorno em dividendos |
| **LPA** | Lucro por Ação (Lucro Líquido ÷ Nº Ações) |
| **VPA** | Valor Patrimonial por Ação (PL ÷ Nº Ações) |

### Fórmula de Benjamin Graham

O Valor Intrínseco (VI) é estimado pela fórmula proposta em *The Intelligent Investor* (1949):

$$VI = \sqrt{22{,}5 \times LPA \times VPA}$$

Onde a constante **22,5** implica simultaneamente P/L ≤ 15 e P/VP ≤ 1,5. O **Upside** indica quantos % o preço atual está abaixo (oportunidade) ou acima (risco) do valor intrínseco.

> A fórmula não é válida para ações com LPA ou VPA negativos e deve ser usada como uma das referências, não critério único.

---

## Stack Tecnológica

**Backend (geração de dados):**
- Python 3.12
- [yfinance](https://github.com/ranaroussi/yfinance) — cotações históricas (Yahoo Finance)
- [fundamentus](https://github.com/fundamentus/fundamentus) — indicadores fundamentalistas (B3)
- pandas, numpy — processamento de dados

**Frontend:**
- [Plotly.js 2.35](https://plotly.com/javascript/) — gráficos interativos (candlestick, séries temporais)
- [Bootstrap 5.3](https://getbootstrap.com/) — UI responsiva com dark theme
- JavaScript puro (sem frameworks) — leve e rápido

**Infraestrutura:**
- GitHub Actions — atualização automática diária dos dados (seg–sex, 23h BRT)
- GitHub Pages — hospedagem gratuita e segura

---

## Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/alefonsecabb/B3-Stock-Analisys-with-Python.git
cd B3-Stock-Analisys-with-Python/OneDrive/Documents/Projeto_Analise_Mercado

# 2. Instale as dependências Python
pip install -r requirements.txt

# 3. Gere os arquivos de dados
python scripts/generate_data.py

# 4. Abra o site localmente (servidor HTTP necessário para fetch() funcionar)
python -m http.server 8000
# Acesse: http://localhost:8000
```

---

## Estrutura do Repositório

```
OneDrive/Documents/Projeto_Analise_Mercado/
│
├── .github/workflows/
│   └── update_data.yml       # GitHub Actions: atualização diária automática
│
├── data/                     # Dados pré-gerados (atualizados pelo CI)
│   ├── cotacoes.json         # OHLCV histórico dos 10 ativos (2 anos)
│   ├── fundamentals.json     # Indicadores fundamentalistas + Graham VI
│   └── metadata.json         # Última atualização e lista de tickers
│
├── notebooks/
│   └── Analise_Mercado_Python.ipynb  # Análise exploratória em Jupyter
│
├── scripts/
│   └── generate_data.py      # Pipeline Python de coleta e processamento
│
├── index.html                # Página principal do site
├── style.css                 # Estilos (dark theme profissional)
├── app.js                    # Lógica JavaScript (charts, tabelas, interações)
├── requirements.txt          # Dependências Python
└── README.md
```

---

## Atualização Automática de Dados

O GitHub Actions executa `generate_data.py` **toda noite útil às 23h (horário de Brasília)**, após o fechamento da B3, e commita os novos JSONs automaticamente. Você pode também disparar manualmente pela aba **Actions** → **Atualizar Dados de Mercado** → **Run workflow**.

---

## Limitações e Trabalho Futuro

- `fundamentus` raspa dados do site fundamentus.com.br (B3 apenas); pode quebrar com mudanças no HTML
- A Fórmula de Graham exclui ações com LPA ou VPA negativos
- **Próximas features planejadas:**
  - MACD, RSI e Bandas de Bollinger
  - Heatmap de correlação entre os ativos da carteira
  - Backtesting de estratégias simples (cruzamento de MAs)

---

## Autor

**Alexandre da Fonseca**  
Estudante de Ciência de Dados — FATEC

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Alexandre%20da%20Fonseca-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/alexandre-da-fonseca)
[![Email](https://img.shields.io/badge/Email-alefonsecabb%40gmail.com-D14836?style=flat&logo=gmail&logoColor=white)](mailto:alefonsecabb@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-alefonsecabb-181717?style=flat&logo=github)](https://github.com/alefonsecabb)

---

> *"Price is what you pay. Value is what you get."* — Warren Buffett
