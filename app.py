
from flask import Flask, render_template, request, redirect, url_for, session
from models.user_model import User
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# OpenAI API Key (Replace with your key)
openai.api_key = "your_openai_api_key"

@app.route('/')
def home():
    return render_template('index.html', user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.authenticate(email, password)
        if user:
            session['user'] = user['name']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if User.register(name, email, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')

@app.route('/tutoring', methods=['GET', 'POST'])
def tutoring():
    if 'user' not in session:
        return redirect(url_for('login'))
    ai_response = None
    if request.method == 'POST':
        question = request.form['question']
        ai_response = ask_ai(question)
    return render_template('tutoring.html', user=session['user'], ai_response=ai_response)

def ask_ai(question):
    prompt = f"Provide detailed chemistry tutoring on: {question}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
