import streamlit as st
import random
import string
import io
import time

# Function to generate a password
def generate_password(length, use_digits, use_special_chars, custom_special_chars, complexity):
    characters = string.ascii_letters  # Letters (a-z, A-Z)
    
    if complexity == "Easy":
        characters = string.ascii_lowercase  # Only lowercase letters
    
    if use_digits:
        characters += string.digits  # Add digits (0-9)
    
    if use_special_chars:
        characters += custom_special_chars if custom_special_chars else string.punctuation  # Custom or default special characters

    if not characters:
        return "Please select at least one option!"
    
    return ''.join(random.choice(characters) for _ in range(length))

# Function to check password strength
def check_password_strength(password):
    score = 0
    if any(char.isdigit() for char in password):
        score += 1
    if any(char.islower() for char in password) and any(char.isupper() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1
    if len(password) >= 12:
        score += 1

    if score == 4:
        return "🟢 Strong"
    elif score == 3:
        return "🟡 Medium"
    else:
        return "🔴 Weak"

# Streamlit App UI
st.set_page_config(page_title="Password Generator", layout="centered")

# Dark mode toggle
dark_mode = st.toggle("🌙 Dark Mode")
# Apply dark mode using built-in Streamlit theme settings
if dark_mode:
    st.markdown("""
        <style>
        :root {
            --primary-background-color: #0e1117;
            --secondary-background-color: #161b22;
            --text-color: white;
        }
        body {
            background-color: var(--primary-background-color);
            color: var(--text-color);
        }
        .stApp {
            background-color: var(--primary-background-color);
        }
        .stButton>button {
            background-color: #238636;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Light Grey Theme Toggle
light_grey_theme = st.toggle("🌫️ Light Grey Theme")

# Apply light grey theme using CSS
if light_grey_theme:
    st.markdown("""
        <style>
        :root {
            --primary-background-color: #f0f0f0;  /* Light Grey */
            --secondary-background-color: #e0e0e0; /* Slightly Darker Grey */
            --text-color: #333333;  /* Dark Grey Text */
            --button-bg: #d6d6d6;
            --button-hover: #bbbbbb;
        }
        body {
            background-color: var(--primary-background-color);
            color: var(--text-color);
        }
        .stApp {
            background-color: var(--primary-background-color);
        }
        .stButton>button {
            background-color: var(--button-bg);
            color: black;
            border: 1px solid #cccccc;
        }
        .stButton>button:hover {
            background-color: var(--button-hover);
        }
        .stSidebar {
            background-color: var(--secondary-background-color);
        }
        </style>
    """, unsafe_allow_html=True)

st.title("🔑 Advanced Password Generator")
st.write("Generate secure passwords with advanced features.")

# User inputs
password_length = st.slider("Select Password Length", min_value=6, max_value=32, value=12)

# Password complexity selection
complexity = st.radio("Select Password Complexity", ["Easy", "Medium", "Hard"], index=1)

use_digits = st.checkbox("Include Digits (0-9)")
use_special_chars = st.checkbox("Include Special Characters")

# Custom special characters input
custom_special_chars = ""
if use_special_chars:
    custom_special_chars = st.text_input("Enter Special Characters to Use (leave empty for default)", value="!@#$%^&*")

# Generate multiple passwords
num_passwords = st.number_input("How many passwords to generate?", min_value=1, max_value=10, value=1, step=1)

# Password expiration timer
expiration_time = st.slider("Set Password Expiration (Seconds)", min_value=10, max_value=300, value=60)

# Generate password button
if st.button("Generate Passwords"):
    passwords = [generate_password(password_length, use_digits, use_special_chars, custom_special_chars, complexity) for _ in range(num_passwords)]
    
    st.write("### Your Generated Passwords:")
    for i, password in enumerate(passwords, start=1):
        st.code(password, language="text")

    # Password Strength
    st.write(f"**Password Strength:** {check_password_strength(passwords[0])}")

    # Clipboard Copy Button using JavaScript
    for password in passwords:
        st.markdown(
            f"""
            <button onclick="navigator.clipboard.writeText('{password}')" 
            style="background-color:green; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer; margin-bottom:5px;">
            📋 Copy {password} to Clipboard</button>
            """,
            unsafe_allow_html=True
        )

    # Convert list of passwords to a single string
    password_text = "\n".join(str(p) for p in passwords)  # Ensure all items are strings

    # Save passwords to file
    buffer = io.BytesIO()
    buffer.write(password_text.encode("utf-8"))  # Encode properly
    buffer.seek(0)  # Move cursor to the beginning

    st.download_button(
        label="📥 Save Passwords",
        data=buffer,
        file_name="passwords.txt",
        mime="text/plain"
    )

    # Expiration Timer
    with st.spinner(f"These passwords will expire in {expiration_time} seconds..."):
        time.sleep(expiration_time)
        st.warning("⏳ Passwords expired! Generate new ones.")

# Footer
st.markdown("---")
st.write("Built with ❤️ by SZ Abbas using Streamlit")
