import streamlit as st
evaluation_string = st.text_input("Enter the expression to be evaluated : ")
answer = eval(str(evaluation_string))
st.write(
  f"""
  ### ANSWER:
    {answer}
  """
)
