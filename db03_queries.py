# db03_queries.py
# Runs various queries and displays results.
import pandas as pd

def run_query(query):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

queries = {
    "Aggregation": "SELECT category, COUNT(*) as count, AVG(sentiment) as avg_sentiment FROM buzzline_messages GROUP BY category;",
    "Filter": "SELECT * FROM buzzline_messages WHERE sentiment > 0.5;",
    "Sorting": "SELECT * FROM buzzline_messages ORDER BY sentiment DESC;",
    "Group By": "SELECT category, COUNT(*) FROM buzzline_messages GROUP BY category;",
    "Join": "SELECT users.name, buzzline_messages.message, buzzline_messages.sentiment FROM users JOIN buzzline_messages ON users.id = buzzline_messages.author_id;"
}

for name, query in queries.items():
    print(f"\n{name} Query Results:")
    print(run_query(query))

print("Queries executed successfully!")