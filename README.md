# Getting Started with Calendify

Calendify is a Python-based project that simplifies the process of creating calendar events from email invites and other snippets of text. Before you can run the project, you'll need to set up the necessary credentials from the Google Cloud Console and install the required dependencies.

## Step 1: Google Cloud Console Setup

1. **Create a Project:**
   Go to the [Google Cloud Console](https://console.cloud.google.com/), sign in with your Google account, and create a new project.

2. **Enable the Google Calendar API:**
   In the Google Cloud Console, navigate to the "APIs & Services" > "Dashboard" page. Click on "Enable APIs and Services," search for "Google Calendar API," and enable it for your project.

3. **Create OAuth 2.0 Client ID:**
   In the Google Cloud Console, navigate to "APIs & Services" > "Credentials." Click on "Create Credentials," then select "OAuth client ID." Choose "Desktop App" as the application type, and give it a name (e.g., "Calendify OAuth Client"). Once created, download the `credentials.json` file.

## Step 2: Set Up Your Environment

1. **Python Environment:**
   Make sure you have Python 3 installed on your system.

2. **Virtual Environment (Optional but Recommended):**
   To create a virtual environment, you can use `venv`. Run the following commands to set up and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate

3. **Install Dependencies:**
   To install the required Python packages, use `pip`:

   ```bash
   pip install -r requirements.txt

## Step 3: Run the Project

1. **Add Credentials:**
   Place the `credentials.json` file you downloaded from the Google Cloud Console in the root directory of the project.

2. **Run the Main Script:**
   Run the main script to start the Calendify application:

   ```bash
   python main.py
   ```
   
   The application will prompt you for your Google account credentials for the first-time setup. Follow the instructions to authenticate your account.

3. **Sample Event:**
   After successful setup, the application will create sample calendar events based on the provided test data. Modify the `main.py` file to customize and add your own events programmatically.

