from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_id_card():
    name = request.form['name']
    age = request.form['age']
    company = request.form['company']
    department = request.form['department']

    id_number = company + str(random.randint(100000, 999999))

    id_card = f"""
    ID Card
    ----------------
    Name: {name}
    Age: {age}
    Department-Company: {department} {company}
    ID Number: {id_number}
    """

    return render_template('id_card.html', id_card=id_card)

if __name__ == "__main__":
    app.run(debug=True)