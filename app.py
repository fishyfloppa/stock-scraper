import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='templates')

# Function to scrape P/E ratio from Yahoo Finance
def get_pe_ratio(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {
        "User-Agent": "Your User Agent String"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pe_ratio_element = soup.find("td", {"data-test": "PE_RATIO-value"})
        if pe_ratio_element:
            pe_ratio = pe_ratio_element.text
            return pe_ratio
    return 'N/A'

# Function to get the current stock price from Yahoo Finance
def get_stock_price(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {
        "User-Agent": "Your User Agent String"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find("td", {"data-test": "OPEN-value"})
        if price_element:
            stock_price = price_element.text
            return stock_price
    return 'N/A'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tickers = [ticker.strip() for ticker in request.form.get("tickers", "").split(",")]
        max_tickers = 10  # Maximum number of tickers to display

        data = {}

        for ticker in tickers:
            pe_ratio = get_pe_ratio(ticker)
            stock_price = get_stock_price(ticker)
            data[ticker] = {"P/E Ratio": pe_ratio, "Stock Price": stock_price}

        return render_template("index.html", data=data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)
