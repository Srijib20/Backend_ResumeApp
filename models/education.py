from config import db

class Education(db.Model):
    __tablename__= 'education'
    #school_name,degree_name,Start_date,end_date
    id=db.Column(db.Integer,primary_key=True)
    school_name=db.Column(db.String(200),nullable=False)
    degree_name=db.Column(db.String(200),nullable=False)
    Start_date=db.Column(db.String(200),nullable=False)
    End_date=db.Column(db.String(200),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
