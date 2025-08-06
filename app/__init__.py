import os
import datetime
import pymysql

pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request
from peewee import *
from dotenv import load_dotenv
from playhouse.shortcuts import model_to_dict


load_dotenv()

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


def initialize_db():
    if mydb.is_closed():
        mydb.connect()
    mydb.create_tables([TimelinePost])


# Flask app factory
def create_app():
    app = Flask(__name__)
    with mydb:
        mydb.create_tables([TimelinePost])
    experiences = [
        {
            "title": "Software Developer Intern",
            "company": "UTDesign Studio",
            "location": "Richardson, TX",
            "date": "June 2025 - Present",
            "description": [
                "Developed internal real-time event calendar application, enabling dynamic scheduling, event tracking, and live updates using Vue.js, Nuxt.js, and Prisma ORM",
                "Built and maintained RESTful API endpoints with Node.js, Express, and Prisma, handling event CRUD operations, user sessions, and notifications",
                "Implemented secure email verification system with token-based authentication for account security",
            ],
        },
        {
            "title": "Software Track Lead",
            "company": "Theta Tau",
            "date": "January 2025 - Present",
            "description": [
                "Currently developing cross-platform health monitoring app using React Native, integrating Firebase for real-time data sync and secure cloud storage",
                "Building analytics dashboards to process heart rate, activity, and sleep metrics, turning raw data into insights",
            ],
        },
        {
            "title": "Software Engineer Intern",
            "company": "Texas A&M Health Science Center",
            "location": "College Station, TX",
            "date": "May 2024 - August 2024",
            "description": [
                "Developed a digital intake portal with frontend forms and backend data layer integration, reducing manual data entry by up to 50%",
                "Designed and developed 20+ dynamic intake and assessment workflows in Next.js with reusable React components, refining form layouts and streamlining user flows",
                "Implemented PostgreSQL data layer using Prisma ORM models, enabling efficient CRUD operations for robust record management",
            ],
        },
        {
            "title": "Member",
            "company": "Association for Computing Machinery",
            "date": "Since Fall 2022",
            "description": ["Workshops, hackathons, and mentorships"],
        },
    ]


    projects = [
        {
            "title": "Expense Tracker",
            "technologies": "React, Next.js, Tesseract.js, Multer (for file uploads)",
            "description": [
                "Built a full-stack expense tracker that lets users upload receipt images, automatically extracts totals and dates via OCR, and provides an organized, searchable history with category filters."
            ],
            "github": "https://github.com/affiq23/expense-tracker",
        },
        {
            "title": "Kvault",
            "technologies": "Next.js, Typescript, React, Supabase, Commander.js",
            "description": [
              "Version-controlled note-taking system with a unified command line and web interface for managing markdown notes with authentication and local snapshot tracking."
            ],
            "github": "https://github.com/affiq23/kvault",
            "demo": "https://kvault.vercel.app/"
        },
        {
            "title": "Stem4Stems",
            "technologies": "React, Three.js, OpenAI API",
            "description": [
               "Developed a browser-based learning tool that uses engaging visuals and AI-powered quizzes to help younger students grasp STEM concepts through interactivity."
            ],
            "github": "https://github.com/affiq23/stem4stems",
            "demo": "https://stem4stems.vercel.app/"
        },
        {
            "title": "ML Classifier",
            "technologies": "Python, Google Colab, numpys, scikit-learn",
            "description": [
             "Built reliable text classification models that handle a range of natural language processing tasks with ease and flexibility."
            ],
            "github": "https://github.com/affiq23/text_classification_project",
        },
    ]

    education = [
        {
            "school": "University of Texas at Dallas",
            "degree": "Bachelor of Science in Computer Science",
            "date": "Expected Spring 2026",
            "location": "Richardson, TX",
            "image": "img/utd.jpg",
        }
    ]

    skills = {
        "Programming Languages": [
            {"name": "Java", "icon": "☕"},
            {"name": "Swift", "icon": "🍎"},
            {"name": "JavaScript", "icon": "📜"},
            {"name": "TypeScript", "icon": "🔷"},
            {"name": "Python", "icon": "🐍"},
            {"name": "C++", "icon": "⚙️"},
        ],
        "Frameworks & Libraries": [
            {"name": "React.js", "icon": "⚛️"},
            {"name": "Next.js", "icon": "▲"},
            {"name": "Tailwind", "icon": "💨"},
            {"name": "Node.js", "icon": "🟢"},
            {"name": "Flask", "icon": "🌶️"},
            {"name": "Express", "icon": "🚄"},
            {"name": "LangChain", "icon": "🔗"},
        ],
        "Tools & Technologies": [
            {"name": "GitHub", "icon": "🐙"},
            {"name": "MongoDB", "icon": "🍃"},
            {"name": "Supabase", "icon": "⚡"},
            {"name": "PostgreSQL", "icon": "🐘"},
            {"name": "Docker", "icon": "🐳"},
            {"name": "Prisma", "icon": "🔺"},
        ],
    }

    hobbies = [
        {
            "name": "Guitar",
            "image": "img/guitar.jpg",
            "description": "I've been playing guitar for almost 5 years now, and I enjoy playing songs from bands like Blink 182, Arctic Monkeys, and The 1975. I play both acoustic and electric, but playing acoustic songs have recently become my new favorite!",
        },
        {
            "name": "Drawing",
            "image": "img/drawing.jpg",
            "description": "I like sketching out cartoons and comics as a way to pass the time. I also enjoy drawing nature and landscapes (although I'm not very good at it!)",
        },
        {
            "name": "Space",
            "image": "img/space.jpg",
            "description": "I've always been interested in space and learning about all the cool things in our universe we don't understand. I like watching videos and reading books on topics such as black holes, supernovas, and the possibility of alien life.",
        },
    ]

    menu_items = {
        "Home": "index",
        "About": "about",
        "Experience": "experience",
        "Projects": "projects_view",
        "Hobbies": "hobbies_view",
        "Map": "map_view",
        "Timeline": "timeline",
    }

    @app.route("/")
    def index():
        return render_template(
            "index.html", title="Affiq's Portfolio", menu_items=menu_items
        )

    @app.route("/about")
    def about():
        about_text = (
            "Hi! I'm currently a junior studying computer science at UT Dallas. I've worked hands "
            "on in the fields of web and mobile app development, and am currently exploring fields "
            "such as artificial intelligence and cloud computing."
        )
        return render_template(
            "about.html",
            title="About Me",
            about_text=about_text,
            education=education,
            skills=skills,
            menu_items=menu_items,
        )

    @app.route("/experience")
    def experience():
        # Passing 'experiences' (plural) to the template
        return render_template(
            "experience.html",
            title="Experience",
            experiences=experiences,
            menu_items=menu_items,
        )

    @app.route("/projects")
    def projects_view():
        return render_template(
            "projects.html",
            title="Projects",
            projects=projects,
            menu_items=menu_items,
        )

    @app.route("/hobbies")
    def hobbies_view():
        return render_template(
            "hobbies.html", title="Hobbies", hobbies=hobbies, menu_items=menu_items
        )

    @app.route("/map")
    def map_view():
        return render_template(
            "map.html", title="Places I've Visited", menu_items=menu_items
        )

    @app.route("/timeline")
    def timeline():
        return render_template("timeline.html", title="Timeline", menu_items=menu_items)

    @app.route("/api/timeline_post", methods=["POST"])
    def post_time_line_post():
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        content = request.form.get("content", "").strip()

        if not name:
            return "Invalid name", 400
        if "@" not in email or not email:
            return "Invalid email", 400
        if not content:
            return "Invalid content", 400

        timeline_post = TimelinePost.create(name=name, email=email, content=content)

        return model_to_dict(timeline_post)

    @app.route("/api/timeline_post", methods=["GET"])
    def get_time_line_post():
        return {
            "timeline_posts": [
                model_to_dict(p)
                for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
            ]
        }

    @app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
    def delete_timeline_post(post_id):
        post = TimelinePost.get_or_none(TimelinePost.id == post_id)
        if post is None:
            return {"error": "Post not found"}, 404
        post.delete_instance()
        return {"message": f"Post {post_id} deleted successfully"}

    return app


if __name__ == "__main__":
    initialize_db()
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
