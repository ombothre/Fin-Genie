import streamlit as st
import requests

st.title("Financial AI Agent")

# File Upload
uploaded_file = st.file_uploader("Upload your financial data (CSV)", type=['csv'])

if uploaded_file:
    # Upload file to the backend
    try:
        response = requests.post(
            "http://127.0.0.1:5000/upload",
            files={"file": ("data.csv", uploaded_file.getvalue())},  # Pass file content
        )
        if response.ok:
            st.success("File uploaded successfully!")
        else:
            st.error("File upload failed!")
            st.json(response.json())
    except Exception as upload_error:
        st.error(f"Error uploading file: {str(upload_error)}")

# User Query
query = st.text_input("Enter your query:")
if query and st.button("Submit"):
    # Send query to the backend
    try:
        response_query = requests.post(
            "http://127.0.0.1:5000/process",
            json={"query": query},  # Send JSON body with query
        )
        if response_query.ok:
            response_data = response_query.json()
            st.success("Query processed successfully!")
            st.write("Response:")
            st.text(response_data.get("response", "No valid response received."))
        else:
            st.error("Query processing failed!")
            st.json(response_query.json()) 
    except Exception as query_error:
        st.error(f"Error submitting query: {str(query_error)}")
