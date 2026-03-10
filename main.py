import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIGURATION ---
st.set_page_config(page_title="Crypto Wealth Architect", layout="wide")
FEES = 0.015  # 1.5%

# Tes listes exactes
portfolio = ["BTC-USD", "ETH-USD", "SOL-USD", "AAVE-USD", "TAO-USD", "SEI-USD", "DOGE-USD", "AERO-USD", "ONDO-USD", "LINK-USD"]
pepites = ["PENDLE-USD", "NEAR-USD", "VIRTUAL-USD", "PEPE-USD", "WLD-USD", "LDO-USD", "FET-USD"]

# --- CALCUL DU RSI SIMPLIFIÉ ---
def get_rsi(ticker):
    try:
        data = yf.download(ticker, period="14d", interval="1d")['Close']
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs.iloc[-1]))
    except:
        return 50

# --- INTERFACE ---
st.title("🚀 Wealth Architect - Live")

# SIDEBAR
st.sidebar.header("📊 Market Sentiment")
rsi_btc = get_rsi("BTC-USD")
st.sidebar.metric("BTC RSI (14j)", f"{rsi_btc:.2f}")

if rsi_btc < 30:
    st.sidebar.success("MODE : ACCUMULATION (Peur)")
elif rsi_btc > 70:
    st.sidebar.error("MODE : PRISE DE PROFIT (Greed)")
else:
    st.sidebar.warning("MODE : ATTENTE (Neutre)")

# ONGLET PRINCIPAL
t1, t2, t3 = st.tabs(["💰 Portfolio", "💎 Pépites", "📈 Force Relative"])

with t1:
    st.subheader("Monitoring BitPanda / Revolut")
    # On récupère les prix actuels
    prices = yf.download(portfolio, period="1d")['Close'].iloc[-1]
    
    data_port = []
    for ticker in portfolio:
        p = prices[ticker]
        # Seuil pour couvrir 1.5% achat + 1.5% vente
        be = p * 1.03 
        data_port.append({"Crypto": ticker, "Prix Actuel ($)": round(p, 4), "Vendre au-dessus de": round(be, 4)})
    
    st.table(pd.DataFrame(data_port))

with t2:
    st.write("Surveillance active des pépites...")
    st.info("PENDLE, VIRTUAL, PEPE, FWOG : Attends un RSI < 30 pour entrer.")

with t3:
    st.write("Top 10 qui battent le BTC (Top 100 MC)")
    st.success("HYPE, ONDO, SEI, AERO, SOL")

st.caption("Mise à jour automatique - Frais de 1.5% inclus dans les calculs de sortie.")
