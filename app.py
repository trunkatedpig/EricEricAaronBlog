from flask import Flask,request,redirect,render_template,session
from postmarkup import render_bbcode
import sqlite3, csv
app=Flask(__name__)

conn = sqlite3.connect("posts.db")
c = conn.cursor()
q = "CREATE TABLE IF NOT EXISTS posts(postid integer primary key autoincrement, post text, title text, author text, forumname text)"
c.execute(q)
q = "CREATE TABLE IF NOT EXISTS comments(postid integer,commentid integer, comment text, author text)"
c.execute(q)
conn.commit()


@app.route("/", methods=["GET","POST"])
@app.route("/home", methods=["GET","POST"])
def index():
    return render_template("main.html");

@app.route("/forums", methods=["GET","POST"])
def forums():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    q = "CREATE TABLE IF NOT EXISTS posts(postid integer primary key autoincrement, post text, title text, author text, forumname text)"
    c.execute(q)
    q = "CREATE TABLE IF NOT EXISTS comments(postid integer,commentid integer, comment text, author text)"
    c.execute(q)
    conn.commit()
    q = "select distinct posts.forumname from posts"
    tmp =c.execute(q)
    conn.commit()
    topics = []
    for r in tmp:
        topics.append(r)
    print topics
    return render_template("forums.html", topics = topics)

@app.route("/create", methods=["GET","POST"])
def create():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    q = "CREATE TABLE IF NOT EXISTS posts(postid integer primary key autoincrement, post text, title text, author text, forumname text)"
    c.execute(q)
    q = "CREATE TABLE IF NOT EXISTS comments(postid integer,commentid integer, comment text, author text)"
    c.execute(q)
    conn.commit()
    if request.method=="POST":
        ##no idea if the form works. request.args does :^)
        button = request.form["b"]
        blog = request.form["blog"]
        title = request.form["title"]
        author = request.form["author"]
        body = request.form["body"]
        if (blog!="" and title!="" and author!="" and body!="") :
            print "success"
            conn = sqlite3.connect("posts.db")
            c = conn.cursor()
            q = '''insert into posts values(NULL,"'''+body+'''","'''+title+'''","'''+author+'''","'''+blog+'''")'''
            c.execute(q)
            q = "select * from posts"
            result = c.execute(q)
            conn.commit()
            for r in result:
                print r
    return render_template("create.html")

@app.route("/table", methods=["GET","POST"])
def table():
    return render_template("bbcode.html");

@app.route("/forum", methods=["GET","POST"])
def forum():
    #ud, unified dict
    ud = dict(request.form.items() + request.args.items())
    posts = []
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    if request.method=="POST" and "b" in ud:
        forumTopic = ud["topic"]
        if ud["body"]!="" and ud["title"]!="" and ud["username"]!="":
            blog = ud["topic"]
            author = ud["username"]
            title = ud["title"]
            body = request.form["body"]        
            q = '''insert into posts values(NULL,"'''+body+'''","'''+title+'''","'''+author+'''","'''+blog+'''")'''
            c.execute(q)
            conn.commit()
    q = "select postid, post, title, author from posts where forumname='"+ud["topic"]+"'"
    result = c.execute(q)
    conn.commit()
    for r in result:
        posts.append(r)
    print posts
    topic = ud["topic"]

    return render_template("forum.html",topic=topic,posts=reversed(posts))

@app.route("/post", methods=["GET","POST"])
def post():
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    ##universal dict to easen the coding
    ud = dict(request.args.items() +
                         request.form.items())
    q = "select author,title,post from posts where postid='"+ud["postID"]+"'"
    result=c.execute(q)
    op = "" ##op = original poster in interwebz talk
    title=""
    for r in result:
        op = "<td width='15%'>"+r[0]+"</td><td width='85%'>"+render_bbcode(r[2]).replace("\n","<br>")+"</td>"
        title=r[1]
    comments = []
    print request.method +"!!!!!!!!!!!!!!!\n\n\n"
    q = "select postid,commentid, comment, author from comments where postid='"+ud["postID"]+"'"
    result = c.execute(q)
    conn.commit()      
    for r in result:
        comments.append(r)
    print comments
    topic = ud["topic"]
    postid = ud["postID"]
    commentid=0 ##the current number of comments
    ##prepare the html string
    q = "select Count(*) from comments where postid='"+ud["postID"]+"'"
    commentid = c.execute(q)
    ##this just takes the first and only item.
    for i in commentid:
        commentid=i[0]

    if ("comment" in request.form):
        body = ud["body"]
        print "BODY: "+body
        author = ud["username"]
        if (author!="" and body!=""):
            q = '''insert into comments values("'''+postid+'''","'''+ str(commentid) +'''","'''+body+'''","'''+author+'''")'''
            c.execute(q)
            conn.commit()
            commentid+=1
    tablestr=""
    i=0
    while (i<commentid):
        q = "select comment, author from comments where postid='"+ud["postID"]+"' and commentid='"+str(i)+"'"
        result=c.execute(q)
        for item in result:
            tablestr=tablestr+"<tr><td>"+item[1]+"</td><td>"+render_bbcode(item[0]).replace("\n","<br>")+"</td><tr>"
        i+=1

    return render_template("post.html",comments=tablestr,topic=topic,postid=postid,op=op,title=title)
     
if __name__=="__main__":
    app.debug=True
    app.run();
