import numpy as np
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, render_template
import pickle

# create an app object using the Flask class
app = Flask(__name__)

# load the trained model
model = pickle.load(open('models/rf_model.pkl', 'rb'))

# define the route to be home
# use the route decorator to tell Flask what URL should trigger our function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def home2():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def detectRobot():
    return render_template('contact.html')

@app.route('/contact.html', methods=['GET','POST'])
def predict():
    if request.method== 'POST':
        f1=request.form['0_time_diff_counts']
        f2=request.form['total_biddings']
        f3=request.form['max_bids_per_auction']
        f4=request.form['uniqueDevices']
        f5=request.form['uniqueCountry']
        f6=request.form['uniqueURL']
        f7=request.form['uniqueip']

        features_input = [float(f1),float(f2),float(f1)/float(f2),float(f3),float(f4)/float(f2),float(f5)/float(f2), float(f5), float(f6)/float(f2), float(f7)/float(f2)]
        features = [np.array(features_input)]
        prediction = model.predict(features) # features must be like [[11,2,..]]

        output = prediction[0]
        if output == 0:
            re = 'human'
        else:
            re = 'robot'

    if re == 'human':
        return render_template('contact.html', prediction_result = "Congratulation! This bidder is a {}. Keep this customer!".format(re))

    if re == 'robot':
        return render_template('contact.html', prediction_result = "Warning! This bidder is a {}. Delete it!".format(re))


if __name__ == "__main__":
    app.run(debug = True, host = "127.0.0.1", port = 5000)
