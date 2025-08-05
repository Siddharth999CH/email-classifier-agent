📧 Email Classifier & Responder Agent
A smart Python agent that uses the power of AI to automatically triage your emails, classify them, and draft intelligent responses. Spend less time in your inbox and more time on what matters!

✨ Features
Intelligent Classification: Uses OpenAI's gpt-3.5-turbo to categorize emails as Urgent, Follow-up, or Spam.

Context-Aware Drafting: Generates professional and polite draft replies based on the email's content and its classification.

Gmail API Integration: Seamlessly connects to your Gmail inbox to fetch new messages and handle responses.

Secure & Private: Handles all API keys and sensitive credentials safely in a .env file, ensuring they are never exposed in your public repository.

🚀 Getting Started
Follow these steps to set up and run the agent on your local machine.

Prerequisites
Python 3.7+

Git

An OpenAI API Key

Google Cloud Account with the Gmail API enabled.

⚙️ Setup Instructions
1. Clone the Repository

Clone this project to your computer and navigate into the directory.

git clone https://github.com/Siddharth999CH/email-classifier-agent.git
cd email-classifier-agent

2. Create & Activate a Virtual Environment

This isolates the project dependencies from your global Python environment.

On Windows:

python -m venv venv
.\venv\Scripts\activate

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install Python Packages

Install all the required libraries from the requirements.txt file.

pip install -r requirements.txt

🔑 API Configuration
1. Create a .env file

This file holds your secret keys and is automatically ignored by Git. Create a new file named .env in your project's root folder and add the following lines, replacing the placeholder with your actual key:

OPENAI_API_KEY=your_openai_api_key_here
GMAIL_CREDENTIALS_FILE=credentials.json

2. Get Google Cloud Credentials

Go to the Google Cloud Console and create a new project.

Enable the Gmail API.

Go to the OAuth consent screen and configure your app, making sure to add your email as a test user.

Under Credentials, create a new OAuth client ID of type "Desktop app."

Download the credentials.json file and place it in your project's root directory.

🔒 Security Note: Both credentials.json and the generated token.json are already listed in the .gitignore file and will not be committed to GitHub.

🏃 Usage
1. Initial Run & Authentication

The very first time you run the script, a browser window will open to securely authenticate with your Gmail account.

python agent.py

After granting permissions, an access token will be saved to a file named token.json so you won't need to authenticate again.

2. Processing Emails

The agent will then fetch your unread emails, classify them, and print the results to the console. The code to actually send replies and mark emails as read is initially commented out for your safety.

You can uncomment the send_reply and modify lines in agent.py once you are ready to automate these actions.

📂 Project Structure
email-classifier-agent/
├── .env                  # Your secret API keys (ignored by Git)
├── .gitignore            # Tells Git which files to ignore
├── agent.py              # The core logic of the email agent
├── requirements.txt      # List of all Python dependencies
├── credentials.json      # Google Cloud credentials (ignored by Git)
└── token.json            # Generated access token (created on first run, ignored by Git)
