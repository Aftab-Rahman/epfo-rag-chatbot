import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="chatbot_db",
    user="postgres",
    password="0011"
)

cursor = conn.cursor()

# Chatbot loop
while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        print("Goodbye")
        break


import json

with open("data.json", "r") as f:
    data = json.load(f)

print(len(data))
print(data[0])
cursor.execute(
        "SELECT answer FROM faq WHERE Lower(question) = LOWER(ILIKE %s)",
        (question,)
    )

    result = cursor.fetchone()

    if result:
        print("\nBot:", result[0])
    else:
        print("\nBot: Answer not found")
        