import streamlit as st
import requests

st.title("Zakat Calculator")

# -------------------------
# Fetch metal prices
# -------------------------
def get_gold_price():
    url = "https://api.gold-api.com/price/XAU"
    data = requests.get(url).json()
    return data["price"]  # price per troy ounce (USD)

def get_silver_price():
    url = "https://api.gold-api.com/price/XAG"
    data = requests.get(url).json()
    return data["price"]

def get_usd_to_inr():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    data = requests.get(url).json()
    return data["rates"]["INR"]


try:
    gold_usd_oz = get_gold_price()
    silver_usd_oz = get_silver_price()
    usd_to_inr = get_usd_to_inr()

    # 1 troy ounce = 31.1035 grams
    gold_price_per_gram = (gold_usd_oz * usd_to_inr) / 31.1035
    silver_price_per_gram = (silver_usd_oz * usd_to_inr) / 31.1035

except:
    st.error("Could not fetch metal prices")
    gold_price_per_gram = 0
    silver_price_per_gram = 0


st.write(f"Gold price per gram: ₹{gold_price_per_gram:.2f}")
st.write(f"Silver price per gram: ₹{silver_price_per_gram:.2f}")

# -------------------------
# User Inputs
# -------------------------
st.header("Assets")

gold_grams = st.number_input("Gold (grams)", min_value=0.0)
silver_grams = st.number_input("Silver (grams)", min_value=0.0)

gold_value = gold_grams * gold_price_per_gram
silver_value = silver_grams * silver_price_per_gram

st.write(f"Gold value: ₹{gold_value:.2f}")
st.write(f"Silver value: ₹{silver_value:.2f}")

# -------------------------
# Other assets
# -------------------------
# st.header("Other Assets")

cash = st.number_input("Cash", min_value=0.0)
bank = st.number_input("Bank Balance", min_value=0.0)
Investment = st.number_input("Investment", min_value=0.0)
Business = st.number_input("Business", min_value=0.0)
Money = st.number_input("Money Owned by You", min_value=0.0)

st.header("Liabilities")
Loans = st.number_input("Loans(only the upcoming year's installments)", min_value=0.0)

st.header("Nisab Method")

nisab_choice = st.radio(
    "Choose Nisab calculation method",
    ("Gold Nisab (87.87g gold)", "Silver Nisab (612.36g silver)")
)

# -------------------------
# Zakat calculation
# -------------------------
if st.button("Calculate Zakat"):
    total_assets = cash + bank + gold_value + silver_value
    net_wealth = total_assets - Loans

    gold_nisab = gold_price_per_gram * 87.87
    silver_nisab = silver_price_per_gram * 612.36

    if nisab_choice == "Gold Nisab (87.87g gold)":
        nisab = gold_nisab
        method_used = "Gold Nisab"
    else:
        nisab = silver_nisab
        method_used = "Silver Nisab"

    st.subheader("Calculation Summary")
    st.write(f"Method used: {method_used}")
    st.write(f"Net wealth: ₹{net_wealth:.2f}")
    st.write(f"Nisab value: ₹{nisab:.2f}")

    if net_wealth >= nisab:
        zakat = net_wealth * 0.025
        st.success(f"Zakat payable: ₹{zakat:.2f}")
    else:
        st.warning("Net wealth is below Nisab. No Zakat due.")