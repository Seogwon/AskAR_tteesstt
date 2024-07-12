import streamlit as st
import sqlite3
from datetime import datetime
import csv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM

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

# Define your credentials and parameters
my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": "hkEEsPjALuKUCakgA4IuR0SfTyVC9uT0qlQpA15Rcy8U"
}

params = {
    'MAX_NEW_TOKENS': 1000,
    'TEMPERATURE': 0.1,
}

LLAMA2_model = Model(
    model_id='meta-llama/llama-2-70b-chat',
    credentials=my_credentials,
    params=params,
    project_id="16acfdcc-378f-4268-a2f4-ba04ca7eca08",
)

llm = WatsonxLLM(LLAMA2_model)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('history.db', check_same_thread=False)
    return conn

# Function to handle inquiry submission
def run_inquiry(inquiry):
    conn = get_db_connection()

    # Create SQL query based on the inquiry text
    QUERY = f"""SELECT * FROM transactions WHERE {inquiry} ORDER BY InvoiceDate DESC"""
    
    try:
        # Placeholder for query execution using WatsonxLLM or other logic
        response = llm.run(prompt=QUERY)
    except Exception as e:
        response = f"Error occurred: {str(e)}"
    
    conn.close()

    return response

# Function to fetch transactions from database
def fetch_transactions():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM transactions ORDER BY InvoiceDate DESC')
    transactions = cursor.fetchall()
    conn.close()
    return transactions

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

    # Display transactions table
    st.markdown("**Transactions:**")
    transactions = fetch_transactions()[:21]  # Limit to first 20 rows
    st.table(transactions)

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

if __name__ == '__main__':
    main()
