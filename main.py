import streamlit as st
import smtplib
import re
import os
import ssl
from email.mime.text import MIMEText
from datetime import datetime


def send_email(name, organisation, email):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.example.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    subject = f"Volunteer registration for The Project - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"Name: {name}\nOrganisation: {organisation}\nEmail: {email}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False


def registration_form_with_indemnity():
    # Set page configuration with favicon
    st.set_page_config(
        page_title="JBay Project Volunteer Registration", page_icon="🛢")

    # Display logo image
    st.image("logo.jpeg", width=200)

    st.title("Volunteer Registration Form")

    # Capture Name, Phone Number, and Email
    name = st.text_input("Full Name")
    organisation = st.text_input("Organisation Name")
    email = st.text_input("Email Address")

    # Email validation
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Indemnity Policy
    indemnity_text = """
    By participating in this recycling project, you agree to the following terms:
    
    1. You acknowledge that you are participating at your own risk.
    2. The recycling project and its coordinators are not liable for any injuries or accidents that may occur.
    3. You agree to indemnify and hold harmless the recycling project, its staff, and volunteers from any claims or liabilities.
    
    Please read the above terms carefully before participating.
    """

    st.markdown(indemnity_text)
    agree_to_terms = st.checkbox(
        "I have read and agree to the indemnity policy")

    # Check if all fields are filled and terms are accepted
    if st.button("Submit"):
        if not name or not organisation or not email:
            st.error("Please fill in all fields.")
        elif not organisation.strip():  # Check if organisation is not just whitespace
            st.error("Please enter a valid organisation name.")
        elif not re.match(email_pattern, email):
            st.error("Please enter a valid email address.")
        elif not agree_to_terms:
            st.error("You must accept the indemnity policy to proceed.")
        else:
            if send_email(name, organisation, email):
                st.success(
                    f"Thank you for registering, {name}! Your details have been sent.")


# Run the combined registration form with indemnity policy
registration_form_with_indemnity()
