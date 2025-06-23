import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for

def create_app():
    app = Flask(__name__)

    # Updated Experiences Data
    experiences = [
        {
            "title": "Software Track Lead",
            "company": "Theta Tau",
            "date": "January 2025 - Present",
            "description": [
                "Currently developing cross-platform health monitoring app using React Native, integrating Firebase for real-time data sync and secure cloud storage",
                "Building analytics dashboards to process heart rate, activity, and sleep metrics, turning raw data into insights"
            ]
        },
        {
            "title": "Software Engineer Intern",
            "company": "Texas A&M Health Science Center",
            "date": "May 2024 - September 2024",
            "description": [
                "Worked on frontend and data-layer development building a user-focused digital portal to replace paper forms; reduced nurse data entry time by 70%",
                "Engineered 50+ dynamic intake and assessment workflows in Next.js with reusable React components, collaborating with UI/UX designers to refine form layouts and streamline user flows",
                "Implemented PostgreSQL data layer using Prisma ORM models, enabling efficient CRUD operations for robust patient record management."
            ]
        },
        {
            "title": "Member",
            "company": "Association for Computing Machinery",
            "date": "Since Fall 2022",
            "description": [
                "Workshops, hackathons, and mentorships"
            ]
        }
    ]

    education = [
        {"school": "University of Texas at Dallas", "degree": "B.S. in Computer Science", "image": "img/utd.jpg"}
    ]

    hobbies = [
        {"name": "Guitar", "image": "img/guitar.jpg"},
        {"name": "Drawing", "image": "img/drawing.jpg"},
        {"name": "Space", "image": "img/space.jpg"}
    ]

    menu_items = {
        "Home": "index",
        "About": "about",
        "Experience": "experience",
        "Education": "education_view",
        "Hobbies": "hobbies_view",
        "Map": "map_view"
    }

    @app.route("/")
    def index():
        return render_template("index.html", title="Affiq's Portfolio", menu_items=menu_items)

    @app.route("/about")
    def about():
        about_text = (
            "Hello, I'm Affiq, a Computer Science student at the University of Texas at Dallas. "
            "I enjoy coding, playing guitar, and exploring new places."
        )
        return render_template("about.html", title="About Me", about_text=about_text, menu_items=menu_items)

    @app.route("/experience")
    def experience():
        # Passing 'experiences' (plural) to the template
        return render_template("experience.html", title="Experience", experiences=experiences, menu_items=menu_items)

    @app.route("/education")
    def education_view():
        return render_template("education.html", title="Education", education=education, menu_items=menu_items)

    @app.route("/hobbies")
    def hobbies_view():
        return render_template("hobbies.html", title="Hobbies", hobbies=hobbies, menu_items=menu_items)

    @app.route("/map")
    def map_view():
        return render_template("map.html", title="Places I've Visited", menu_items=menu_items)

    return app