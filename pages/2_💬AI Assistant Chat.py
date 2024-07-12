import streamlit as st
import sqlite3
import pandas as pd
import csv
from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from datetime import datetime, timezone
import pytz

# Function to create SQLite table and import data from CSV
def create_table_from_csv():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    
    # Create the transactions table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 Category TEXT,
                 CustomerName TEXT,
                 CustomerNumber INTEGER,
                 InvoiceNumber TEXT,
                 InvoiceAmount TEXT,
                 InvoiceDate TEXT,
                 DueDate TEXT,
                 ForecastCode TEXT,
                 ForecastDate TEXT,
                 Collector TEXT
                 )''')

    # Read data from CSV and insert into SQLite table
    with open('transactions.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for row in csvreader:
            c.execute('INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
    
    conn.commit()
    conn.close()

# Call the function to create the table and import data
create_table_from_csv()

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('history.db', check_same_thread=False)
    return conn

# Initialize IBM Watson Machine Learning client
wml_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": "hkEEsPjALuKUCakgA4IuR0SfTyVC9uT0qlQpA15Rcy8U"
}

client = APIClient(wml_credentials)

# Define model credentials and parameters
my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": "hkEEsPjALuKUCakgA4IuR0SfTyVC9uT0qlQpA15Rcy8U"
}

params = {
    GenParams.TEMPERATURE: 0.1,
    GenParams.MAX_NEW_TOKENS: 1000,
}

# Load the WatsonxLLM model
LLAMA2_model = Model(
    model_id='meta-llama/llama-2-70b-chat',
    credentials=my_credentials,
    params=params,
    project_id="16acfdcc-378f-4268-a2f4-ba04ca7eca08",
)

llm = WatsonxLLM(LLAMA2_model)

# Function to handle inquiry submission
def run_inquiry(inquiry):
    conn = get_db_connection()

    # Construct SQL query based on the inquiry text
    query = f"SELECT * FROM transactions WHERE {inquiry} ORDER BY InvoiceDate DESC"

    try:
        # Perform model inference
        response = llm.invoke(input=query)
    except Exception as e:
        response = f"Error occurred: {str(e)}"
    
    conn.close()

    return response


# Function to fetch transactions from database
def fetch_transactions():
    conn = get_db_connection()
    cursor = conn.execute('SELECT DISTINCT * FROM transactions ORDER BY InvoiceDate DESC')
    transactions = cursor.fetchall()
    conn.close()

    # Convert fetched data into DataFrame
    df = pd.DataFrame(transactions, columns=['Category', 'CustomerName', 'CustomerNumber', 'InvoiceNumber', 'InvoiceAmount',
                                             'InvoiceDate', 'DueDate', 'ForecastCode', 'ForecastDate', 'Collector'])
    # Add 1 to index to make it 1-based
    df.index = df.index + 1

    return df

# Initialize Streamlit app
def main():
    st.title('Text-To-Watsonx : Engage AR')

    # Introduction section
    st.markdown("""
        Welcome to the Text-To-Watsonx : Engage AR.
        Here, you can inquire about various aspects of Engage AR transactions.
        Use the example queries as a guide to format your questions.
        **Important: AI responses can vary, you might need to fine-tune your prompt template or LLM for improved results.**
    """)

    # Example inquiries section (optional)
    st.markdown("**Example Inquiries:**")
    st.markdown("- What are the items with a due date after today?")
    st.markdown("- Show me the list where the collector is Lisa and the category is Yellow!")
    st.markdown("- Show me the list where the collector is David and the forecast code is AUTO!")
    st.markdown("- Show me the list where the collector is John and the forecast date is after August!")
    st.markdown("- How many AUTO in Forecastcode per collector?")
    st.markdown("- How many invoice numbers with due date greater than August 10th 2024?")
    st.markdown("- How many green per collector in category?")

    # Form for inquiry submission
    inquiry = st.text_input('Submit an Inquiry:', '')

    if st.button('Submit'):
        response = run_inquiry(inquiry)
        st.markdown(f"**Response:**")
        st.write(response)

    # Display transactions table using Pandas DataFrame
    st.markdown("**Transactions:**")
    transactions = fetch_transactions()
    st.dataframe(transactions)

    # Custom CSS for table styling
    st.markdown(
        """
        <style>
        table.dataframe {
            border: 2px solid #5e5e5e; /* Darker gray than default */
            text-align: center; /* Center align text in cells */
        }
        th {
            border: 2px solid #5e5e5e; /* Darker gray than default */
            text-align: center; /* Center align text in header cells */
        }
        td {
            border: 2px solid #5e5e5e; /* Darker gray than default */
            text-align: center; /* Center align text in data cells */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
     
    st.markdown(
    """
    <style>
    table.dataframe {
        width: 100%;
        table-layout: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if __name__ == '__main__':
    main()
