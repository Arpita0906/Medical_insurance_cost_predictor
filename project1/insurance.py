from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np

model=pickle.load(open('Insurance.pkl','rb'))
ins=pd.read_csv("Insurance/insurance.csv")

#app=Flask(__name__)
app = Flask(__name__, template_folder='template') 
cors=CORS(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/services.html')

def servic():
    region=ins['region'].unique()
    
    return render_template('services.html',region=region)
@app.route('/contacts.html')
def contc():
    return render_template('contacts.html')
@app.route('/abc.html')
def abc():
    return render_template('abc.html')
@app.route('/action.html')
def act():
    return render_template('action.html')

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    if request.method=='POST':

        age=int(request.form.get('age'))
        bmi=float(request.form.get('bmi'))
        noc=int(request.form.get('noc'))
        smoker=int(request.form.get('smoker'))
        gender=int(request.form.get('gender'))
        region=request.form.get('origin')
        iregion=5
        if region == "southeast":
            iregion=0
        elif region == "southewest":
            iregion=1
        elif region == "northeast":
            iregion=2
        else:
            iregion=3
        #print(age,bmi,noc)
    prediction=model.predict(pd.DataFrame([[age,gender,bmi,noc,smoker,iregion]],columns=['age','sex','bmi','children','smoker','region']))
    #print(prediction)
    ans=[]
    ans.append(age)
    if gender == 0:
        ans.append("female")
    else:
        ans.append("male")
    ans.append(bmi)
    ans.append(noc)
    if smoker == 0:
        ans.append("yes")
    else:
        ans.append("no")
    #ans.append(gender)
    
    #ans.append(smoker)
    ans.append(region)
    ans.append(str(np.round(prediction[0],2)))
    return render_template('action.html',result=ans)

if __name__ == '__main__':
    app.run(debug=True)