from flask import Flask, render_template, request
import requests
import yfinance as yf

app = Flask(__name__, template_folder='templates')

# Function to scrape P/E ratio from YCharts
def get_pe_ratio(ticker):
    url = f"https://ycharts.com/companies/{ticker}/pe_ratio"
    response = requests.get(url)
    if response.status_code == 200:
        pe_ratio = response.text
        return pe_ratio
    return None

# Function to get the current stock price from Yahoo Finance
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            stock_price = data["Close"].values[0]
            return stock_price
    except Exception as e:
        print(f"Error fetching stock price: {e}")
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tickers = [ticker.strip() for ticker in request.form.get("tickers", "").split(",")]
        max_tickers = 10  # Maximum number of tickers to display

        pe_ratios = {}
        stock_prices = {}

        for ticker in tickers:
            pe_ratio = get_pe_ratio(ticker)
            stock_price = get_stock_price(ticker)
            pe_ratios[ticker] = pe_ratio
            stock_prices[ticker] = stock_price

        return render_template("index.html", tickers=tickers, pe_ratios=pe_ratios, stock_prices=stock_prices)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=1000)
