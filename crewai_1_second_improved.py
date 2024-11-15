import streamlit as st
import os
import sys
import warnings
from crewai_tools import BaseTool  # Assuming BaseTool exists in crewai_tools
import pandas as pd

# Define the StockDataTool if it's not already imported
class StockDataTool(BaseTool):
    name: str = "Stock Data Tool"
    description: str = "Fetches stock data, financial metrics, and other key data using yfinance"

    def _run(self, ticker: str, period: str = "5y", fetch_financials: bool = True):
        import yfinance as yf
        stock = yf.Ticker(ticker)
        data = {
            "history": stock.history(period=period)
        }
        if fetch_financials:
            data["financials"] = stock.financials
        return data

# Initialize Streamlit app
st.title("Stock Data Retrieval Tool")

# User input for stock ticker symbol
ticker = st.text_input("Enter Stock Ticker", placeholder="e.g., AAPL")
period = st.selectbox("Select Time Period", options=["1y", "5y", "10y"], index=1)
fetch_financials = st.checkbox("Include Financial Metrics", value=True)

# Button to fetch data
if st.button("Fetch Stock Data"):
    if ticker:
        tool = StockDataTool()
        result = tool._run(ticker=ticker, period=period, fetch_financials=fetch_financials)
        
        # Display stock history
        st.subheader("Stock Price History")
        if "history" in result:
            st.dataframe(result["history"].tail(10))  # Show the last 10 records for brevity

        # Display financial metrics if fetched
        if fetch_financials and "financials" in result:
            st.subheader("Financial Metrics")
            st.dataframe(result["financials"].head(10))  # Display only the first few rows

    else:
        st.error("Please enter a valid stock ticker symbol.")

# Additional configurations, agents, and tool setups
warnings.filterwarnings('ignore')
sys.modules.pop('PIL', None)

# Set the API key directly in the environment (for testing or local setup)
groq_api_key = "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"
os.environ["GROQ_API_KEY"] = groq_api_key

if 'google.colab' in sys.modules:
    from google.colab import userdata
    groq_api_key = userdata.get('GROQ_API_KEY')
else:
    groq_api_key = os.getenv('GROQ_API_KEY')

if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key
else:
    raise ValueError("No Groq API Key found. Set it as an environment variable.")

# Stock Analysis Tool with type annotations for all fields
class StockAnalysisTool(BaseTool):
    name: str = "Stock Analysis Tool"
    description: str = "Analyzes stock data for trends, moving averages, and RSI"
    
    def _run(self, stock_data):
        stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()
        return stock_data

# Additional tools and agent configurations
# Continue adding other tools, agents, tasks, and report generation logic as needed
