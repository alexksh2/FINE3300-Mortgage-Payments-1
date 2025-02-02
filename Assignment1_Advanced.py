import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
# Use a pipeline as a high-level helper

from transformers import AutoModelForCausalLM, AutoTokenizer
from groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


def printing_output():
    client = Groq(api_key=API_KEY)
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{
            'role':'user',
            'content':'State three benefits and losses of having higher frequency payment for loan payment. Just provide me the answer dont give me your reasoning or I will sack you!!!!  Explain in a third person narrative and give three bullet points.'}],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True,
        stop=None,
    )
    
    full_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        full_response += content

    return full_response




def mortgage_payments(principal, rate, amortization):
    # Calculate the total number of periods for each case using amortization (in years)
    monthly_periods = amortization * 12
    semi_monthly_periods = amortization * 24
    bi_weekly_periods = amortization * 26
    weekly_periods = amortization * 52

    # Calculate periodic rates using the nominal interest rate e.g. rate
    monthly_rate = (1 + rate / 2) ** (2 / 12) - 1
    semi_monthly_rate = (1 + rate / 2) ** (2 / 24) - 1
    bi_weekly_rate = (1 + rate / 2) ** (2 / 26) - 1
    weekly_rate = (1 + rate / 2) ** (2 / 52) - 1

    # Function to Calculate the Present Value of Annuity Factor (PVA)
    def pva(r, n):
        return (1 - (1 + r) ** -n) / r

    # Calculate the individual payments
    monthly_payment = principal / pva(monthly_rate, monthly_periods)
    semi_monthly_payment = principal / pva(semi_monthly_rate, semi_monthly_periods)
    bi_weekly_payment = principal / pva(bi_weekly_rate, bi_weekly_periods)
    weekly_payment = principal / pva(weekly_rate, weekly_periods)

    #Accelerated Bi-weekly payments are also made every two weeks. The payment is equal to half the monthly amount.
    rapid_bi_weekly_payment = monthly_payment * 13 / 26  
    #Accelerated Weekly payments are also made every week. The payment is equal to one-quarter of the monthly amount.
    rapid_weekly_payment = monthly_payment * 13 / 52

    return (monthly_payment, semi_monthly_payment, bi_weekly_payment, 
            weekly_payment, rapid_bi_weekly_payment, rapid_weekly_payment)

# Streamlit App
st.title("Welcome to Mortgage Payment Calculator")
            
# User Inputs on SideBar
st.sidebar.header("Input Parameters")
principal = st.sidebar.number_input("Loan Amount (Principal)", value=100000, step=1000)
rate = st.sidebar.number_input("Annual Interest Rate (e.g., 0.05 for 5%)", value=0.05, step=0.01)
amortization = st.sidebar.number_input("Amortization Period (Years)", value=25, step=1)

# Checking User Input
if principal <= float(0):
    st.error("Principal amount must be greater than 0.")
    st.stop()
elif rate <= float(0):
    st.error("Annual interest rate must be greater than 0.")
    st.stop()
elif amortization <= float(0):
    st.error("Amortization period must be greater than 0.")
    st.stop()
else:
    # Proceed with calculations if inputs are valid
    st.success("Inputs are valid! Proceeding with calculations...")
    # Add your mortgage payment calculation logic here

# Calculate Payments
payments = mortgage_payments(principal, rate, amortization)

# Display Results
st.subheader("Payment Details")
st.markdown(f"<p style='font-size:16px;'>Monthly Payment: ${payments[0]:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:16px;'>Semi-Monthly Payment: ${payments[1]:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:16px;'>Bi-Weekly Payment: ${payments[2]:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:16px;'>Weekly Payment: ${payments[3]:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:16px;'>Rapid Bi-Weekly Payment: ${payments[4]:,.2f}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:16px;'>Rapid Weekly Payment: ${payments[5]:,.2f}</p>", unsafe_allow_html=True)
st.markdown("---")


st.header("Payment Amount Comparison per Period")

# Labels and values
labels = [
    "Monthly",
    "Semi-Monthly",
    "Bi-Weekly",
    "Weekly",
    "Rapid Bi-Weekly",
    "Rapid Weekly",
]
values = [
    payments[0],
    payments[1],
    payments[2],
    payments[3],
    payments[4],
    payments[5],
]

# Create a bar chart using Plotly
fig = go.Figure(
    data=[
        go.Bar(
            x=labels,
            y=values,
            text=[f"${val:,.2f}" for val in values],  # Add values as text
            textposition="auto",  # Display text on the bars
        )
    ]
)

# Update layout for better visualization
fig.update_layout(
    title="Mortgage Payments by Frequency",
    xaxis_title="Payment Frequency",
    yaxis_title="Payment Amount per Period ($)",
    xaxis=dict(tickangle=45),  # Rotate x-axis labels
    template="plotly_white",  # Clean theme
)

# Display the chart in Streamlit
st.plotly_chart(fig)


st.header("Financial Advice by DeepSeek Model")

st.markdown(f"""
                <div style="padding:15px; border-radius:5px;">
                    <p style="font-size: 16px; ">{printing_output()}</p>
                </div>
            """, unsafe_allow_html=True)
