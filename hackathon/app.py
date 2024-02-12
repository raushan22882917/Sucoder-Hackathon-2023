# app.py
from flask import Flask, request, session, redirect, url_for, render_template, flash,redirect, url_for,g,jsonify
import psycopg2  # pip install psycopg2
import psycopg2.extras
import re
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import sql
from googlesearch import search
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from newsapi.newsapi_client import NewsApiClient 
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "22882288"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route("/")
def home():
    # Check if user is loggedin
    if "loggedin" in session:
        # User is loggedin show them the home page
        return render_template("home.html", username=session["username"])
    # User is not loggedin redirect to login page
    return redirect(url_for("login"))

@app.route("/home/profile")
def profiles():
    # Check if user is loggedin
    if "loggedin" in session:
        # User is loggedin show them the home page
        return render_template("profile.html", username=session["username"])
    # User is not loggedin redirect to login page
    return redirect(url_for("profile"))    


@app.route("/index")
def about():
    # Check if user is loggedin
    if "loggedin" in session:
        # User is loggedin show them the home page
        return render_template("about.html", username=session["username"])
    # User is not loggedin redirect to login page
    return redirect(url_for("index"))


    return redirect(url_for("login"))




def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    feedback = request.form.get('feedback')

    # Insert feedback into the database
    conn = psycopg2.connect(
        host="localhost",
        dbname="sampledb",
        user="postgres",
        password="22882288"
    )
    cur = conn.cursor()
    cur.execute(
        sql.SQL("INSERT INTO feedbacks (name, email, feedback) VALUES ({}, {}, {})")
        .format(sql.Literal(name), sql.Literal(email), sql.Literal(feedback))
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('login'))

@app.route("/about", methods=["GET", "POST"])
def hackathon():
    # Check if user is logged in
    if "loggedin" in session:
        if request.method == "POST":
            # User submitted the feedback form
            name = request.form["name"]
            email = request.form["email"]
            feedback_text = request.form["feedback"]
            insert_feedback(name, email, feedback_text)
            return render_template(
                "/contest/hackathon_home.html", username=session["username"]
            )

        # User is logged in, show them the home page
        return render_template(
            "/contest/hackathon_home.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))




@app.route("/daily")
def daily():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/contest/daily.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login")) 


@app.route("/weekly")
def weekly():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/contest/weekly.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))       
@app.route("/learning")
def learning():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "learn.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login")) 

@app.route("/workshop")
def workshop():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/workshop/workshop_front.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login")) 

@app.route("/uploaded_blog")
def uploadedblog():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/blog/blog_template.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login")) 

@app.route("/python_exercise")
def python():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/question/python.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login")) 



@app.route("/workshops")
def workshops():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/workshop/workshop.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))   



@app.route("/project")
def project():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/workshop/project.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))     



@app.route("/carrier")
def carrier():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/workshop/carrier.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))  


@app.route("/exercise")
def exercise():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "exercise.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))  



    



@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    success_message = None

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_text = request.form['message']

        # Store the message in the database
        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message_text)
        )
        conn.commit()

        success_message = f'Thank you, {name}! Your message has been sent successfully.'

    return render_template('/workshop/contact.html', success_message=success_message)           



       


@app.route("/hackathon")
def blog():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "blog.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login")) 

    


@app.route("/hackathons")
def hackathons():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "/contest/hackathon.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))  


@app.route("/practice")
def practice():
    # Check if user is logged in
    if "loggedin" in session:
        # User is logged in, show them the home page
        return render_template(
            "practice.html", username=session["username"]
        )

    # User is not logged in, redirect to the login page
    return redirect(url_for("login"))      



       



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    success_message = None

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_text = request.form['message']

        # Store the message in the database
        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message_text)
        )
        conn.commit()

        success_message = f'Thank you, {name}! Your message has been sent successfully.'

    return render_template('contact.html', success_message=success_message)



@app.route('/registration', methods=['POST'])
def registration():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        team_lead_name = request.form['name']
        team_members = request.form['team_members']
        email = request.form['email']
        college_name = request.form['college_name']

        # Store the form data in the PostgreSQL database
        cursor.execute(
            "INSERT INTO registrations (team_lead_name, team_members, email, college_name) VALUES (%s, %s, %s, %s)",
            (team_lead_name, team_members, email, college_name)
        )
        conn.commit()

        success_message = f'Thank you, {team_lead_name}! Your registration has been successfully saved.'
        return render_template('index.html', success_message=success_message)

    return render_template('index.html')  


@app.route("/login/", methods=["GET", "POST"])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username" and "password" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        print(password)

        # Check if account exists using MySQL
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            password_rs = account["password"]
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session["loggedin"] = True
                session["id"] = account["id"]
                session["username"] = account["username"]
                # Redirect to home page
                return redirect(url_for("home"))
            else:
                # Account doesnt exist or username/password incorrect
                flash("Incorrect username/password")
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        # Create variables for easy access
        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        _hashed_password = generate_password_hash(password)

        # Check if account exists using MySQL
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address!")
        elif not re.match(r"[A-Za-z0-9]+", username):
            flash("Username must contain only characters and numbers!")
        elif not username or not password or not email:
            flash("Please fill out the form!")
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute(
                "INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)",
                (fullname, username, _hashed_password, email),
            )
            conn.commit()
            flash("You have successfully registered!")
    elif request.method == "POST":
        # Form is empty... (no POST data)
        flash("Please fill out the form!")
    # Show registration form with message (if any)
    return render_template("register.html")


@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    # Redirect to login page
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if user is loggedin
    if "loggedin" in session:
        cursor.execute("SELECT * FROM users WHERE id = %s", [session["id"]])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template("profile.html", account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for("login"))














db_connection = {
    'host': 'localhost',
    'database': 'sampledb',
    'user': 'postgres',
    'password': '22882288'
}

# Function to initialize the database
def initialize_database():
    connection = psycopg2.connect(**db_connection)
    cursor = connection.cursor()

    # Create a table to store quiz results if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            score INT
        );
    ''')

    connection.commit()
    connection.close()

# Initialize the database on application startup
initialize_database()

# Load quiz questions from JSON file
questions_path = os.path.join(app.root_path, 'static', 'questions.json')

# Load quiz questions from JSON file
with open(questions_path) as f:
    questions = json.load(f)


# Quiz route
@app.route('/quiz/index')
def quiz():
    return render_template('index.html', questions=questions)

# Results route
@app.route('/quiz/index/results', methods=['POST'])
def results():
    name = request.form['name']
    email = request.form['email']
    score = 0

    for question in questions:
        user_answer = request.form.get(str(question['id']))
        if user_answer and user_answer == question['answer']:
            score += 1

    # Store quiz results in the database
    connection = psycopg2.connect(**db_connection)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO quiz_results (name, email, score)
        VALUES (%s, %s, %s);
    ''', (name, email, score))
    connection.commit()
    connection.close()

    return redirect(url_for('quiz'))



@app.route('/quizs')
def quizs():
    return render_template('quiz_front.html')    


@app.route('/python/intro_quiz')
def pythons():
    return render_template('/Quiz/python.html')      


@app.route('/titanic')
def titanic():
    return render_template('/project/titanic.html')   



@app.route('/material')
def blogmaterial():
    return render_template('/blog/blog.html')   





@app.route('/intro_exercise')
def intro():
    return render_template('/material/python/intro.html')     


@app.route('/editor')
def codeeditor():
    return render_template('editor.html') 

@app.route("/")
def blogs():
    # Fetch blogs from the database
    conn = psycopg2.connect(
        dbname="sampledb",
        user="postgres",
        password="22882288",
        host="localhost",
        port="5432",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blogs")
    blogs = cursor.fetchall()
    conn.close()
    return render_template("/blog/blog.html", blogs=blogs)

    


@app.route("/submit", methods=["POST"])
def submit():
    # Retrieve form data
    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]

    # Save blog to the database
    conn = psycopg2.connect(
        dbname="sampledb",
        user="postgres",
        password="22882288",
        host="localhost",
        port="5432",
    )
    cursor = conn.cursor()
    insert_query = sql.SQL(
        "INSERT INTO blogs (name, email, content) VALUES ({}, {}, {})"
    ).format(sql.Literal(name), sql.Literal(email), sql.Literal(content))
    cursor.execute(insert_query)
    conn.commit()
    conn.close()
    return redirect(url_for("blog"))





# About page
@app.route('/about')
def abouts():
    return render_template('/blog/about.html')

 




@app.route('/contact', methods=['GET', 'POST'])
def cont():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Insert data into the 'contacts' table
        query = """
            INSERT INTO contacts (name, email, subject, message)
            VALUES (%s, %s, %s, %s);
        """
        params = (name, email, subject, message)

        execute_query(query, params)

        return redirect(url_for('home'))

    return render_template('/blog/contact.html')


@app.route('/python/learning')
def pythonmaterial():
    return render_template('/material/python.html')   



@app.route('/ask')
def homebot():
    return render_template('dout.html')

# Define the route to handle the chatbot functionality
@app.route('/ask/doubt', methods=['POST'])
def ask():
    # Get the user's question from the form
    user_question = request.form['question']

    # Use Google Search API to get search results
    search_results = list(search(user_question, num=5, stop=5, pause=2))

    # Pass the results to the HTML template
    return render_template('dout.html', question=user_question, results=search_results)








def headlines_api():
    API_KEY = "fd8a9fe21ec848d2b5fab1e3703a536a"
    api_url = "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=" + API_KEY
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data['articles']
    else:
        return None

def get_user_reaction(article_title):
    return session.get(article_title, {'likes': 0, 'dislikes': 0})

def set_user_reaction(article_title, reaction_type):
    user_reaction = get_user_reaction(article_title)
    if reaction_type == 'likes':
        user_reaction['likes'] += 1
        user_reaction['dislikes'] = max(0, user_reaction['dislikes'] - 1)  # Reset dislikes
    elif reaction_type == 'dislikes':
        user_reaction['dislikes'] += 1
        user_reaction['likes'] = max(0, user_reaction['likes'] - 1)  # Reset likes
    session[article_title] = user_reaction

@app.route('/news')
def news():
    news_headlines = headlines_api()
    return render_template('news.html', headlines=news_headlines, get_user_reaction=get_user_reaction)

@app.route('/like/<title>')
def like(title):
    set_user_reaction(title, 'likes')
    return update_reaction(title, 'likes')

@app.route('/dislike/<title>')
def dislike(title):
    set_user_reaction(title, 'dislikes')
    return update_reaction(title, 'dislikes')

def update_reaction(title, reaction_type):
    user_reaction = get_user_reaction(title)
    return f'{reaction_type.capitalize()}: {user_reaction[reaction_type]}'


@app.route('/question')
def easyquestion():
    return render_template('question.html')    



@app.route('/compiler')
def compiler_data():
    return render_template('editor.html')    

@app.route('/editprofile')
def edit():
    return render_template('prof.html')     





   













db_connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="22882288",
    database="sampledb"
)
cursor = db_connection.cursor()

@app.route('/quiz')
def question():
    return render_template('/create/index.html')

@app.route('/quizplateform')
def quizes():
    return render_template('/create/quiz.html')

@app.route('/add-question', methods=['POST'])
def add_question():
    try:
        data = request.get_json()
        question_text = data['questionText']
        option1 = data['option1']
        option2 = data['option2']
        option3 = data['option3']
        option4 = data['option4']
        correct_option = data['correctOption']

        # Insert question into the database
        cursor.execute("""
            INSERT INTO quiz_questions (question_text, option1, option2, option3, option4, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (question_text, option1, option2, option3, option4, correct_option))

        db_connection.commit()

        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False})

@app.route('/getquestions')
def get_questions():
    try:
        # Fetch all quiz questions from the database
        cursor.execute("SELECT * FROM quiz_questions;")
        questions = cursor.fetchall()

        # Convert the result to a list of dictionaries
        questions_list = [{
            'question_text': q[1],
            'option1': q[2],
            'option2': q[3],
            'option3': q[4],
            'option4': q[5],
            'correct_option': q[6]
        } for q in questions]

        return jsonify(questions_list)
    except Exception as e:
        print(e)
        return jsonify([])

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    try:
        data = request.get_json()
        user_answers = data['answers']

        # Fetch correct answers from the database
        cursor.execute("SELECT id, correct_option FROM quiz_questions;")
        correct_answers = dict(cursor.fetchall())

        # Calculate user's score
        marks = 0
        for answer in user_answers:
            question_id = int(answer['question'].replace('q', ''))
            user_answer = answer['answer']
            correct_answer = correct_answers.get(question_id)

            if correct_answer and user_answer == correct_answer:
                marks += 1

        # Insert user's result into the database
        cursor.execute("""
            INSERT INTO quizresultshack (user_name, marks)
            VALUES (%s, %s);
        """, ('User', marks))

        db_connection.commit()

        return jsonify({'success': True, 'marks': marks})
    except Exception as e:
        print(e)
        return jsonify({'success': False})




UPLOAD_FOLDER = 'R:/hackathon/login_register/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Database configuration
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'sampledb'
DB_USER = 'postgres'
DB_PASSWORD = '22882288'

# Function to connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the registration form
@app.route('/registrationforquiz', methods=['GET', 'POST'])
def registrationdata():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        email = request.form['email']
        opportunity_type = request.form['opportunityType']
        institute_name = request.form['instituteName']

        # Upload image
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        # Store data in the database
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users_data (username, email, opportunity_type, institute_name, image)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, opportunity_type, institute_name, filename))

            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('question'))

    return render_template('/create/register.html')

# Route to display the entered data
@app.route('/display_data')
def display_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users_data
        """)

        data = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

    return render_template('/create/display_data.html', data=data)











# with open('data.json', 'r') as file:
#     companies_data = json.load(file)

@app.route('/company')
def company():
    return render_template('/indeed/company.html')

@app.route('/review')
def review():
    # Get the company name from the query parameter
    company_name = request.args.get('company')

    # Search for the company details
    company_details = None
    for company in companies_data:
        if company['company_name'].lower() == company_name.lower():
            company_details = company
            break

    if company_details:
        return render_template('/indeed/reviews.html', company_details=company_details)
    else:
        return redirect(url_for('company'))










@app.route('/interview')
def interview():
    return render_template('/interview/interview.html')

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'sampledb'
DB_USER = 'postgres'
DB_PASSWORD = '22882288'

# Database connection function
def connect_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

# Initialize the database with a table for interview experiences
def init_db():
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interview_experiences (
                    id SERIAL PRIMARY KEY,
                    user_name VARCHAR(255) NOT NULL,
                    company_name VARCHAR(255) NOT NULL,
                    interview_experience TEXT NOT NULL
                );
            """)
            conn.commit()

# Route for the registration form
@app.route('/shareexperiance')
def registration_form():
    return render_template('/interview/registration.html')


@app.route('/interview/onetoone')
def one():
    return render_template('/interview/one.html')

# Route for submitting the form
@app.route('/submitform', methods=['POST'])
def submit_form():
    user_name = request.form.get('userName')
    company_name = request.form.get('companyName')
    interview_experience = request.form.get('interviewExperience')

    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO interview_experiences (user_name, company_name, interview_experience)
                VALUES (%s, %s, %s);
            """, (user_name, company_name, interview_experience))
            conn.commit()

    return redirect(url_for('display_interviews'))

# Route for displaying all interview experiences
@app.route('/display')
def display_interviews():
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM interview_experiences;")
            interviews = cursor.fetchall()

    return render_template('/interview/display.html', interviews=interviews)

@app.route('/practices')
def coding():
    return render_template('/interview/practice.html')


db_config = {
    'host': 'localhost',
    'dbname': 'sampledb',
    'user': 'postgres',
    'password': '22882288'
}

# Function to create a connection to the database
def create_connection():
    connection = psycopg2.connect(**db_config)
    return connection

# Function to create a table if it does not exist
def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    # Creating a 'questions' table
    create_questions_table_query = '''
    CREATE TABLE IF NOT EXISTS questions (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        field VARCHAR(50) NOT NULL,
        question TEXT NOT NULL
    );
    '''
    cursor.execute(create_questions_table_query)

    # Creating an 'answers' table
    create_answers_table_query = '''
    CREATE TABLE IF NOT EXISTS answers (
        id SERIAL PRIMARY KEY,
        answer TEXT NOT NULL
    );
    '''
    cursor.execute(create_answers_table_query)

    connection.commit()
    cursor.close()
    connection.close()

# Create the table on startup
create_table()

# Route for the main page
@app.route('/response')
def response():
    # Fetch questions from the 'questions' table
    connection = create_connection()
    cursor = connection.cursor()

    select_questions_query = 'SELECT * FROM questions;'
    cursor.execute(select_questions_query)
    questions = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('response.html', questions=questions)

# Route for adding a new question
@app.route('/add_question', methods=['POST'])
def add_questions():
    name = request.form['name']
    email = request.form['email']
    field = request.form['field']
    question_text = request.form['question']

    # Insert the new question into the 'questions' table
    connection = create_connection()
    cursor = connection.cursor()

    insert_question_query = 'INSERT INTO questions (name, email, field, question) VALUES (%s, %s, %s, %s) RETURNING id;'
    cursor.execute(insert_question_query, (name, email, field, question_text))
    question_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('response'))

# Route for the 'doubt' page
@app.route('/doubt')
def doubt():
    # Fetch answers from the 'answers' table
    connection = create_connection()
    cursor = connection.cursor()

    select_answers_query = 'SELECT * FROM answers;'
    cursor.execute(select_answers_query)
    answers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('doubt.html', answers=answers)

# Route for sharing an answer
@app.route('/share_answer', methods=['POST'])
def share_answer():
    shared_answer = request.form['shared_answer']

    # Insert the shared answer into the 'answers' table
    connection = create_connection()
    cursor = connection.cursor()

    insert_answer_query = 'INSERT INTO answers (answer) VALUES (%s) RETURNING id;'
    cursor.execute(insert_answer_query, (shared_answer,))
    answer_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('doubt'))
# Route for fetching shared answers
@app.route('/get_shared_answers')
def get_shared_answers():
    connection = create_connection()
    cursor = connection.cursor()

    select_answers_query = 'SELECT * FROM answers;'
    cursor.execute(select_answers_query)
    rows = cursor.fetchall()

    answers = [clean(row[1], tags=[], attributes={}, styles=[]) for row in rows]

    cursor.close()
    connection.close()

    return {'answers': answers} 


@app.route('/update-photo', methods=['POST'])
def update_photo():
    user_id = request.form.get('user_id')
    file = request.files.get('file')

    # Save the file to the server (you can customize this part)
    file_path = f'static/uploads/{user_id}_{file.filename}'
    file.save(file_path)

    # Update the database with the new file path (you should customize this part)
    # Replace the following lines with your database update logic
    new_photo_url = f'/static/uploads/{user_id}_{file.filename}'
    # update_database(user_id, new_photo_url)

    return jsonify({'success': True, 'new_photo_url': new_photo_url})     




CSV_FILE = 'hackathon/users.csv'

@app.route('/chatbot')
def indexchatbot():
    fields = get_unique_fields()
    return render_template('index_chatbot.html', fields=fields)

@app.route('/submitemail', methods=['POST'])
def submitemail():
    user_question = request.form['question']
    selected_field = request.form['field']

    email_addresses = get_email_addresses_for_field(selected_field)

    if email_addresses:
        for email in email_addresses:
            send_email("New Question", user_question, email)
        message = "Question sent to all emails in the selected field."
    else:
        message = "No email addresses found for the selected field. Question not sent."

    return render_template('result_chatbot.html', message=message)

def get_unique_fields():
    fields = set()
    with open(CSV_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fields.add(row['field'])
    return list(fields)

def get_email_addresses_for_field(selected_field):
    email_addresses = []
    with open(CSV_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['field'] == selected_field:
                email_addresses.append(row['email'])
    return email_addresses

def send_email(subject, message, to_email):
    # Email configuration
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'raushan22882917@gmail.com'
    SMTP_PASSWORD = 'yescbxrbadtamkem'
    SENDER_EMAIL = 'raushan22882917@gmail.com'

    # Create the MIME message
    mime_message = MIMEMultipart()
    mime_message['From'] = SENDER_EMAIL
    mime_message['To'] = to_email
    mime_message['Subject'] = subject

    # Attach the text message
    text_part = MIMEText(message, 'plain')
    mime_message.attach(text_part)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)

            # Send the email
            server.sendmail(SENDER_EMAIL, to_email, mime_message.as_string())

        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
     
if __name__ == "__main__":
    app.run(debug=True)
