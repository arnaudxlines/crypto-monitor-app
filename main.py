import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIGURATION ---
st.set_page_config(page_title="Crypto Bro Advisor", layout="wide")
FEES = 0.015  # 1.5% par transaction

# LISTES DES CRYPTOS DEMANDÉES
portfolio = ["BTC-USD", "ETH-USD", "SOL-USD", "AAVE-USD", "TAO-USD", "SEI-USD", "DOGE-USD", "AERO-USD", "ONDO-USD", "LINK-USD"]
pepites = ["PENDLE-USD", "NEAR-USD", "VIRTUAL-USD", "PEPE-USD", "WLD-USD", "LDO-USD", "FET-USD"]

# --- FONCTIONS ---
def get_crypto_data(tickers):
    data = yf.download(tickers, period="7d", interval="1h")['Close'].iloc[-1]
    return data

def get_market_trend():
    # Simulation d'indicateur de synthèse (RSI + MA200)
    return "BEARISH (PRUDENCE)" # À automatiser avec ta logique

# --- INTERFACE ---
st.title("🚀 Wealth Architect - Dashboard Live")

# SIDEBAR : INDICATEURS MACRO
st.sidebar.header("📊 Market Sentiment")
st.sidebar.metric("Fear & Greed", "13", "Extreme Fear")
st.sidebar.subheader("Tendance Globale")
st.sidebar.error(get_market_trend())

# ONGLET PRINCIPAL
t1, t2, t3 = st.tabs(["💰 Mon Portfolio", "💎 Super Pépites", "📈 Top 10 vs BTC"])

with t1:
    st.subheader("Gestion Active (Spot)")
    prices = get_crypto_data(portfolio)
    for ticker in portfolio:
        p = prices[ticker]
        breakeven = p * (1 + FEES * 2) # Prix pour être rentable après achat/vente
        st.write(f"**{ticker}** : {p:.4f}$ | 🎯 Seuil Rentabilité : {breakeven:.4f}$")

with t2:
    st.subheader("Objectif X100")
    st.info("Surveillance des volumes sur PENDLE, VIRTUAL, PEPE...")
    # Ici tu affiches les données des pépites

with t3:
    st.subheader("Top 10 Outperformers (Top 100 Cap)")
    st.write("1. HYPE | 2. ONDO | 3. SEI | 4. AERO | 5. SOL")

st.divider()
st.caption("Données temps réel via Yahoo Finance API - Rappel : Tes frais BitPanda/Revolut mangent ton profit.")
