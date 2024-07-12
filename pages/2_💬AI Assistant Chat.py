from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    transactions = conn.execute('SELECT id, * FROM transactions ORDER BY InvoiceDate DESC').fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions)

# Creating the Prompt Template
# Initializing the Database Chain
# Interacting with the Database
# Running the App

# LLaMA uses [INST] and [/INST] to indicate user messages, and <<SYS>> and <</SYS>> to indicate system messages
QUERY = """
<<SYS>> 
You are a powerful text-to-SQLite model, and your role is to answer questions about a database. You are given questions and context regarding the Invoice details table, which represents the detailed records of currently open invoices.
The table name is {table_name} and corresponding columns are {columns}.
You must run SQLite queries to the table to find an answer. Ensure your query does not include any non-SQLite syntax such as DATE_TRUNC or any use of backticks (`) or "```sql". Then, execute this query against the 'transactions' table and provide the answer.

Guidelines:
- Filter results using the current time zone: {time} only when query specifis a specific date/time period. You should use ">=" or "<=" operators to filter the date or use "GROUP BY strftime('%m', date)" for grouping into month.  Assume the date format in the database is 'YYYY-MM-DD'.
- If the query result is [(None,)], run the SQLite query again to double check the answer. 
- If a specific category is mentioned in the inquiry, such as 'Yellow', 'Red', or 'Green', use the "WHERE" condition in your SQL query to filter transactions by that category. For example, when asked for the complete invoice details for 'Green', use "FROM transactions WHERE category = 'Green'".
- If not asked for a specific category, you shouldn't filter any category out. On the other hand, you should use "where" condition to do the filtering. When asked for the average amount in a category, use the SQLite query (AVG(amount) WHERE category = 'category_name').
- When asked for \'highest\' or \'lowest\', use SQL function MAX() or MIN() respectively.
-If a specific condition is provided in the inquiry, such as mentioning a specific Collector like 'John', 'David', 'Lisa', 'Mary', or 'Michael', and specifying a category such as 'Yellow', 'Red', or 'Green', use the "WHERE" clause in your SQL query to filter transactions accordingly. For example, if you need to fetch invoice details for 'John' and 'Green', you would use "FROM transactions WHERE Collector = 'John' AND category = 'Green'".

Use the following format to answer the inquiry:

Response: Result of the SQLite-compatible SQL query. If you know the transaction details such as the Category,  Customer Name, Customer #, Inv. #, Inv. Amt, Inv. Date, Due Date, Forecast Code, Forecast Date, and Collector, mention it in your answer to be more clear.
---------------------- line break
<br>
---------------------- line break
<br>
Explanation: Concise and succinct explanation on your thought process on how to get the final answer including the relevant transaction details such as the Category,   Customer Name, Customer #, Inv. #, Inv. Amt, Inv. Date, Due Date, Forecast Code, Forecast Date, and Collector.
---------------------- line break
<br>
---------------------- line break
<br>
Advice: Provide tips here, such as reminding users of progress for invoices with a due date within 10 days by comparing the due date with today.

<</SYS>>

[INST] 
{inquiry}
[/INST]
"""

from db import *
from langchain_experimental.sql import SQLDatabaseChain
from model import llm

# Create the database chain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

from datetime import datetime
import pytz

@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    inquiry = request.form['inquiry']

    # Handle transaction queries
    prompt = QUERY.format(table_name=table_name, columns=columns, time=datetime.now(pytz.timezone('America/New_York')), inquiry=inquiry)
    response = db_chain.run(prompt)

    # Fetch transactions data again to pass to the template
    conn = get_db_connection()
    cursor = conn.execute('SELECT id, * FROM transactions ORDER BY InvoiceDate DESC')
    transactions = [dict(ix) for ix in cursor.fetchall()]
    conn.close()

    # Replace newline characters with HTML break tags
    response = response.replace('\n', '<br>')
    
    return render_template('index.html', inquiry=prompt, answer=response, transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
