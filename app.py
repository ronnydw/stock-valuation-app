import streamlit as st
import plotly.express as px
import numpy as np
import yfinance as yf

def earnings_growth_model(fcf, growth_rate, discount_rate, years=10):
    future_fcf = [fcf * (1 + growth_rate) ** i for i in range(1, years + 1)]
    discounted_fcf = [fcf / (1 + discount_rate) ** i for i, fcf in enumerate(future_fcf, 1)]
    return sum(discounted_fcf)

def reverse_dcf(fcf, discount_rate, terminal_value, shares_outstanding):
    intrinsic_value = fcf / discount_rate + terminal_value
    return intrinsic_value / shares_outstanding

def free_cashflow_yield(fcf, market_cap):
    return fcf / market_cap

st.title("Minotaurus Waardering App")

st.sidebar.header("Input Parameters")

# Input for Yahoo Finance ticker symbol
ticker_symbol = st.sidebar.text_input("Yahoo Finance Ticker Symbol", value="AAPL").upper()

# Fetch company information using yfinance
try:
    ticker = yf.Ticker(ticker_symbol)
    company_name = ticker.info['longName']
except KeyError:
    st.error("Invalid ticker symbol. Please enter a valid Yahoo Finance ticker symbol.")
    st.stop()

growth_rate = st.sidebar.number_input("Expected EPS or FCF growth (%)", value=11.0) / 100
discount_rate = st.sidebar.number_input("Discount rate - DCF (%)", value=10.0) / 100
terminal_value = st.sidebar.number_input("Terminal value (%)", value=3.0) / 100
fcf = st.sidebar.number_input("Free Cash Flow LTM (mio)", value=535.7)
market_cap = st.sidebar.number_input("Market Capitalization (mio)", value=355.15 * 31.0)
shares_outstanding = st.sidebar.number_input("Shares Outstanding (mio)", value=31.0)

valuation_egm = earnings_growth_model(fcf, growth_rate, discount_rate)
valuation_dcf = reverse_dcf(fcf, discount_rate, terminal_value, shares_outstanding)
yield_fcf = free_cashflow_yield(fcf, market_cap)

st.subheader("Valuation Results")
st.write(f"Earnings Growth Model Valuation: ${valuation_egm:.2f} million")
st.write(f"Reverse Discounted Cash Flow Valuation: ${valuation_dcf:.2f} per share")
st.write(f"Free Cash Flow Yield: {yield_fcf:.2%}")

fig = px.bar(
    x=["EGM", "Reverse DCF", "FCF Yield"],
    y=[valuation_egm, valuation_dcf, yield_fcf * market_cap],
    labels={'x': "Valuation Method", 'y': "Value (in million)"},
    title=f"Valuation Comparisons for {company_name}"
)
st.plotly_chart(fig)
