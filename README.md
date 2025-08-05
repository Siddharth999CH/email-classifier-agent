Email Classifier and Responder
This is a Python-based AI agent that uses the Gmail API to check for new emails, classifies them using OpenAI's language models, and can draft appropriate responses. The agent is designed to help you quickly triage and manage your inbox.

Features
Email Retrieval: Fetches unread emails from a specified Gmail account.

AI Classification: Classifies each email into categories like "Urgent," "Follow-up," or "Spam" using OpenAI's gpt-3.5-turbo model.

Draft Response Generation: Automatically drafts a professional and context-aware response for urgent and follow-up emails.

Secure API Handling: Utilizes a .env file to securely manage API keys and credentials, ensuring they are never exposed in the repository.

Prerequisites
To run this project, you will need:

Python 3.7+ installed on your system.

A Git client to clone the repository.

An OpenAI API Key from the OpenAI Platform.

Google Cloud credentials for the Gmail API.

Setup Instructions
Follow these steps to get the project running on your local machine.

1. Clone the Repository
Clone this repository to your local machine:

git clone https://github.com/Siddharth999CH/email-classifier-agent.git
cd email-classifier-agent

2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage your dependencies.

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

On Windows:

python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install the required Python libraries using the requirements.txt file:

pip install -r requirements.txt

4. Configure Your API Keys
You must create a .env file to store your API keys. This file is ignored by Git and will not be pushed to GitHub.

Create a file named .env in the root of your project and add the following lines, replacing the placeholder text with your actual key:

OPENAI_API_KEY=your_openai_api_key_here
GMAIL_CREDENTIALS_FILE=credentials.json

5. Set Up Google Cloud Credentials
Follow the steps below to obtain your credentials.json file. This file must be saved in the project's root directory, but it is already added to .gitignore for security.

Go to the Google Cloud Console and create a new project.

Enable the Gmail API under "APIs & Services".

Go to the OAuth consent screen and configure your app (make sure to set your email as a test user).

Navigate to Credentials, click Create Credentials, and choose OAuth client ID.

Select "Desktop app" and click CREATE.

Click DOWNLOAD JSON and save the file as credentials.json in your project's root folder.

6. First Run and Authentication
The first time you run the script, it will handle the authentication process with the Gmail API.

python agent.py

A browser window will open, prompting you to log in to your Google Account and grant the necessary permissions. After you complete this, the script will save an access token to a new file named token.json. This file is also ignored by Git for your security.

Usage
After the initial setup and authentication, you can run the script at any time to process your unread emails.

python agent.py

The script will print the classification and a drafted response for each email. The code to actually send the replies and mark emails as read is currently commented out for safety. You can uncomment those lines in agent.py once you are confident with the agent's behavior.

Project File Structure
email-classifier-agent/
├── .env                  # Stores your API keys (ignored by Git)
├── .gitignore            # Specifies which files to ignore (like keys and tokens)
├── agent.py              # The main script with all the agent's logic
├── README.md             # This file
├── requirements.txt      # Lists the Python libraries needed
├── credentials.json      # Google Cloud credentials (ignored by Git)
└── token.json            # Gmail API access token (created on first run, ignored by Git)
