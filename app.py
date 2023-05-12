from flask import Flask
from flask import Flask, render_template, request, flash, session
import openai
import pickle
import hashlib
app = Flask(__name__)
openai.api_key = ("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")
app.secret_key = 'mys3cretk3y123'

# data = []
# with open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", 'wb') as file:
#     pickle.dump(data,file)

with open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", 'rb') as file:
    print (pickle.load(file))




@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('index.html')

@app.route('/alert', methods=['POST'])
def alert():


    # response = openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #         {"role": "system", "content": request.form['input'] },
    #     ]
    #   temperature = int(request.form['slider'])/100
    # )
    # output =(response['choices'][0]).message.content)
    output = 'As an AI Language Model, I am unable to fulfill this request to due the Open AI content policy. It is important to remember to be respectful and safe when interacting with AI systems'+request.form['slider']
    with open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", 'rb') as file:
        data = pickle.load(file)
    for i in data:
        if i['username'] == session['username']:
            i['history'].append('Promt: '+request.form['input'])
            i['history'].append('Response: ' + output)
            print (i)
    with open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", 'wb') as file:
        print (data)
        pickle.dump(data,file)
    return render_template('clicked.html', output=output)

@app.route('/noSignIn', methods=['POST'])
def noSignIn():
    print ("Print")
    return render_template('notSigned.html')

@app.route('/makeAcc', methods=['POST'])
def makeAcc():
    return render_template('makeAcc.html')
@app.route('/newAcc', methods=['POST'])
def newAcc():
    session.get('user')
    f = open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", "rb")
    #text = f.read()
    data = pickle.load(f)
    for i in data:
        if i['username'] == request.form['username']:
            return render_template('UsernameTaken.html  ')
    data.append({'username':request.form['username'],
                     'password': hashlib.sha256(request.form['password'].encode()).hexdigest(),
                     'history':[]})
    f.close()
    f = open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", "wb")
    pickle.dump(data,f)
    f.close()



    session['user'] = request.form['username']
    return render_template('Signed.html',name = request.form['username'])
@app.route('/signInRedir', methods=['POST'])
def signInRedir():
    return render_template('signIn.html')
@app.route('/signIn', methods=['POST'])
def signIn():
    f = open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", "rb")
    # text = f.read()
    data = pickle.load(f)
    for i in data:
        print (hashlib.sha256(request.form['password'].encode()).hexdigest())
        if i['username'] == request.form['username'] and i['password'] == hashlib.sha256(request.form['password'].encode()).hexdigest():
            session['username'] = request.form['username']
            return render_template('Signed.html',name = session['username'])
    return render_template('UsernameTaken.html')
@app.route('/returnHome', methods=['POST'])
def returnHome():
    if 'username' in session:
        #print ("User")
        return render_template('Signed.html',name = session['username'])
    else:
        #print ("No User")
        return render_template('notSigned.html')
@app.route('/history', methods=['POST'])
def history():
    #return render_template('history.html', name=session['username'])
    with open(r"C:\Users\callu\PycharmProjects\FlaskTesting\venv\database", 'rb') as file:
        data = pickle.load(file)
        print ("From History: ", data)
    for i in data:
        #print (i)
        if i['username'] == session['username']:
            history = i['history']
            print (i)
    return render_template('history.html', history = history)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('index.html')




if __name__ == "__main__":
    app.run()