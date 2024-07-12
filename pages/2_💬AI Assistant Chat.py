import streamlit as st
import sqlite3
from datetime import datetime
import pytz
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

# Connect to SQLite database
db = SQLDatabase.from_uri("sqlite:///history.db")

# Initialize SQLDatabaseChain instance
from model import llm_hub  # Assuming llm_hub is imported correctly from your model.py

# Create db chain
QUERY = """
<s>[INST] 
You are a powerful text-to-SQLite model. Your job is to answer questions about a database. You are given a question and context regarding the table of credit card transaction records which represents a person's expense records. You must run SQLite queries to the table to find an answer. Ensure your query does not include any non-SQLite syntax such as DATE_TRUNC or any use of backticks (`) or "```sql". Then, execute this query against the 'transactions' table and provide the answer. 
Provide strategies to manage expenses or tips to reduce the expenses in your answer as well. Compare the result with the spending in the previous months if any and include the insights in your answer.

Guidelines:
- Include all transactions if no specific date/time is mentioned. However, filter results to a specific date/time period using the current time zone: {time}. You should use ">=" or "<=" operators to filter the date or use "GROUP BY strftime('%m', date)" for grouping.  Assume the date format in the database is 'YYYY-MM-DD'.
- If the query result is [(None,)], run the SQLite query again to double check the answer. 
- If a specific category is mentioned in the inquiry, such as 'Groceries', 'Dining', or 'Utilities', use the "WHERE" condition in your SQL query to filter transactions by that category. For example, when asked for the average amount spent on 'Groceries', use "SELECT AVG(amount) FROM transactions WHERE category = 'Groceries'".
- If not asked for a specific category, you shouldn't filter any category out. On the other hand, you should use "where" condition to do the filtering. When asked for the average amount in a category, use the SQLite query (AVG(amount) WHERE category = 'category_name').
- When asked for \'highest\' or \'lowest\', use SQL function MAX() or MIN() respectively.

<<SYS>>
Use the following format to answer the inquiry:

Response: Result of the SQLite-compatible SQL query. If you know th transaction detailes such as the date, category, merchant, and amount, mention it in your answer to be more clear. - When asked for an \'overview\' of transactions, analyze and present the data in a way that highlights the proportions of different categories or types of transactions. For instance, calculate the percentage each category (like \'Groceries\', \'Dining\', \'Utilities\') contributes to the total transactions or total spending.
---------------------- line break
<br>
---------------------- line break
<br>
Explanation: Concise and succinct explanation on your thought process on how to get the final answer including the relevant transaction details such as the date, category, merchant, and amount.
---------------------- line break
<br>
---------------------- line break
<br>
Advice: Provide strategies to manage expenses or tips to reduce the expenses here.
<</SYS>>

{inquiry}
[/INST]
"""

# Function to fetch transactions from database
def fetch_transactions():
    conn = sqlite3.connect('history.db', check_same_thread=False)
    cursor = conn.execute('SELECT id, * FROM transactions ORDER BY date DESC')
    transactions = [dict(ix) for ix in cursor.fetchall()]
    conn.close()
    return transactions

# Function to handle inquiry submission
def handle_inquiry(inquiry):
    prompt = QUERY.format(time=datetime.now(pytz.timezone('America/New_York')), inquiry=inquiry)
    response = db_chain.run(prompt)
    response = response.replace('\n', '<br>')
    return response

# Streamlit UI components
st.title('Invoice Inquiry System')
inquiry = st.text_area('Enter your inquiry:')
if st.button('Submit'):
    response = handle_inquiry(inquiry)
    st.markdown(f"**Response:** {response}")

# Display transactions
transactions = fetch_transactions()
st.write('Recent Transactions:')
st.write(transactions)
