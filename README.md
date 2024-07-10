# Payment Gateway

This is a simple Payment Gateway API built using Flask for the backend and a frontend component using Dash and Bootstrap. 
The application allows merchants to process payments and retrieve payment details.

## Features

1. **Process Payment**: Allows merchants to process a payment.
2. **Retrieve Payment**: Allows merchants to retrieve the details of a previously made payment.

## Project Structure

```
paymentGateway/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── bank_simulator.py
│   ├── requirements.txt
├── frontend/
│   ├── app.py
│   ├── requirements.txt
├── README.md
```

## Backend

### Setup

1. **Navigate to the backend directory**:

```bash
cd backend
```

2. **Create and activate a virtual environment** (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the Flask application**:

```bash
python3 app.py
```

The backend server will start on `http://127.0.0.1:5000`.

### API Endpoints

#### Process Payment

- **URL**: `/process_payment`
- **Method**: `POST`
- **Description**: Processes a payment.
- **Request Body**:

```json
{
    "merchant_id": "string",
    "card_number": "string",
    "expiry_month": "int",
    "expiry_year": "int",
    "amount": "float",
    "currency": "string",
    "cvv": "string"
}
```

- **Response**:

```json
{
    "payment_id": "string",
    "status": "string"
}
```

#### Retrieve Payment

- **URL**: `/retrieve_payment/<payment_id>`
- **Method**: `GET`
- **Description**: Retrieves the details of a previously made payment.
- **Response**:

```json
{
    "payment_id": "string",
    "merchant_id": "string",
    "masked_card_number": "string",
    "expiry_month": "int",
    "expiry_year": "int",
    "amount": "float",
    "currency": "string",
    "status": "string"
}
```

### Example Requests

#### Process Payment

```bash
curl -X POST http://localhost:5000/process_payment \
    -H "Content-Type: application/json" \
    -d '{
        "merchant_id": "merchant123",
        "card_number": "4111111111111111",
        "expiry_month": 12,
        "expiry_year": 2024,
        "amount": 100.0,
        "currency": "USD",
        "cvv": "123"
    }'
```

#### Retrieve Payment

```bash
curl -X GET http://localhost:5000/retrieve_payment/<payment_id>
```

Replace `<payment_id>` with the actual payment ID you received from the `process_payment` response.

## Frontend

### Setup

1. **Navigate to the frontend directory**:

```bash
cd frontend
```

2. **Create and activate a virtual environment** (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the Dash application**:

```bash
python3 app.py
```

The frontend server will start on `http://127.0.0.1:8050`.
