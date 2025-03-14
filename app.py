from flask import Flask, render_template, request, redirect, flash
import psycopg2
import os

app = Flask(__name__)

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded .env for development")

app.secret_key = os.environ.get("SECRET_KEY")

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT', 5432)
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, role, bio, image_url FROM developer_profile LIMIT 1;")
    profile = cur.fetchone()
    conn.close()
    return render_template('index.html', profile=profile)

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        conn.close()
        flash('Message sent successfully!', 'success')
    except Exception as e:
        flash('Something went wrong. Please try again.', 'error')
    
    return redirect('/contact')

if __name__ == '__main__':
    app.run(debug=True)
