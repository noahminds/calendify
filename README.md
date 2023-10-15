# About Calendify
Calendify is a Python-based, AI powered event management tool that simplifies the process of creating calendar events from email invites and other snippets of text. User interaction is currently supported through a simple command-line interface, with plans to further develop the application into a chrome extension to facilitate a more user-friendly experience in the future.

# Demo
https://github.com/noahminds/calendify/assets/125851385/db2075e7-59ca-4073-9348-f5a8609b12ec

# Getting Started with Calendify
Before you can run the project, you'll need to follow these steps:

## Step 1: Install Project Dependencies

1. **Python Environment:**
   Make sure you have Python 3.10.7 or higher installed on your system.

2. **Virtual Environment (Optional but Recommended):**
   To create a virtual environment, you can use `venv`. Run the following commands to set up and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate

3. **Install Python Packages:**
   To install the required Python packages, use `pip`:

   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openai

## Step 2: Set up Google Calendar API Credentials
To use the Google Calendar API, you need to set up credentials. You can follow [Google's quickstart guide](https://developers.google.com/calendar/api/quickstart/python) which details how to create credentials for your application. After creating the credentials, save the JSON file as credentials.json in your project directory.

## Step 3: Set Up OpenAI API Credentials
To use the OpenAI API, you need to set up credentials. To do so login to [OpenAI's API Keys page](https://platform.openai.com/account/api-keys) and create a new secret key.

To securely store your OpenAI GPT-3.5 Turbo API key, set an environment variable on your system. You can do this by adding the following line to your shell profile (e.g., .bashrc or .zshrc) with your API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Don't forget to restart your terminal or reload your shell configuration for the changes to take effect.

## Step 4: Run the Project
Now you're ready to run your project. Open a terminal, navigate to your project directory, and run the following command:

```bash
python main.py
```
   
The application will prompt you for your Google account credentials for the first-time setup. Follow the instructions to authenticate your account.

## Step 5: Using the Project
Your project provides an interactive command-line interface for event management. Follow the prompts to create, edit, and submit events to your Google Calendar.

* To create an event, provide an event description and follow the prompts.
* To edit event details, type 'edit' when prompted.
* To submit the event to your calendar, type 'done' when prompted.

## Additional Notes
* The project is set up to handle natural language event descriptions and provides assistance using the GPT-3.5 Turbo model to interpret and format the event details.
* Be cautious about the token limit when providing lengthy event descriptions, as it could impact the GPT-3.5 Turbo response.

## Support and Issues
If you encounter any issues or have questions about this project, feel free to reach out to the [project owner](mailto:riyals_welders0z@icloud.com) for support.

## Disclaimer
Please be aware of any privacy and security considerations when using external services like Google Calendar and OpenAI's GPT-3.5 Turbo model. Review the respective privacy policies and terms of use to ensure compliance with their rules and regulations.

