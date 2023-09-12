from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(length=10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if name == '':
            raise ValueError("All authors must have name.")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError("Phone numbers must be 10 digits.")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, value):
        if value == '':
            raise ValueError('Title cannot be left blank')
        
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        for word in clickbait:
            if word in value:
                return value
        raise ValueError('Not clickbait-y enough.')
    
    @validates('content')
    def validate_content(self, key, words):
        if len(words) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return words
        
    @validates('summary')
    def validate_summary(self, key, words):
        if len(words) >= 250:
            raise ValueError("Summary can only be up to 250 characters.")
        return words
    
    @validates('category')
    def validate_category(self, key, value):
        valid_categories = ['Fiction', 'Non-Fiction']
        if value not in valid_categories:
            raise ValueError('Must be fiction or non-fiction.')
        return value
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
