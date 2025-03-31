import openai
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify

# Set your API keys
openai.api_key = 'your-openai-api-key'


# Function to interact with OpenAI GPT for NLP-powered chatbot
def get_nlp_response(user_input):
    response = openai.Completion.create(
        model="gpt-4",  # You can switch between GPT-3 or GPT-4
        prompt=user_input,
        max_tokens=200
    )
    return response.choices[0].text.strip()


# Function to fetch property data from an API like Zillow or MLS (use your own API key)
def get_property_data(address):
    # Replace this with actual API call
    url = f"http://api.zillow.com/v1/property/details"
    params = {
        'address': address,
        'key': 'your-zillow-api-key',
    }
    response = requests.get(url, params=params)
    return response.json()


# Function for legal document review (use LawGeex or a similar service)
def review_legal_document(document_text):
    # Replace with actual API call to legal document review service
    url = "https://api.lawgeex.com/review"
    headers = {"Authorization": "Bearer your-api-key"}
    data = {"document": document_text}

    response = requests.post(url, json=data, headers=headers)
    return response.json()


# Function to perform financial modeling (e.g., NPV, IRR)
def financial_model(cash_flows, discount_rate=0.1):
    npv = np.npv(discount_rate, cash_flows)  # Using numpy for NPV calculation
    irr = np.irr(cash_flows)  # Calculate internal rate of return
    return npv, irr


# Function to generate a simple cash flow chart using Matplotlib
def plot_cash_flow(cash_flows):
    years = [i for i in range(len(cash_flows))]
    plt.plot(years, cash_flows, marker='o')
    plt.title('Cash Flow Over Time')
    plt.xlabel('Year')
    plt.ylabel('Cash Flow ($)')
    plt.show()


# Initialize Flask app for the web dashboard
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = get_nlp_response(user_input)
    return jsonify({"response": response})


@app.route('/financial_model', methods=['POST'])
def financial_model_route():
    data = request.json
    cash_flows = data.get('cash_flows')
    npv, irr = financial_model(cash_flows)
    return jsonify({"npv": npv, "irr": irr})


@app.route('/property_data', methods=['POST'])
def property_data_route():
    address = request.json.get('address')
    property_data = get_property_data(address)
    return jsonify(property_data)


@app.route('/legal_review', methods=['POST'])
def legal_review_route():
    document_text = request.json.get('document_text')
    review_results = review_legal_document(document_text)
    return jsonify(review_results)


if __name__ == '__main__':
    app.run(debug=True)
