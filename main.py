import streamlit as st
import re

# For input st.text_input, For output st.write
st.title("PASSWORD STRENGTH CHECKER : ")
password = st.text_input("Enter your password : ")
strength_score = len(password) - 5

if password.isalnum() : strength_score += 1 # Contain Number
else : strength_score += 2                  # Contain Special Character
if any(char.isupper() for char in password) : strength_score += 1 # Contain Upper case letter
if any(char.islower() for char in password) : strength_score += 1 # Contain Lower case letter

st.write(strength_score)
