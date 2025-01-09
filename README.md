## FinGenie - AI Agent with CSV/Excel Integration  

This project implements an AI agent using **LangChain** and **Streamlit** that takes in a CSV/Excel file, processes it to extract schema and data, and allows users to query it in natural language. The AI agent generates Python code to answer the query, executes it, and displays the result.

### Key Features:  
- **File Upload:** Users can upload CSV files containing structured data.  
- **AI Code Generation:** The agent generates Python code tailored to the query and executes it.  
- **Results Display:** Output is formatted and presented in a user-friendly manner.  
- **Streamlit Frontend:** A simple and intuitive UI for file uploads and querying.  

---

## Setup Instructions  

### Envoirment File

Create a `.env` file with

```bash
GOOGLE_API_KEY = ""
```

### Backend  

1. Navigate to the `backend` directory:  
   ```bash
   cd backend
   ```  

2. Install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

3. Start the backend server using **Waitress**:  
   ```bash
   waitress-serve --host localhost --port 5000 app:app
   ```  

---

### Frontend  

1. Navigate to the `frontend` directory:  
   ```bash
   cd frontend
   ```  

2. Start the Streamlit application:  
   ```bash
   streamlit run app.py
   ```  

The application will be accessible at `http://localhost:8501`.  