"""
Pipeline de dados para o B3 Stock Analysis.
Busca OHLCV (yfinance) + indicadores fundamentais (fundamentus),
calcula MAs e Graham VI, e serializa JSONs em data/.
"""

import json
import math
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf
import fundamentus

OUTPUT_DIR = Path(__file__).parent.parent / "data"

TICKERS_YF = [
    "BBAS3.SA", "ABEV3.SA", "B3SA3.SA", "GGBR4.SA", "ITSA4.SA",
    "PETR4.SA", "RENT3.SA", "SUZB3.SA", "VALE3.SA", "WEGE3.SA",
]
TICKERS_FUND = [t.replace(".SA", "") for t in TICKERS_YF]

HISTORY_YEARS = 2


# ── 1. OHLCV ──────────────────────────────────────────────────────────────────

def fetch_ohlcv() -> pd.DataFrame:
    end = date.today()
    start = end - timedelta(days=365 * HISTORY_YEARS)
    print(f"Buscando OHLCV de {start} a {end}…")

    df = yf.download(
        TICKERS_YF,
        start=str(start),
        end=str(end),
        auto_adjust=True,
        progress=False,
    )

    prices = df.stack(level=1, future_stack=True).reset_index()
    prices.rename(columns={"Ticker": "ticker", "Date": "date"}, inplace=True)
    prices["ticker"] = prices["ticker"].str.replace(".SA", "", regex=False)
    prices["date"] = prices["date"].dt.strftime("%Y-%m-%d")

    # Médias móveis calculadas em Python (mais eficiente que no browser)
    prices.sort_values(["ticker", "date"], inplace=True)
    for ma in [20, 50, 200]:
        prices[f"MA{ma}"] = (
            prices.groupby("ticker")["Close"]
            .transform(lambda s: s.rolling(ma, min_periods=1).mean())
            .round(4)
        )

    print(f"  {len(prices)} linhas OHLCV ({len(TICKERS_YF)} ativos).")
    return prices


# ── 2. Fundamentos ─────────────────────────────────────────────────────────────

def fetch_fundamentals() -> pd.DataFrame:
    print("Buscando dados fundamentalistas…")

    desired_cols = [
        "Setor", "Cotacao", "Min_52_sem", "Max_52_sem", "Valor_de_mercado",
        "Nro_Acoes", "Patrim_Liq", "Receita_Liquida_12m", "Receita_Liquida_3m",
        "Lucro_Liquido_12m", "Lucro_Liquido_3m",
    ]

    records = []
    for ticker in TICKERS_FUND:
        try:
            row = fundamentus.get_papel(ticker)
            data = row.iloc[0].to_dict() if hasattr(row, "iloc") else row.to_dict()
            filtered = {col: data.get(col) for col in desired_cols}
            filtered["ticker"] = ticker
            records.append(filtered)
            print(f"  {ticker} OK")
        except Exception as exc:
            print(f"  AVISO: não foi possível buscar {ticker}: {exc}")

    if len(records) < 8:
        print("ERRO: menos de 8 ativos obtidos — abortando para não publicar dados incompletos.")
        sys.exit(1)

    ind = pd.DataFrame(records)
    ind.set_index("ticker", inplace=True)

    # Buscar P/L, P/VP, ROE, DY via get_resultado_raw (sem .SA — esse era o bug do notebook)
    try:
        resultado = fundamentus.get_resultado_raw().reset_index()
        resultado.rename(columns={"papel": "ticker", "Div.Yield": "DY"}, inplace=True)
        resultado = resultado[resultado["ticker"].isin(TICKERS_FUND)].copy()
        resultado.set_index("ticker", inplace=True)
        ind = ind.join(resultado[["P/L", "P/VP", "ROE", "DY"]], how="left")
    except Exception as exc:
        print(f"  AVISO: get_resultado_raw falhou ({exc}); P/L, P/VP, ROE, DY ficarão nulos.")
        for col in ["P/L", "P/VP", "ROE", "DY"]:
            ind[col] = None

    # Converter colunas numéricas
    numeric_cols = [
        "Cotacao", "Min_52_sem", "Max_52_sem", "Valor_de_mercado",
        "Nro_Acoes", "Patrim_Liq", "Receita_Liquida_12m", "Receita_Liquida_3m",
        "Lucro_Liquido_12m", "Lucro_Liquido_3m", "P/L", "P/VP", "ROE", "DY",
    ]
    ind[numeric_cols] = ind[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # LPA = Lucro Líquido / Nº Ações  (não Receita — bug do notebook corrigido aqui)
    ind["LPA"] = (ind["Lucro_Liquido_12m"] / ind["Nro_Acoes"]).round(2)
    ind["VPA"] = (ind["Patrim_Liq"] / ind["Nro_Acoes"]).round(2)

    # Fórmula de Graham: VI = √(22,5 × LPA × VPA), válida só para LPA e VPA positivos
    def graham_vi(row):
        lpa, vpa = row["LPA"], row["VPA"]
        if pd.notna(lpa) and pd.notna(vpa) and lpa > 0 and vpa > 0:
            return round(math.sqrt(22.5 * lpa * vpa), 2)
        return None

    ind["Graham_VI"] = ind.apply(graham_vi, axis=1)
    ind["Graham_Upside_pct"] = (
        (ind["Graham_VI"] - ind["Cotacao"]) / ind["Cotacao"] * 100
    ).round(1)

    # DY em percentual legível (fundamentus retorna 0.0569 para 5,69%)
    ind["DY_pct"] = (ind["DY"] * 100).round(2)

    ind.reset_index(inplace=True)
    print(f"  {len(ind)} registros fundamentalistas.")
    return ind


# ── 3. Serialização ────────────────────────────────────────────────────────────

def safe_val(v):
    """Converte NaN/inf para None para JSON válido."""
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v


def serialize(df: pd.DataFrame) -> list:
    return [
        {k: safe_val(v) for k, v in row.items()}
        for row in df.to_dict(orient="records")
    ]


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    prices = fetch_ohlcv()
    fundamentals_df = fetch_fundamentals()

    # cotacoes.json
    ohlcv_cols = ["ticker", "date", "Open", "High", "Low", "Close", "Volume", "MA20", "MA50", "MA200"]
    cotacoes_out = prices[ohlcv_cols].rename(columns={
        "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Volume": "volume",
    })
    cotacoes_records = serialize(cotacoes_out)

    # fundamentals.json
    fund_cols = [
        "ticker", "Setor", "Cotacao", "Min_52_sem", "Max_52_sem",
        "Valor_de_mercado", "Nro_Acoes", "Patrim_Liq",
        "Lucro_Liquido_12m", "Receita_Liquida_12m",
        "P/L", "P/VP", "ROE", "DY", "DY_pct", "LPA", "VPA",
        "Graham_VI", "Graham_Upside_pct",
    ]
    fund_records = serialize(fundamentals_df[fund_cols])

    # metadata.json
    from datetime import datetime
    metadata = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tickers": TICKERS_FUND,
        "history_start": str(date.today() - timedelta(days=365 * HISTORY_YEARS)),
        "history_end": str(date.today()),
    }

    (OUTPUT_DIR / "cotacoes.json").write_text(
        json.dumps(cotacoes_records, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "fundamentals.json").write_text(
        json.dumps(fund_records, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nPronto! {len(cotacoes_records)} linhas OHLCV, {len(fund_records)} registros fundamentalistas.")
    print(f"Arquivos gerados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
