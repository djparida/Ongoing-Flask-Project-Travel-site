from flask import render_template, request, flash, redirect, jsonify, session
from main import app
from mongo import mongo


#it will sho you the home site
@app.route('/')
def home():
    return render_template('home.html')



#it will show the Signin/Signup Page
@app.route('/signin')
def signin():
    return render_template('login.html')

#for the login function
@app.route('/logdata', methods=['post'])
def logdata():
    _username = request.form['login']
    #Session has been used here
    session['usersession'] = request.form['login']
    _password = request.form['login_pass']
    myquery = {'username': _username, 'password': _password}
    select_users = mongo.db.users.find_one(myquery)
    if select_users == None:
        return "No Data"
    else:
        #print(select_users)
        #return "We will do that"
        if 'usersession' in session:
            usersession = session['usersession']
            return render_template('home.html', usersession=usersession)

#it will show the Signup page
@app.route('/login')
def formongo():
    return render_template('signin.html')

#user signup functionalities
@app.route('/signup', methods=['post'])
def signup():

    _username = request.form['username']
    print(_username)
    _email = request.form['email']
    _password = request.form['password']
    _password2 = request.form['password2']
    if _username and _email and _password and _password2 and request.method == 'POST':
        user_collection = mongo.db.users
        user_collection.insert({'username':_username, 'email': _email, 'password': _password,'confirm_password':_password2})
        flash('Added user successfuly')
        return redirect('/login')
    else:
        return "something going wrong"

#Forgot Password Code is here
@app.route('/forgotpassword')
def forgotpassword():
        if 'user' in session:
                session.pop('user', None)
                return render_template('forgotpassword.html')
        else:
                return render_template('forgotpassword.html')

#Password updated
@app.route('/changepwd', methods=['post'])
def changepwd():
        
        name = request.form['username']
        print(name)
        #session['name'] = request.form['username']
        #print(session)
        user = mongo.db.users.find_one({'username':name})
        #it will return the Username menu
        if user == None:
                Data = 'User Not Found'
                return render_template('forgotpassword.html', Data = Data)
        else:
                #it will return the forgot password zone
                for i in user:
                        session['user'] = user['password']
                        break
                print(user)
                print(session)
                Data2 = "Return me to Login Page"
                return render_template('forgotpassword.html', Data2 = Data2, name = name)

#password changed successfully
@app.route('/pcs', methods=['Post'])
def pcs():
        name = request.form['username']
        pwd = request.form['password']
        mongo.db.users.update_one({"username":name},{ "$set": {"password":pwd}})
        return redirect('/login')

        
#for user dashboard
@app.route('/dashboard')
def dashboard():     
        if 'usersession' in session:
                usersession = session['usersession']
                user = mongo.db.users.find_one({'username':usersession})
                return render_template('dashboard.html',user = user)

#edit profile successfully
@app.route('/eps',methods=['post'])
def eps():
        return redirect('/dashboard')


#user can edit Profile
@app.route('/editprofile')
def editprofile():
        if 'usersession' in session:
                usersession = session['usersession']
                user = mongo.db.users.find_one({'username':usersession})
                print(user['email'])
                return render_template('editprofile.html',user = user)

#user profile
@app.route('/profile',methods = ['post'])
def profile():
        if 'usersession' in session:
                        usersession = session['usersession']
                        user = mongo.db.users.find_one({'username':usersession})
                        email = user['email']
                        print(email)
                        fullname = request.form['name']
                        print(fullname)
                        image = request.form['image']
                        print(image)
                        #session['email'] = email  #session
                        mob = request.form['mob']
                        print(mob)
                        gender = request.form['x']
                        print(gender)
                        address = request.form['address']
                        print(address)
                        try:
                                dataa = mongo.db.userinfo.find_one({'email':email})
                                mongo.db.userinfo.update_one({'email':email},{'$set':{'name':fullname,'mob':mob,'gender':gender,'address':address,'image':image}})
                                print("data Updated")
                        except:
                                mongo.db.userinfo.insert_one({'name':fullname,'email':email,'mob':mob,'gender':gender,'address':address,'image':image})
                                print("data inserted")

                        user_info = mongo.db.userinfo.find_one({'email':email})
                        #Aggregate function has been used
                        pipeline = [
                        {
                                '$lookup': {
                                'from': 'userinfo',
                                'localField': 'email',
                                'foreignField': 'email',
                                'as': 'Matches'
                                }
                        }
                        ]

                        rel = mongo.db.users.aggregate(pipeline)

                        for i in rel:
                                while i['email'] == email:
                                        print(i['Matches'])
                                        for data in i['Matches']:
                                                return render_template('profile.html',data = data )
                                        break
                                break
                        
                         #       print(i)
                        #return "going well"
                        
        else:
                return "something wrong yaar"

#it will show you the user
@app.route('/listusers')
def list_users():
    user = mongo.db.users.find()
    return render_template('show.html', user = user)

#The Logout portion
@app.route('/logout')
def logout():
    if 'usersession' in session:
        session.pop('usersession',None)
        #return 'we are going good!'
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
