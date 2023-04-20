from flask import Flask,jsonify,request
from flask_cors import CORS
from config import db,SECRET_KEY
from config import load_dotenv
from flask import Flask,request,jsonify
from uuid import uuid1,uuid4
import os,json,pytz
from datetime import date,datetime
import pandas as pd

from models.user import User
from models.personalDetails import PersonalDetails
from models.projects import Projects
from models.experiences import Experiences
from models.education import Education
from models.certificate import Certificate
from models.skills import Skills
from os import environ
def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]= environ.get("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
    app.config["SQLALCHEMY_ECHO"]=False
    app.secret_key=SECRET_KEY
    db.init_app(app)
    print("DB Initialized Successfully")
    with app.app_context():
        # db.drop_all()
        '''
        use 
        Create an endpoint
            - Sign up user
            - add personal details
            - add experience details
            - add project details
            - add education details
            - add certificate details
            - add skills details
        '''
        @app.route('/sign_up',methods=['POST'])
        def sign_up():
            data=request.form.to_dict(flat=True)
            new_user=User(
                username=data["username"]
            )
            db.session.add(new_user)
            db.session.commit()
            return "User added successfully"

        @app.route("/add_personal_details",methods=['POST'])
        def add_personal_details():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            '''
            {
                "name": "",
                "email":"",
                "phone":"",
                "address":"",
                "linked_in":"",
            }
            '''
            personal_details=request.get_json()
            new_personal_details=PersonalDetails(
                name=personal_details["name"],
                email=personal_details["email"],
                phone=personal_details["phone"],
                address=personal_details["address"],
                linkedin_link=personal_details["linkedin_link"],
                user_id=user.id
            )
            db.session.add(new_personal_details)
            db.session.commit()
            return "Personal Details"


        @app.route("/add_experience",methods=['POST'])
        def add_experience():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            experience_data=request.get_json()
            for data in experience_data["data"]:
                new_experience=experience_data(
                    company_name=data["company_name"],
                    role=data["role"],
                    role_desc=data["role_desc"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    user_id=user.id
                )
                db.session.add(new_experience)
                db.session.commit()
                return "Experience added"

        @app.route("/add_education_details",methods=['POST'])
        def add_education_details():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            education_data=request.get_json()
            for education in education_data["data"]:
                new_education=education_data(
                    id=education["id"],
                    school_name=education["school_name"],
                    degree_name=education["degree_name"],
                    start_date=education["start_date"],
                    end_date=education["end_date"],
                    user_id=user.id
                )
                db.session.add(new_education)
                db.session.commit()
                return "Education details added"
        @app.route("/add_projects",methods=['POST'])
        def add_projects():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            project_data=request.get_json()
            for project in project_data["data"]:
                new_projects= Projects(
                    name=project["name"],
                    desc=project["description"],
                    start_date=project["start_date"],
                    end_date=project["end_date"],
                    user_id=user.id
            )
                db.session.add(new_projects)
                db.session.commit()
                return "Project added"
        @app.route("/add_certificate_details",methods=['POST'])
        def add_certificate_details():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            personal_details=request.get_json()
        @app.route("/add_skills_details",methods=['POST'])
        def add_skills_details():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            personal_details=request.get_json()
        db.create_all()
        db.session.commit()
        @app.route('/get_resume',methods=['GET'])
        def get_resume():
            username=request.args.get('username')
            user=User.query.filter_by(username=username).first()
            Personal_details=PersonalDetails.query.filter_by(user_id=user.id).all()
            experiences=Experiences.query.filter_by(user_id=user.id).first()
            #educations=Education.query.filter_by(user_id=user.id).all()
            projects=Projects.query.filter_by(user_id=user.id).all()
            #certificates=Certificate.query.filter_by(user_id=user.id).all()
            #skills=Skills.query.filter_by(user_id=user.id).all()
            experiences_data=[]
            education_data=[]
            projects_data=[]
            certificates_data=[]
            skills_data=[]
            resume_data={
                "name":Personal_details.name,
                "email":Personal_details.email,
                "phone":Personal_details.phone,
                "address":Personal_details.address,
                "linkedin_link":Personal_details.linkedin_link
            }
            # add experience
            for exp in experiences:
                experiences_data.append({
                    "company_name":exp.company_name,
                    "role":exp.role,
                    "role_desc":exp.role_desc,
                    "start_date":exp.start_date,
                    "end_date":exp.end_date
                })
            resume_data["experiences"]=experiences_data
            # add projects
            for proj in projects:
                projects_data.append({
                    "name": proj.name,
                    "desc":proj.name,
                    "start_date":proj.start_date,
                    "end_date":proj.end_date
                })
                resume_data["projects"]=projects_data
                return "Resume data"


        return app
if __name__=="__main__":
    app=create_app()
    app.run(host='0.0.0.0',port="5000",debug=True)