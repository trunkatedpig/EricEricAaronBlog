from flask import Flask,request,redirect,render_template,session
from postmarkup import render_bbcode
import sqlite3
app=Flask(__name__)
conn = sqlite3.connect("forum.db")
c = conn.cursor()
##q = "CREATE TABLE forumstuff(forumid integer, forumname text, author text)"
##result = c.execute(q)
##q = "CREATE TABLE poststuff(postid integer, post text)"
##result = c.execute(q)
##conn.commit();


@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("main.html")
    else:
        ##no idea if the form works. request.args does :^)
        button = request.form["b"]
        blog = request.form["blog"]
        title = request.form["title"]
        body = request.form["body"]
        return render_template("main.html")
@app.route("/forum", methods=["GET","POST"])
def forum():
    ##list all of the posts using the db
    forumTopic = request.args["topic"]
    return render_template("forum.html",topic=forumTopic)
@app.route("/post", methods=["GET","POST"])
def post():
    ##get strings from the database, read.
    ##parse it?
    ##return in string format and place into the comments
    ##be sure to include all <th>, <br> <tr>, etc.
    forumTopic = request.args["topic"]
    return render_template("post.html",topic=forumTopic)
    
if __name__=="__main__":
    app.debug=True
    app.run();
