import streamlit as st
import smtplib
import re
import os
from email.mime.text import MIMEText
from datetime import datetime

def send_email(name, phone, email):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    subject = f"Volunteer registration for The Project - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"Name: {name}\nPhone: {phone}\nEmail: {email}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def registration_form_with_indemnity():
    st.title("Volunteer Registration Form")
    
    # Capture Name, Phone Number, and Email
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    
    # Email validation
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Phone number validation (only digits)
    phone_pattern = r'^\d+$'
    
    # Indemnity Policy
    indemnity_text = """
    By participating in this recycling project, you agree to the following terms:
    
    1. You acknowledge that you are participating at your own risk.
    2. The recycling project and its coordinators are not liable for any injuries or accidents that may occur.
    3. You agree to indemnify and hold harmless the recycling project, its staff, and volunteers from any claims or liabilities.
    
    Please read the above terms carefully before participating.
    """
    
    st.markdown(indemnity_text)
    agree_to_terms = st.checkbox("I have read and agree to the indemnity policy")
    
    # Check if all fields are filled and terms are accepted
    if st.button("Submit"):
        if not name or not phone or not email:
            st.error("Please fill in all fields.")
        elif not re.match(phone_pattern, phone):
            st.error("Please enter a valid phone number (digits only).")
        elif not re.match(email_pattern, email):
            st.error("Please enter a valid email address.")
        elif not agree_to_terms:
            st.error("You must accept the indemnity policy to proceed.")
        else:
            if send_email(name, phone, email):
                st.success(f"Thank you for registering, {name}! Your details have been sent.")

# Run the combined registration form with indemnity policy
registration_form_with_indemnity()