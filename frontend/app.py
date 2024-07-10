import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import requests

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Payment Gateway"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Label("Merchant ID"),
                dbc.Input(id="merchant_id", type="text", placeholder="Enter Merchant ID"),
            ]),
            dbc.CardGroup([
                dbc.Label("Card Number"),
                dbc.Input(id="card_number", type="text", placeholder="Enter Card Number"),
            ]),
            dbc.CardGroup([
                dbc.Label("Expiry Month"),
                dcc.Dropdown(
                    id="expiry_month",
                    options=[{"label": f"{i:02d}", "value": i} for i in range(1, 13)],
                    placeholder="Select Expiry Month"
                )
            ]),
            dbc.CardGroup([
                dbc.Label("Expiry Year"),
                dcc.Dropdown(
                    id="expiry_year",
                    options=[{"label": str(i), "value": i} for i in range(2023, 2053)],
                    placeholder="Select Expiry Year"
                )
            ]),
            dbc.CardGroup([
                dbc.Label("Amount"),
                dbc.Input(id="amount", type="number", placeholder="Enter Amount"),
            ]),
            dbc.CardGroup([
                dbc.Label("Currency"),
                dbc.Input(id="currency", type="text", placeholder="Enter Currency"),
            ]),
            dbc.CardGroup([
                dbc.Label("CVV"),
                dbc.Input(id="cvv", type="password", placeholder="Enter CVV"),
            ]),
            dbc.Button("Process Payment", id="process_payment_button", color="primary"),
            html.Div(id="payment_status", className="mt-3")
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Input(id="payment_id_input", type="text", placeholder="Enter Payment ID to Retrieve Details"),
            dbc.Button("Retrieve Payment", id="retrieve_payment_button", color="secondary", className="mt-2"),
            html.Div(id="payment_details", className="mt-3")
        ], width=6)
    ])
])

@app.callback(
    Output("payment_status", "children"),
    Input("process_payment_button", "n_clicks"),
    State("merchant_id", "value"),
    State("card_number", "value"),
    State("expiry_month", "value"),
    State("expiry_year", "value"),
    State("amount", "value"),
    State("currency", "value"),
    State("cvv", "value")
)
def process_payment(n_clicks, merchant_id, card_number, expiry_month, expiry_year, amount, currency, cvv):
    if n_clicks:
        response = requests.post("http://127.0.0.1:5000/process_payment", json={
            "merchant_id": merchant_id,
            "card_number": card_number,
            "expiry_month": expiry_month,
            "expiry_year": expiry_year,
            "amount": amount,
            "currency": currency,
            "cvv": cvv
        })
        if response.status_code == 200:
            result = response.json()
            return f"Payment Status: {result['status']}, Payment ID: {result['payment_id']}"
        else:
            return "Error processing payment"
    return ""

@app.callback(
    Output("payment_details", "children"),
    Input("retrieve_payment_button", "n_clicks"),
    State("payment_id_input", "value")
)
def retrieve_payment(n_clicks, payment_id):
    if n_clicks:
        response = requests.get(f"http://127.0.0.1:5000/retrieve_payment/{payment_id}")
        if response.status_code == 200:
            payment = response.json()
            return html.Div([
                html.P(f"Payment ID: {payment['payment_id']}"),
                html.P(f"Merchant ID: {payment['merchant_id']}"),
                html.P(f"Masked Card Number: {payment['masked_card_number']}"),
                html.P(f"Expiry Month: {payment['expiry_month']}"),
                html.P(f"Expiry Year: {payment['expiry_year']}"),
                html.P(f"Amount: {payment['amount']}"),
                html.P(f"Currency: {payment['currency']}"),
                html.P(f"Status: {payment['status']}")
            ])
        else:
            return "Error retrieving payment details"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
