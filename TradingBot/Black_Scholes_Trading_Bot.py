import requests
import json
import time
import datetime

from TradingBot.Black_Scholes_Formula import black_scholes

# Define the required input parameters
S = float(input("Enter the current stock price: "))
K = float(input("Enter the strike price: "))
T = float(input("Enter the time to maturity in years: "))
r = float(input("Enter the risk-free interest rate: "))
sigma = float(input("Enter the annualized volatility: "))
option_type = input("Enter the option type (call/put): ")


# Define the main function to fetch the live data, calculate the option price, and place the order
def trade_bot():
    # Define the API endpoint and request headers
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/quotes'
    headers = {'Content-Type': 'application/json'}

    # Define the request body and convert it to JSON
    body = {'symbol': 'AMZN', 'apikey': 'Actual_api_key'}
    json_body = json.dumps(body)

    # Send the request and get the response
    response = requests.post(endpoint, headers=headers, data=json_body)
    json_response = json.loads(response.text)

    # Extract the current stock price and volatility from the response
    current_price = json_response['AMZN']['lastPrice']
    volatility = json_response['AMZN']['volatility']

    # Calculate the option price using the Black-Scholes formula
    option_price = black_scholes(current_price, K, T, r, volatility, option_type)

    # Define the order JSON object and convert it to a string
    order = {'symbol': 'AMZN', 'price': option_price, 'type': option_type, 'quantity': 1}
    json_order = json.dumps(order)

    # Use AWS Lambda to place the order automatically
    # Replace the following lines with your own Lambda code
    lambda_endpoint = 'https://The_lambda_function_URL'
    lambda_headers = {'Content-Type': 'application/json'}
    lambda_response = requests.post(lambda_endpoint, headers=lambda_headers, data=json_order)

    # Printing the order confirmation
    print(lambda_response.text)


# Calling the main function repeatedly at a fixed interval
while True:
    trade_bot()
    time.sleep(300)  # 5 minutes
