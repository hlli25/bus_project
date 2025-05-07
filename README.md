## System description

This system is intended to support students of the University of Birmingham with their wellbeing.
It includes a chatbot, trend report, and review feature which will be summarised further down.
It is intended to be used by three main user types: Student, Admin, Counsellor; each of whom have varying access to the
different functionalities.


## How to run the project in an IDE (e.g. PyCharm/ VS Code)

### Prerequisites

* **Python 3.11** (or higher)
* A Google Gemini API key – get one at [https://ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key) (you must be signed in with a Google account).

1. **Clone and enter the repo**
```bash
git clone https://github.com/hlli25/bus_project.git
cd bus_project
```

2. **Create & activate a virtual environment in your IDE**

3. **Install appropriate libraries**
The main libraries which may need to be installed are:
python-dotenv ([PyPI](https://pypi.org/project/python-dotenv/) / [Anaconda](https://anaconda.org/conda-forge/python-dotenv))
google-genai ([PyPI](https://pypi.org/project/google-genai/) / [Anaconda](https://anaconda.org/conda-forge/google-genai))
flask ([PyPI](https://pypi.org/project/Flask/) / [Anaconda](https://anaconda.org/conda-forge/flask))
flask-login ([PyPI](https://pypi.org/project/Flask-Login/) / [Anaconda](https://anaconda.org/conda-forge/flask-login))
flask-sqlalchemy ([PyPI](https://pypi.org/project/Flask-SQLAlchemy/) / [Anaconda](https://anaconda.org/conda-forge/flask-sqlalchemy))
flask-wtf ([PyPI](https://pypi.org/project/Flask-WTF/) / [Anaconda](https://anaconda.org/conda-forge/flask-wtf))

4. **Set up a run configuration with module: 'flask'.**

5. **Configure your Google Gemini API key**
* **Create `.env` from the template `.env.example`**
Run the following command:
```bash
# Linux/macOS
cp .env.example .env

# Windows PowerShell
copy .env.example .env
```

* **Open `.env` and paste your key**
```bash
GEMINI_API_KEY=YOUR‑OWN‑API‑KEY‑GOES‑HERE
```

6.  The test data is already within the SQL database. If for any reason it does not work, repopulate the database by running the reset_db() function in a flask shell via the terminal, or by executing it directly from debug_utils.py.

---

## Run the app

**PyCharm**
1. *Run/Debug Configurations ▸ + ▸ Python*
2. Change the *script* drop-down box to show *module*; enter `flask` in the text box beside it
3. **Script parameters**: enter `run`

**VS Code**
Open workspace → *Run ▸ Run Without Debugging* (launch configuration included).

**CLI**
```bash
flask run
```

Access [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

Once the web app has been opened, please login using the login details below (also listed in the home page of the app):

| Role       | Username      | Password      |
| ---------- | ------------- | ------------- |
| Admin      | `admin1`      | `admin1.pw`   |
| Counsellor | `counsellor1` | `counsel1.pw` |
| Student    | `student1`    | `student1.pw` |

---

## List of programming languages, frameworks, tools

Python - the main programming language used to create this project
Flask - web application framework used to handle sessions, user authentication and integrate with WTforms
Bootstrap - front-end CSS framework used to create aesthetically pleasing UI features
SQLAlchemy - an Object Relational Mapper used to interact with the SQL database using Python classes
Google Gemini API - used to integrate Google's generative AI model into the app

---

## Summary of implemented functionalities

Login / Register - simple login and register features which utilise the `User` SQLAlchemy model, which has attributes id, username, password, role. Access to certain pages, and the contents of the navbar are dependent on if a user is logged in, and what their role is.

Chatbot - integrated with Google Gemini API. Provides a signposting service to different parts of the web app due to the customised responses provided in `chatbot.py`. Future functionality would include direct booking functionality through the chatbot, and direct completion of the CORE34 form through the chatbot

Reviews - allows users to provide reviews for each functionality, both via a 1-5 star rating, and an optional text review. Admins can view all reviews in a centralised "Manage reviews" page, as well as delete any reviews which may be inappropriate or malicious. If a User is deleted, their reviews still stay due to the cascade option used in `models.py`, ensuring that feedback is not lost.

Trend report - analyses data from user input from Review and chatbot conversation to summarise user engagement and feedback of the app. Future functionality will include analysing data from the `Review` SQLAlchemy model and `Conversation` SQLAlchemy model, more detailed analysis, splitting feedback by feature, and producing graphs based on user-inputted parameters.

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contributions

Tanveer Haider - 2181796 (35%): Web app template (base, home, placeholder pages), login/register function, adding/managing reviews, decorators, `User` and `Review` models, adding in parameters to Chatbot to give customised responses, README.md file, created video demo

James Jackson - 2839180 (10%): updates to trend report feature

Carrick Kennedy - 2837588 (10%): initial trend report feature

Ho Lam Li - 2879279 (35%): developing Chatbot UI feature, adding in `Models` for `Conversation`, `Message`, `Resource`, `CounsellingSession`, `Ticket`, destination pages for Chatbot signposting such as "Resources", adding pytest test cases, created video demo

Jalal Zulfiqar - 2724243 (10%): initial Chatbot UI development
