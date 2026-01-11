# DocGenius-Revolutionizing-PDFs-with-AI

## Aboout the Project
This is a Python application that allows you to load a PDF and ask questions about it using natural language. The application uses a LLM to generate a response about your PDF. The LLM will not answer questions unrelated to the document. The application reads the PDF and splits the text into smaller chunks that can be then fed into a LLM. It uses OpenAI embeddings to create vector representations of the chunks. The application then finds the chunks that are semantically similar to the question that the user asked and feeds those chunks to the LLM to generate a response. Here is the Proof of Concept.

## Images of Proof of Concept

![logo](https://github.com/KalyanMurapaka45/DocGenius-Revolutionizing-PDFs-with-AI/blob/main/Outputs/Screenshot%202023-05-15%20212935.png)

![logo](https://github.com/KalyanMurapaka45/DocGenius-Revolutionizing-PDFs-with-AI/blob/main/Outputs/Screenshot%202023-05-15%20213027.png)

## Required Libraries

 - tiktoken
 - faiss-cpu
 - langchain
 - PyPDF2
 - python-dotenv
 - streamlit
 
#  Installation 

This is make you understand how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps.

1. Clone the repo

 ```
 git clone https://github.com/KalyanMurapaka45/DocGenius-Revolutionizing-PDFs-with-AI.git
 ```
 
 2. Install the required libraries

```
pip install -r requirements.txt
```

```You will also need to add your OpenAI API key to the .env file.```

3. To use the application, run the `app.py` file with the Streamlit CLI (after having installed the requirements):

```
# create & activate venv (Windows example)
python -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

## Using the Dashboard

The repository now includes a full Streamlit **DocGenius Dashboard** (implemented in `app.py`) that provides:

- Upload PDF files (saved to the `uploads/` folder)
- Select an uploaded PDF (optional) and ask natural-language prompts
- Responses from Google Gemini (when `GEMINI_API` is configured) or a mock response if not configured
- Accurate **timestamp** shown for each response
- Conversation **history** stored in `st.session_state` with a Download (JSON) button
- Upload management (list and delete files)
- Optional password protection via `DASHBOARD_PASSWORD` in `.env`

### Environment variables

Create a `.env` file in the project root with the following variables:

```
# Replace with your real Google Gemini API key to enable live LLM calls
GEMINI_API=your_gemini_api_key_here

# Optional: set a dashboard password for simple auth protection
DASHBOARD_PASSWORD=some_secret_password
```

If `GEMINI_API` is not set, the dashboard will still run and show mock replies and timestamps so you can test the UI.

### Running locally

1. Install dependencies (see earlier commands).
2. Run the dashboard locally:
```
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```
3. Open http://localhost:8501 in your browser and log in (if `DASHBOARD_PASSWORD` is set).

### Exposing the dashboard publicly (tunnel)

- Localtunnel (no account required):
```
# runs a temporary public URL that proxies to your local port
npx -y localtunnel --port 8501 --local-host 127.0.0.1 --print-requests
```
Note: localtunnel URLs are temporary and sometimes return transient 503 errors; re-run the command if the URL doesn't respond.

- ngrok (recommended for stability; requires an account + authtoken):
```
# install/configure once with your authtoken
npx -y ngrok authtoken <YOUR_AUTHTOKEN>

# then run the tunnel
npx -y ngrok http 127.0.0.1:8501
```

**Security note:** Tunneling your local app exposes it to the internet — use `DASHBOARD_PASSWORD` and do not place sensitive files in `uploads/` when the tunnel is public.

### Troubleshooting

- If the page is blank or 503: re-run the tunnel command; try local binding to `127.0.0.1` explicitly.
- If Gemini calls fail: verify `GEMINI_API` is set in `.env` and valid.
- If uploads can't be saved: ensure the `uploads/` folder exists (the dashboard creates it automatically) and the process has write permission.

---

# Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!. ```Don't forget to star the project if you find it useful!```

1. Fork the Project

2. Create your Feature Branch

3. Commit your Changes

4. Push to the Branch

5. Open a Pull Request

# Licnese

Distributed under the GNU General Public License v3.0. See ```LICENSE.txt``` for more information.

# Acknowledgements

We would like to express our gratitude to the open-source community for their invaluable inspiration and contributions. We also acknowledge the Python libraries used in this project and their respective contributors.
