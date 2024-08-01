from flask import Flask, render_template, request,redirect, url_for, session
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
app = Flask(__name__, template_folder='templates')

app.secret_key = 'Mls@29052003.*'

# try
def load_model(model_name):
    with open(model_name, 'rb') as f:
        model = pickle.load(f)
    return model

def load_label_encoder(label_name):
    with open(label_name, 'rb') as f:
        label_encoder = pickle.load(f)
    return label_encoder

fuel_model = load_model('model_fuel.pkl')
vehicle_model = load_model('model_vehicle.pkl')
driver_model = load_model('model_driver.pkl')

fuel_label_encoder = load_label_encoder('label_fuel.pkl')
vehicle_label_encoder = load_label_encoder('label_vehicle.pkl')
driver_label_encoder = load_label_encoder('label_driver.pkl')


@app.route('/fuel', methods=['GET', 'POST'])
def fuel():
    if request.method == 'POST':
        # Get the input values
        vehicle_class = request.form['vehicle_class']
        engine_size = request.form['engine_size']
        cylinders = request.form['cylinders']
        transmission = request.form['transmission']
        fuel_type = request.form['fuel_type']
        co2_rating = request.form['co2_rating']

        # Create a DataFrame with the input values
        df = pd.DataFrame([[vehicle_class, engine_size, cylinders, transmission, fuel_type, co2_rating]], columns=['Vehicle class', 'Engine size (L)', 'Cylinders', 'Transmission', 'Fuel type', 'CO2 rating'])
        # le = LabelEncoder()
        # df['Vehicle class'] = le.fit_transform(df['Vehicle class'])
        # df['Transmission'] = le.fit_transform(df['Transmission'])
        # df['Fuel type'] = le.fit_transform(df['Fuel type'])

        for column in fuel_label_encoder:
            df[column] = fuel_label_encoder[column].transform(df[column])


        # Make a prediction
        prediction = fuel_model.predict(df)

        return render_template('Fuelpredictor.html', prediction=prediction[0])
    else:
        return render_template('Fuelpredictor.html')
    
@app.route('/vehicle', methods=['GET', 'POST'])
def vehicle():
    if request.method == 'POST':
        # Get the input values
        driving_duration = request.form['driving_duration']
        average_speed = request.form['average_speed']
        co2_emissions = request.form['co2_emissions']
        combined = request.form['combined']
        vehicle_load = request.form['vehicle_load']

        # Create a DataFrame with the input values
        df = pd.DataFrame([[driving_duration, average_speed, co2_emissions, combined, vehicle_load]], columns=['Driving_Duration_hrs', 'Average_Speed_kmh', 'CO2 emissions (g/km)', 'Combined (L/100 km)', 'Vehicle_Load'])
        
        for column in vehicle_label_encoder:
            df[column] = vehicle_label_encoder[column].transform(df[column])

        # Make a prediction
        prediction = vehicle_model.predict(df)

        return render_template('Maintanence.html', prediction=prediction[0])
    else:
        return render_template('Maintanence.html')




#try

# Load the trained SVM model
# with open('svm_model.pkl', 'rb') as f:
#     svm_model = pickle.load(f)

# # Define a function to get the driving style label
# def get_driving_style_label(prediction):
#     driving_style_labels = ['aggressive', 'conservative', 'moderate']
#     return driving_style_labels[prediction]

# @app.route('/')
# def login():
#     return render_template('Login.html')


username = 'admin'
password = 'password'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']
        if form_username == username and form_password == password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('Login.html', error='Invalid credentials')
    return render_template('Login.html')




@app.route('/home')
def home():
    if 'logged_in' in session:
        return render_template('Homepage.html')
    else:
        return redirect(url_for('login'))

@app.route('/driverprediction', methods=['GET', 'POST'])
def driverprediction():
    if request.method == 'POST':
        # Get the input values
        driving_duration = request.form['driving_duration']
        average_speed = request.form['average_speed']
        acceleration_pattern = request.form['acceleration_pattern']
        braking_pattern = request.form['braking_pattern']
        safety_features_usage = request.form['safety_features_usage']
        traffic_violations = request.form['traffic_violations']
 
        # Create a DataFrame with the input values
        input_data = pd.DataFrame({
            'Driving_Duration_hrs': [driving_duration],
            'Average_Speed_kmh': [average_speed],
            'Acceleration_Pattern': [acceleration_pattern],
            'Braking_Pattern': [braking_pattern],
            'Safety_Features_Usage': [safety_features_usage],
            'Traffic_Violations': [traffic_violations]
        })
 
        # Encode categorical variables
        categorical_columns = ['Acceleration_Pattern', 'Braking_Pattern', 'Safety_Features_Usage']
        # for column in categorical_columns:
        #     input_data[column] = driver_label_encoder.transform([input_data[column][0]])
        for col in categorical_columns:
            input_data[col] = driver_label_encoder[col].transform(input_data[col])
 
        # Make a prediction
        prediction = driver_model.predict(input_data)
 
        return render_template('Drivingstyle.html', predicted_driving_style_label=prediction[0])
    else:
        return render_template('Drivingstyle.html')
 

if __name__ == '__main__':
    app.run(debug=True)