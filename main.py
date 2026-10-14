import streamlit as st
def count_special_characters(s):
    count = 0
    for char in s:
        if not char.isalnum():  # Checks if character is not a letter or number
            count += 1
    return count

# For input st.text_input, For output st.write
st.title("PASSWORD STRENGTH CHECKER : ")
password = st.text_input("Enter your password : ")
strength_score = len(password) - 5 + count_special_characters(password)

if any(char.isdigit() for char in password) : strength_score += 1 # Contain numbers
if any(char.isupper() for char in password) : strength_score += 1 # Contain Upper case letter
if any(char.islower() for char in password) : strength_score += 1 # Contain Lower case letter

st.write("Score : ", strength_score)
strength = "VeryBad"
if strength_score <= 5:
    strength = "Bad"
elif strength_score <= 10:
    strength = "Fine"
elif strength_score <= 15:
    strength = "Good"
elif strength_score <= 25:
    strength = "VeryGood"
st.write(strength, "Password!")
