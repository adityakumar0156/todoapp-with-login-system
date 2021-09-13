from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # creating the Flask class object
app.secret_key="hello"

'''
mysql server k case me sabkuch same rahega bas niche wala line me 
jo last me string hai usme modification hojaiga
'''
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///info.db"  #sqlite k case me last wala name table se match krna hoga yani jitna table utna bar ye likhna padega
#app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///database/users_list/info1.db" #ye ek alag table k liywee hai

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class info(db.Model):#class ka naam table k naam se match krna chahiye
    sno = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"{self.email}--{self.password}"
@app.route('/')
def home():
    if 'name' in session:
        print("session with 'name' is present'")
    else:
        print("going to set session")
        return render_template("add_sessions.html")
    data=info.query.all()
    data.reverse()
    c = request.cookies.get('name')
    s=session['name']
    return render_template("index.html", data=data,ss=0,t=5,c=c,s=s)

@app.route('/welcome',methods=['POST','GET'])
def welcome(): #set cookies
    if request.method=='POST':
        x = request.form.get('cookie')
        y = request.form.get('type')
        res = make_response(redirect('/'))
        res.set_cookie(y,x)
        return res

    return render_template("welcome.html")

@app.route('/dcookie',methods=['POST','GET'])
def dcookie():  #delete cookie(name)
    if request.method=='POST':
        x = request.form.get('type')
        res = make_response(redirect('/'))
        res.delete_cookie(x)
        return res
    return render_template('dcookie.html')

@app.route('/add_sessions',methods=['POST','GET'])
def add_sesions():  #add sessions
    if request.method=='POST':
        x = request.form.get('session')
        y = request.form.get('type')
        res = make_response(redirect('/'))
        session[y]=x
        return res
    return render_template("add_sessions.html")

@app.route('/delete_sessions',methods=['POST','GET'])
def delete_sessions():
    if request.method=='POST':
        x = request.form.get('type')
        res = make_response(redirect('/'))
        session.pop(x,None)
        return res
    return render_template('delete_sessions.html')


@app.route('/go',methods=['POST'])
def go():
   if 'name' in session:
        print("session with 'name' is present'")
   else:
        print("going to set session")
        return render_template("add_sessions.html")
   try:
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        entry=info(password=password,email=email)
        db.session.add(entry)
        db.session.commit()
   except:
    print("Error occured in /go")
   return redirect("/")

@app.route('/delete/<int:i>/<int:ss>/<int:t>')
def delete(i,ss,t):
   if 'name' in session:
        print("session with 'name' is present'")
   else:
        print("going to set session")
        return render_template("add_sessions.html")
   try:
    data=info.query.filter_by(sno=i).first()
    db.session.delete(data)
    db.session.commit()
    data = info.query.all()
   except:
    print("Error occured in /delete")
   data = info.query.all()
   data.reverse()
   c = request.cookies.get('name')
   s = session['name']
   return render_template("index.html", data=data, ss=ss, t=t,c=c,s=s)


@app.route('/update/<int:i>/<int:ss>/<int:t>',methods=['POST','GET'])
def update(i,ss,t):
   if 'name' in session:
        print("session with 'name' is present'")
   else:
        print("going to set session")
        return render_template("add_sessions.html")
   try:
    if request.method=="POST":
        email=request.form.get('email')
        password = request.form.get('password')
        data = info.query.filter_by(sno=i).first()
        data.email=email
        data.password=password
        db.session.add(data)
        db.session.commit()
        data = info.query.all()
        data.reverse()
        c = request.cookies.get('name')
        s=session['name']
        return render_template("index.html", data=data, s=s, t=t,c=c,ss=ss)
        #return redirect('/')
    data=info.query.filter_by(sno=i).first()
   except:
    print("Error occured in /update")
   c = request.cookies.get('name')
   s=session['name']
   return render_template('update.html',data=data,s=s,t=t,c=c,ss=ss)

@app.route('/page/<int:s>/<int:t>/<int:u>')
def page(ss,t,u):
    if 'name' in session:
        print("session with 'name' is present'")
    else:
        print("going to set session")
        return render_template("add_sessions.html")
    if u==1:
        ss=ss+5
        t=t+5
    if u==0:
        ss=ss-5
        t=t-5
    data=info.query.all()
    data.reverse()
    c = request.cookies.get('name')
    s=session['name']
    return render_template("index.html", data=data,ss=ss,t=t,c=c,s=s)

if __name__ == '__main__':
    app.run(debug=True)