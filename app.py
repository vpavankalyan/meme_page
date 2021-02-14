from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    caption =  db.Column(db.Text,nullable=False)
    image_link = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Post('{self.username}','{self.caption}','{self.image_link}')"
    
class PostSchema(ma.Schema):
    class Meta:
        fields = ("id","username","caption","image_link")
        model = Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@app.route('/memes',methods=['POST'])
def post_memes():
    name2 = request.json['username']
    caption2 = request.json['caption']
    image_url2 = request.json['image_link']
    print(name2)
    print(caption2)
    post1 = Post(username=name2,caption=caption2,image_link=image_url2)
    db.session.add(post1)
    db.session.commit()

    return jsonify(post_schema(post1))

@app.route('/memes',methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)

@app.route('/memes/<id>',methods=['GET'])
def get_post(id):
    post_needed = Post.query.get(id)
    result = post_schema.dump(post_needed)
    return jsonify(result)


@app.route("/",methods=['GET','POST'])
def home():
    posts = Post.query.all()
    posts.reverse()
    return render_template('home.html',posts=posts)


@app.route("/add",methods=['POST'])
def add():
    name1 = request.form['name']
    print(name1)
    caption1 = request.form['caption']
    image_url1 = request.form['url']
    new_post=Post(username=name1,caption=caption1,image_link=image_url1)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/')

# @app.route("/update")
# def updat
