# import streamlit as st
# st.title("Calculator")
# num1 = st.floating("Enter number 1 : ")
# num2 = st.number_input("Enter number 2 : ")
# operation = st.selectbox(
# 	"Enter Operator : ",
# 	["+", "-", "x", "/", "^"]
# )
# result = 0
# if st.button("Calculate"):
# 	if operation == "+":
# 		result = num1 + num2
# 	elif operation == "-":
# 		result = num1 - num2
# 	elif operation == "x":
# 		result = num1 * num2
# 	elif operation == "/":
# 		result = num1 / num2
# 	elif operation == "^":
# 		result = num1 ** num2
# 	st.write(f"Result : {result}")

"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df
