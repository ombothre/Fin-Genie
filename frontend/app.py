import streamlit as st
import requests

st.title("Financial AI Agent")

# File Upload
uploaded_file = st.file_uploader("Upload your financial data (CSV)", type=['csv'])

if uploaded_file:
    # Upload file to the backend
    response = requests.post(
        "http://127.0.0.1:5000/upload",
        files={"file": ("data.csv", uploaded_file.getvalue())},  # Pass file content
    )

    if response.ok:
        st.success("File uploaded successfully!")
    else:
        st.error("File not uploaded!")
        st.json(response.json())  # Display error response if any

    # User Query
    query = st.text_input("Enter your query:")
    if query and st.button("Submit"):
        # Send query to the backend in JSON format
        response_query = requests.post(
            "http://127.0.0.1:5000/process",
            json={"query": query},  # Send JSON body with query
        )
        if response_query.ok:
            st.success("Query processed successfully!")
            response_data = response_query.json()
            st.write("Response:")
            st.write(response_data.get("response", "No valid response received."))
        else:
            st.error("Failed to process query!")
            st.json(response_query.json())  # Display backend error details

