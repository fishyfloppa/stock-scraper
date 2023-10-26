from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__, template_folder='templates')

# Function to get the P/E ratio and stock price from Yahoo Finance
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        pe_ratio = info.get('trailingPE', 'N/A')
        stock_price = info.get('ask', 'N/A')  # Use 'ask' for more real-time stock price
        return pe_ratio, stock_price
    except Exception as e:
        print(f"Error fetching stock info: {e}")
        return 'N/A', 'N/A'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tickers = [ticker.strip() for ticker in request.form.get("tickers", "").split(",")]
        max_tickers = 10  # Maximum number of tickers to display

        data = {}

        for ticker in tickers:
            pe_ratio, stock_price = get_stock_info(ticker)
            data[ticker] = {"P/E Ratio": pe_ratio, "Stock Price": stock_price}

        return render_template("index.html", data=data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)
