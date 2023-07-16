import requests
import json
import time

from TradingBot.Black_Scholes_Formula import black_scholes

# Define the required input parameters
try:
    S = float(input("Enter the current stock price: "))
    K = float(input("Enter the strike price: "))
    T = float(input("Enter the time to maturity in years: "))
    r = float(input("Enter the risk-free interest rate: "))
    sigma = float(input("Enter the annualized volatility: "))
    option_type = input("Enter the option type (call/put): ").lower()
    assert option_type in ["call", "put"], "Option type must be either 'call' or 'put'"
except ValueError:
    print("Invalid input. Please enter a number.")
    exit(1)
except AssertionError as e:
    print(e)
    exit(1)

# Define the main function to fetch the live data, calculate the option price, and place the order
def trade_bot():
    # Define the API endpoint and request headers
    endpoint = 'https://api.tdameritrade.com/v1/marketdata/quotes'
    headers = {'Content-Type': 'application/json'}

    # Define the request body and convert it to JSON
    body = {'symbol': 'AMZN', 'apikey': 'Actual_api_key'}
    json_body = json.dumps(body)

    # Send the request and get the response
    try:
        response = requests.post(endpoint, headers=headers, data=json_body)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return
    json_response = json.loads(response.text)

    # Extract the current stock price and volatility from the response
    try:
        current_price = json_response['AMZN']['lastPrice']
        volatility = json_response['AMZN']['volatility']
    except KeyError:
        print("Error: unable to extract price/volatility data.")
        return

    # Calculate the option price using the Black-Scholes formula
    option_price = black_scholes(current_price, K, T, r, volatility, option_type)

    # Define the order JSON object and convert it to a string
    order = {'symbol': 'AMZN', 'price': option_price, 'type': option_type, 'quantity': 1}
    json_order = json.dumps(order)

    # Use AWS Lambda to place the order automatically
    lambda_endpoint = 'https://The_lambda_function_URL'
    lambda_headers = {'Content-Type': 'application/json'}
    try:
        lambda_response = requests.post(lambda_endpoint, headers=lambda_headers, data=json_order)
        lambda_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Lambda request failed: {e}")
        return

    # Printing the order confirmation
    print(lambda_response.text)


# Calling the main function repeatedly at a fixed interval
while True:
    trade_bot()
    time.sleep(300)  # 5 minutes

