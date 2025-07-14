import os
import datetime
import pymysql

pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request
from peewee import *
from dotenv import load_dotenv
from playhouse.shortcuts import model_to_dict


load_dotenv()

# Initialize database connection BEFORE model definition
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


mydb.connect()
mydb.create_tables([TimelinePost])


# Flask app factory
def create_app():
    app = Flask(__name__)

    experiences = [
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
            "date": "May 2024 - September 2024",
            "description": [
                "Worked on frontend and data-layer development building a user-focused digital portal to replace paper forms; reduced nurse data entry time by 70%",
                "Engineered 50+ dynamic intake and assessment workflows in Next.js with reusable React components, collaborating with UI/UX designers to refine form layouts and streamline user flows",
                "Implemented PostgreSQL data layer using Prisma ORM models, enabling efficient CRUD operations for robust patient record management.",
            ],
        },
        {
            "title": "Member",
            "company": "Association for Computing Machinery",
            "date": "Since Fall 2022",
            "description": ["Workshops, hackathons, and mentorships"],
        },
    ]

    education = [
        {
            "school": "University of Texas at Dallas",
            "degree": "B.S. in Computer Science",
            "image": "img/utd.jpg",
        }
    ]

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
        "Education": "education_view",
        "Hobbies": "hobbies_view",
        "Map": "map_view",
        "Timeline": "timeline"
    }

    @app.route("/")
    def index():
        return render_template(
            "index.html", title="Affiq's Portfolio", menu_items=menu_items
        )

    @app.route("/about")
    def about():
        about_text = (
            "Hi, I'm Affiq, a CS student at the University of Texas at Dallas. "
            "I enjoy coding, playing guitar, and exploring new places."
        )
        return render_template(
            "about.html", title="About Me", about_text=about_text, menu_items=menu_items
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

    @app.route("/education")
    def education_view():
        return render_template(
            "education.html",
            title="Education",
            education=education,
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
        return render_template(
            'timeline.html', title="Timeline", menu_items=menu_items
        )

    @app.route("/api/timeline_post", methods=["POST"])
    def post_time_line_post():
        name = request.form["name"]
        email = request.form["email"]
        content = request.form["content"]
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
