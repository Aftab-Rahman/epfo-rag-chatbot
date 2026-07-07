#### Chatbot





##### Tools to Use

|PostgreSQL --> Pg-vector|PostgreSQL is used for database setup|Pg-vector is used to embed the data in numerical constraints|
|-|-|-|
|**RAG**: It is used for embedding the data|||
||||
||||
||||





Day 0



Amitji Assigned a project to create while understanding the process



This is about a chatbot working with the given data within the boundaries

Q1. What is my work?

* Create a Database

  1. database is created through Postgre sql
  2. For this data base we create a embedding through Pgvector



Day 1



* Understanding Rag and its uses

  1. Rag is used for







##### notepad database.py



1\.	sample data to check it run successfully



import psycopg2



try:

&#x20;   conn = psycopg2.connect(

&#x20;       host="localhost",

&#x20;       database="chatbot\_db",

&#x20;       user="postgres",

&#x20;       password="your\_password"  --> "0011"

&#x20;   )



&#x20;   cursor = conn.cursor()

&#x20;   print("✅ Connected successfully!")



except Exception as e:

&#x20;   print("❌ Error:", e)



2\.	Replace everything with this:



import psycopg2



conn = psycopg2.connect(

&#x20;   host="localhost",

&#x20;   database="chatbot\_db",

&#x20;   user="postgres",

&#x20;   password="0011"

)



cursor = conn.cursor()



\# Chatbot loop

while True:

&#x20;   question = input("\\nAsk a question (type 'exit' to quit): ")



&#x20;   if question.lower() == "exit":

&#x20;       print("Goodbye 👋")

&#x20;       break



&#x20;   cursor.execute(

&#x20;       "SELECT answer FROM faq WHERE question = %s",

&#x20;       (question,)

&#x20;   )



&#x20;   result = cursor.fetchone()



&#x20;   if result:

&#x20;       print("Answer:", result\[0])

&#x20;   else:

&#x20;       print("Answer not found")





import json



with open("data.json", "r") as f:

&#x20;   data = json.load(f)



print(len(data))

print(data\[0])

