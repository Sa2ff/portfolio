from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '3f2e9c03a0b14589c2d98f2e5f47df1b')

# ─── Page Routes ───────────────────────────────────────────
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ─── Contact Form ───────────────────────────────────────────
@app.route('/submit-form', methods=['POST'])
def submit_form():
    name    = request.form.get('name')
    email   = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    try:
        msg = MIMEMultipart()
        msg['From']    = os.getenv('EMAIL_USER')
        msg['To']      = os.getenv('EMAIL_USER')
        msg['Subject'] = f"Portfolio Contact: {subject} - from {name}"

        body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        smtp.sendmail(os.getenv('EMAIL_USER'), os.getenv('EMAIL_USER'), msg.as_string())
        smtp.quit()

        flash('Your message has been sent successfully!', 'success')

    except Exception as e:
        flash(f'Something went wrong: {str(e)}', 'danger')

    return redirect(url_for('contact'))

# ─── Run ────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)