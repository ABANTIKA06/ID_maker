from flask import Flask, render_template, request, flash
import random
import psycopg2
from psycopg2 import sql, errors

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def get_db_connection():
    return psycopg2.connect(
        dbname="test",
        user="postgres",
        password="271800",  # Ensure this is the correct password
        host="localhost"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_id_card():
    name = request.form['name']
    age = request.form['age']
    company = request.form['company']
    department = request.form['department']
    Govt_Id = request.form['Govt_Id']

    id_number = company + department + str(random.randint(100000, 999999))

    id_card = f"""
    ID Card
    ----------------
    Name: {name}
    Age: {age}
    Department-Company: {department} {company}
    ID Number: {id_number}
    Govt ID: {Govt_Id}
    """

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("INSERT INTO persons (name, age, company, department, id_number, govt_id) VALUES (%s, %s, %s, %s, %s, %s)"),
                (name, age, company, department, id_number, Govt_Id)
            )
            conn.commit()
            flash("Person added successfully.", "success")
    except errors.UniqueViolation:
        conn.rollback()
        flash(f"Duplicate Govt ID found: {Govt_Id}. Please check the existing records.", "warning")
    finally:
        conn.close()

    return render_template('id_card.html', id_card=id_card, alert_message=request.args.get('alert_message'))

def insert_person(conn, name, govt_id):
    try:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("INSERT INTO persons (name, govt_id) VALUES (%s, %s)"),
                (name, govt_id)
            )
            conn.commit()
            print("Person added successfully.")
    except errors.UniqueViolation:
        conn.rollback()
        print(f"Duplicate govt_id found: {govt_id}. Searching for existing entry...")
        search_person_by_govt_id(conn, govt_id)

def search_person_by_govt_id(conn, govt_id):
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("SELECT * FROM persons WHERE govt_id = %s"),
            (govt_id,)
        )
        person = cur.fetchone()
        if person:
            print(f"Existing entry found: {person}")
        else:
            print("No existing entry found.")

if __name__ == "__main__":
    app.run(debug=True)