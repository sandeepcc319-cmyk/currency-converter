import streamlit as st
import requests

st.title("💱 Simple Currency Converter")
st.write("Convert an amount from one currency to another in real time.")

# Sidebar inputs
amount = st.sidebar.number_input("Enter amount:", min_value=0.0, value=1.0, format="%.2f")
from_currency = st.sidebar.text_input("From Currency (e.g. USD):", value="USD").upper()
to_currency = st.sidebar.text_input("To Currency (e.g. INR):", value="INR").upper()

# Optional: put your API key here (if required)
API_KEY = st.sidebar.text_input("exchangerate.host Access Key (if needed):", value="").strip()

def get_rate(frm, to, amount):
    base_url = "https://api.exchangerate.host/convert"
    params = {
        "from": frm,
        "to": to,
        "amount": amount
    }
    # If API_KEY is provided, include it
    if API_KEY:
        params["access_key"] = API_KEY

    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()  # will throw HTTPError for 4xx/5xx
    data = response.json()
    return data

if st.sidebar.button("Convert"):
    try:
        data = get_rate(from_currency, to_currency, amount)
        # Check if API says success
        if ("success" in data and data["success"] is False):
            st.error(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")
        else:
            # If data has result field
            result = data.get("result", None)
            rate = None
            if result is not None:
                st.success(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}")
            else:
                # maybe structure is different
                rate = data.get("info", {}).get("rate", None)
                if rate is not None:
                    result_calc = rate * amount
                    st.success(f"{amount:.2f} {from_currency} ≈ {result_calc:.2f} {to_currency} (rate: {rate:.4f})")
                else:
                    st.error("Unexpected API response structure.")
        # For debugging: show full JSON (optional)
        st.write("Raw API response:", data)
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        st.error("Error connecting to the API. Check network or URL.")
    except requests.exceptions.Timeout:
        st.error("Request timed out.")
    except Exception as e:
        st.error(f"Some error occurred: {str(e)}")

st.caption("Powered by exchangerate.host API")