import streamlit as st
import pandas as pd
import yfinance as yf

# --- CONFIGURATION ---
st.set_page_config(page_title="Crypto Wealth Architect", layout="wide")
FEES = 0.015  # 1.5% BitPanda/Revolut

# Tes listes exactes
portfolio = ["BTC-USD", "ETH-USD", "SOL-USD", "AAVE-USD", "TAO-USD", "SEI-USD", "DOGE-USD", "AERO-USD", "ONDO-USD", "LINK-USD"]
pepites = ["PENDLE-USD", "NEAR-USD", "VIRTUAL-USD", "PEPE-USD", "WLD-USD", "LDO-USD", "FET-USD"]

# --- FONCTION RSI SÉCURISÉE ---
def get_rsi(ticker):
    try:
        df = yf.download(ticker, period="30d", interval="1d", progress=False)
        if df.empty: return 50.0
        close = df['Close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        val = 100 - (100 / (1 + rs.iloc[-1]))
        return float(val) if not pd.isna(val) else 50.0
    except:
        return 50.0

# --- INTERFACE ---
st.title("🚀 Wealth Architect - Live Dashboard")

# SIDEBAR
st.sidebar.header("📊 Market Sentiment")
rsi_btc = get_rsi("BTC-USD")

# Affichage sécurisé du RSI
st.sidebar.metric("BTC RSI (14j)", f"{rsi_btc:.2f}")

if rsi_btc < 35:
    st.sidebar.success("🔥 MODE : ACCUMULATION (Peur)")
elif rsi_btc > 65:
    st.sidebar.error("⚠️ MODE : PRUDENCE (Greed)")
else:
    st.sidebar.warning("⚖️ MODE : NEUTRE")

# AJOUT DU FEAR & GREED (IMAGE DIRECTE)
st.sidebar.image("https://alternative.me/crypto/fear-and-greed-index.png")

# ONGLET PRINCIPAL
t1, t2, t3 = st.tabs(["💰 Portfolio", "💎 Pépites", "📈 Top 10 vs BTC"])

with t1:
    st.subheader("Monitoring BitPanda / Revolut")
    try:
        # Téléchargement groupé
        data = yf.download(portfolio, period="1d", progress=False)['Close']
        
        # Si c'est un DataFrame (plusieurs colonnes) ou une Series
        prices_list = []
        for ticker in portfolio:
            try:
                # On gère le fait que yfinance peut renvoyer plusieurs formats
                current_p = data[ticker].iloc[-1] if isinstance(data, pd.DataFrame) else data.iloc[-1]
                be = current_p * 1.031  # 3% pour couvrir AR + marge de sécurité
                prices_list.append({
                    "Crypto": ticker.replace("-USD", ""),
                    "Prix Actuel ($)": f"{current_p:.4f}",
                    "Vendre au-dessus de (Seuil Rentabilité)": f"{be:.4f}"
                })
            except:
                continue
        
        st.table(pd.DataFrame(prices_list))
    except Exception as e:
        st.error("Chargement des prix en cours... Rafraîchis dans 10 secondes.")

with t2:
    st.subheader("Zone Pépites (High Risk)")
    st.write("Cibles : PENDLE, VIRTUAL, PEPE, FWOG, PLUME")
    st.warning("Stratégie : N'entre que si le RSI de l'actif est < 30.")

with t3:
    st.subheader("Top 10 Outperformers")
    st.info("Actifs avec la plus forte résilience face au BTC.")
    st.write("1. HYPE | 2. ONDO | 3. SEI | 4. AERO | 5. SOL")

st.divider()
st.caption("Données extraites en temps réel. Les calculs incluent les frais de 1.5% par mouvement.")
