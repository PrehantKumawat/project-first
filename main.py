import streamlit as st
st.title("Calculator")
num1 = st.number_input("Enter number 1 : ")
num2 = st.number_input("Enter number 2 : ")
operation = st.selectbox(
	"Enter Operator : ",
	["+", "-", "x", "/"]
)
result = 0
if st.button("Calculate"):
	if operation == "+":
		result = num1 + num2
	elif operation == "-":
		result = num1 - num2
	elif operation == "x":
		result = num1 * num2
	elif operation == "/":
		result = num1 / num2
	st.write(f"Result : {result}")
