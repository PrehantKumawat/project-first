import streamlit as st
evalutation_string = st.text_input("Enter the expression to be evaluated : ")
eval(evaluation_string)
