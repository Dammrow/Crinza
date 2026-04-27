from flask import request
from flask import Flask, render_template
import sqlite3
import smtplib
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            description TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data=request.form

    business_name= data.get('business_name')
    description= data.get('description')
    phone= data.get('phone')
    email= data.get('email')
    city= data.get('city')
    state= data.get('state')
    if "@" not in email or "." not in email:
        return "Invalid email"
    if not phone.isdigit() or len(phone)!=10:
        return "Invalid phone number"
    conn = sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO registrations (business_name, description, phone, email, city, state)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (business_name, description, phone, email, city, state))
    conn.commit()
    conn.close()
    return render_template('success.html')
    try:
        server= smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('dammrow112@gmail.com','uofh twtk mfee stni')
        message = f"""Subject: New Registration
        New Registration Received:
        Business Name: {business_name}
        Description: {description}
        Phone: {phone}
        Email: {email}
        City: {city}
        State: {state}
        """

        server.sendmail('dammrow112@gmail.com', 'dammrow112@gmail.com', message)
        server.quit()
        
    except Exception as e:
       print("email error:", e)

    return 'Registration successfull'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))