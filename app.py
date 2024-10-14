from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load your trained models
flight_model = joblib.load('rf_model_F.pkl')  # Flight prediction model
hotel_model = joblib.load('rf_model_H.pkl')    # Hotel prediction model

# Categorical mappings for encoding
agency_mapping = {'CloudFy': 0, 'FlyingDrops': 1, 'Rainbow': 2}
flight_type_mapping = {'economic': 0, 'firstClass': 1,  'premium': 2}
hotel_name_mapping = {
    'Hotel A': 0,
    'Hotel AF': 1,
    'Hotel AU': 2,
    'Hotel BD': 3,
    'Hotel BP': 4,
    'Hotel BW': 5,
    'Hotel CB': 6,
    'Hotel K': 7,
    'Hotel Z': 8
}

# Create mappings for 'from' and 'to' locations
location_mapping = {
    'Aracaju (SE)': 0,
    'Brasilia (DF)': 1,
    'Campo Grande (MS)': 2,
    'Florianopolis (SC)': 3,
    'Natal (RN)': 4,
    'Recife (PE)': 5,
    'Rio de Janeiro (RJ)': 6,
    'Salvador (BH)': 7,
    'Sao Paulo (SP)': 8
}

# Define a dictionary for time and distance between routes
route_info = {
    ('Recife (PE)', 'Florianopolis (SC)'): (1.76, 676.53),
    ('Florianopolis (SC)', 'Recife (PE)'): (1.76, 676.53),
    ('Brasilia (DF)', 'Florianopolis (SC)'): (1.66, 637.56),
    ('Florianopolis (SC)', 'Brasilia (DF)'): (1.66, 637.56),
    ('Aracaju (SE)', 'Salvador (BH)'): (2.16, 830.86),
    ('Salvador (BH)', 'Aracaju (SE)'): (2.16, 830.86),
    ('Aracaju (SE)', 'Campo Grande (MS)'): (1.69, 650.1),
    ('Campo Grande (MS)', 'Aracaju (SE)'): (1.69, 650.1),
    ('Brasilia (DF)', 'Aracaju (SE)'): (1.11, 425.98),
    ('Aracaju (SE)', 'Brasilia (DF)'): (1.11, 425.98),
    ('Recife (PE)', 'Sao Paulo (SP)'): (1.26, 486.52),
    ('Sao Paulo (SP)', 'Recife (PE)'): (1.26, 486.52),
    ('Brasilia (DF)', 'Campo Grande (MS)'): (0.72, 277.7),
    ('Campo Grande (MS)', 'Brasilia (DF)'): (0.72, 277.7),
    ('Brasilia (DF)', 'Sao Paulo (SP)'): (0.67, 257.81),
    ('Sao Paulo (SP)', 'Brasilia (DF)'): (0.67, 257.81),
    ('Brasilia (DF)', 'Salvador (BH)'): (1.76, 676.56),
    ('Salvador (BH)', 'Brasilia (DF)'): (1.76, 676.56),
    ('Recife (PE)', 'Natal (RN)'): (0.58, 222.67),
    ('Natal (RN)', 'Recife (PE)'): (0.58, 222.67),
    ('Brasilia (DF)', 'Natal (RN)'): (1.43, 550.69),
    ('Natal (RN)', 'Brasilia (DF)'): (1.43, 550.69),
    ('Recife (PE)', 'Salvador (BH)'): (2.05, 788.55),
    ('Salvador (BH)', 'Recife (PE)'): (2.05, 788.55),
    ('Recife (PE)', 'Campo Grande (MS)'): (1.39, 535.4),
    ('Campo Grande (MS)', 'Recife (PE)'): (1.39, 535.4),
    ('Brasilia (DF)', 'Recife (PE)'): (0.63, 242.21),
    ('Recife (PE)', 'Brasilia (DF)'): (0.63, 242.21),
    ('Aracaju (SE)', 'Sao Paulo (SP)'): (1.02, 392.76),
    ('Sao Paulo (SP)', 'Aracaju (SE)'): (1.02, 392.76),
    ('Aracaju (SE)', 'Natal (RN)'): (0.46, 176.33),
    ('Natal (RN)', 'Aracaju (SE)'): (0.46, 176.33),
    ('Aracaju (SE)', 'Recife (PE)'): (1.44, 555.74),
    ('Recife (PE)', 'Aracaju (SE)'): (1.44, 555.74),
    ('Aracaju (SE)', 'Rio de Janeiro (RJ)'): (1.55, 597.61),
    ('Rio de Janeiro (RJ)', 'Aracaju (SE)'): (1.55, 597.61),
    ('Aracaju (SE)', 'Florianopolis (SC)'): (2.1, 808.85),
    ('Florianopolis (SC)', 'Aracaju (SE)'): (2.1, 808.85),
    ('Brasilia (DF)', 'Rio de Janeiro (RJ)'): (0.48, 183.37),
    ('Rio de Janeiro (RJ)', 'Brasilia (DF)'): (0.48, 183.37),
    ('Recife (PE)', 'Rio de Janeiro (RJ)'): (2.3, 885.57),
    ('Rio de Janeiro (RJ)', 'Recife (PE)'): (2.3, 885.57),
    ('Campo Grande (MS)', 'Florianopolis (SC)'): (1.49, 573.81),
    ('Florianopolis (SC)', 'Campo Grande (MS)'): (1.49, 573.81),
    ('Campo Grande (MS)', 'Salvador (BH)'): (1.36, 522.34),
    ('Salvador (BH)', 'Campo Grande (MS)'): (1.36, 522.34),
    ('Campo Grande (MS)', 'Sao Paulo (SP)'): (0.44, 168.22),
    ('Sao Paulo (SP)', 'Campo Grande (MS)'): (0.44, 168.22),
    ('Campo Grande (MS)', 'Natal (RN)'): (0.65, 250.68),
    ('Natal (RN)', 'Campo Grande (MS)'): (0.65, 250.68),
    ('Campo Grande (MS)', 'Rio de Janeiro (RJ)'): (2.09, 806.48),
    ('Rio de Janeiro (RJ)', 'Campo Grande (MS)'): (2.09, 806.48),
    ('Natal (RN)', 'Rio de Janeiro (RJ)'): (1.55, 595.03),
    ('Rio de Janeiro (RJ)', 'Natal (RN)'): (1.55, 595.03),
    ('Sao Paulo (SP)', 'Salvador (BH)'): (1.04, 401.66),
    ('Salvador (BH)', 'Sao Paulo (SP)'): (1.04, 401.66),
    ('Sao Paulo (SP)', 'Natal (RN)'): (0.85, 327.55),
    ('Natal (RN)', 'Sao Paulo (SP)'): (0.85, 327.55),
    ('Sao Paulo (SP)', 'Rio de Janeiro (RJ)'): (0.86, 331.89),
    ('Rio de Janeiro (RJ)', 'Sao Paulo (SP)'): (0.86, 331.89),
    ('Sao Paulo (SP)', 'Florianopolis (SC)'): (1.46, 562.14),
    ('Florianopolis (SC)', 'Sao Paulo (SP)'): (1.46, 562.14),
    ('Natal (RN)', 'Salvador (BH)'): (1.85, 710.57),
    ('Salvador (BH)', 'Natal (RN)'): (1.85, 710.57),
    ('Natal (RN)', 'Florianopolis (SC)'): (1.84, 709.37),
    ('Florianopolis (SC)', 'Natal (RN)'): (1.84, 709.37),
    ('Florianopolis (SC)', 'Rio de Janeiro (RJ)'): (1.21, 466.3),
    ('Rio de Janeiro (RJ)', 'Florianopolis (SC)'): (1.21, 466.3),
    ('Florianopolis (SC)', 'Salvador (BH)'): (2.44, 937.77),
    ('Salvador (BH)', 'Florianopolis (SC)'): (2.44, 937.77),
}


def get_time_distance(from_location, to_location):
    return route_info.get((from_location, to_location), (None, None))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict_flight')
def predict_flight():
    return render_template('predict_flight.html')


@app.route('/predict_hotel')
def predict_hotel():
    return render_template('predict_hotel.html')


@app.route('/predict_both')
def predict_both():
    return render_template('predict_both.html')


@app.route('/predict_flight_price', methods=['POST'])
def predict_flight_price():
    data = request.form
    predictions = {}

    try:
        print(f"Received data: {data}")

        if data['from'] == data['to']:
            return jsonify({"error": "Departure and arrival locations cannot be the same."}), 400

        date_input = datetime.strptime(data['date'], '%Y-%m-%d')
        year, month, day, day_of_week = date_input.year, date_input.month, date_input.day, date_input.weekday()

        time, distance = get_time_distance(data['from'], data['to'])

        if time is None or distance is None:
            return jsonify({"error": "Route not found"}), 404

        flight_features = [
            location_mapping[data['from']],
            location_mapping[data['to']],
            flight_type_mapping[data['flightType']],
            agency_mapping[data['agency']],
            year, month, day, day_of_week,
            time, distance
        ]

        # Predict the flight price
        predicted_price = flight_model.predict([flight_features])[0]

        # Round the predicted price to 2 decimal points
        predictions['flight_price'] = round(predicted_price, 2)
        predictions['time'] = time
        predictions['distance'] = distance

        return predictions  # Change this to just return predictions

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/predict_hotel_price', methods=['POST'])
def predict_hotel_price():
    try:
        data = request.form
        place = data['place']
        hotel = data['hotel']
        days = int(data['days'])
        date_str = data['date']

        date = pd.to_datetime(date_str)
        year = date.year
        month = date.month
        day = date.day
        dayofweek = date.dayofweek

        hotel_encoded = hotel_name_mapping[hotel]
        place_encoded = location_mapping[place]

        X_hotel = [[hotel_encoded, place_encoded,
                    days, year, month, day, dayofweek]]

        predicted_price = hotel_model.predict(X_hotel)

        total_price = predicted_price[0] * days  # multiply by number of days
        predicted_price_rounded = round(predicted_price[0].item(), 2)
        total_price_rounded = round(total_price, 2)

        return jsonify({
            'predicted_price_per_day': f"{predicted_price_rounded:.2f}",
            'total_price': f"{total_price_rounded:.2f}"
        })

    except Exception as e:
        print(f'Error during hotel prediction: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/predict_both_prices', methods=['POST'])
def predict_both_prices():
    data = request.form
    predictions = {}

    try:
        print(f"Received data: {data}")

        if data['from'] == data['to']:
            return jsonify({"error": "Departure and arrival locations cannot be the same."}), 400
        place = data['to']
        hotel = data['hotel']
        days = int(data['days'])

        date_input = datetime.strptime(data['date'], '%Y-%m-%d')
        year, month, day, day_of_week = date_input.year, date_input.month, date_input.day, date_input.weekday()

        time, distance = get_time_distance(data['from'], data['to'])

        if time is None or distance is None:
            return jsonify({"error": "Route not found"}), 404

        flight_features = [
            location_mapping[data['from']],
            location_mapping[data['to']],
            flight_type_mapping[data['flightType']],
            agency_mapping[data['agency']],
            year, month, day, day_of_week,
            time, distance
        ]

        # Predict the flight price
        predicted_price_f = flight_model.predict([flight_features])[0]

        hotel_encoded = hotel_name_mapping[hotel]
        place_encoded = location_mapping[place]

        X_hotel = [[hotel_encoded, place_encoded,
                    days, year, month, day, day_of_week]]

        predicted_price = hotel_model.predict(X_hotel)

        total_price_H = predicted_price[0] * days  # multiply by number of days
        predicted_price_rounded = round(predicted_price[0].item(), 2)
        total_price_rounded = round(total_price_H, 2)
        total_price = predicted_price_f + total_price_H

        return jsonify({
            'flight_price': round(predicted_price_f, 2),
            'predicted_price_per_day': f"{predicted_price_rounded:.2f}",
            'hotel_price_for_days': f"{total_price_rounded:.2f}",
            'total_price': round(total_price, 2)
        })

    except Exception as e:
        print(f'Error during hotel prediction: {str(e)}')
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
