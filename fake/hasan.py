from flask import Flask, request, jsonify, make_response
import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from flask_cors import CORS, cross_origin
import joblib
from pymongo import MongoClient
from app import mongo

app = Flask(__name__)
# CORS(app)
# CORS(app, origins=['http://localhost:3003'])
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})
# CORS(app, resources={r"/predict": {"origins": "*"}})


# Load the property data from MongoDB
property_data = list(mongo.db.price.find())

df = pd.DataFrame(property_data)

duplicates = df.apply(lambda x: x.duplicated()).sum()
data = df.drop_duplicates()
property_df = data.drop(columns=['images', 'title'])
print(property_df)

# Extract the reviews from the DataFrame
reviews = np.array(property_df['description'])
test_reviews = reviews[3000:]
sample_review_ids = [626, 233, 280]
test_reviews = np.array(test_reviews)

for sample_review_id in sample_review_ids:
    description = test_reviews[sample_review_id]
    print('REVIEW:', description)
    print('Predicted Sentiment polarity:',
          TextBlob(description).sentiment.polarity)
    print('-' * 60)

# Calculate sentiment polarity for all test reviews
sentiment_polarity = [
    TextBlob(review).sentiment.polarity for review in test_reviews]
print(sentiment_polarity)


property_df["latitude"] = property_df["latitude"].astype(float)
property_df["longitude"] = property_df["longitude"].astype(float)

locations = property_df[['latitude', 'longitude']].values
k = 5  # Number of neighbors to consider
nn_model = NearestNeighbors(n_neighbors=k)
nn_model.fit(locations)
neighbors_indices = nn_model.kneighbors(
    locations, n_neighbors=k, return_distance=False)
# avg_neighbor_price = property_df.loc[neighbors_indices[0], "avg_neighbor_price"].mean()
# print(avg_neighbor_price)


avg_neighbor_prices = []
for indices in neighbors_indices:
    avg_price = property_df.loc[indices, "base_price"].mean()
    avg_neighbor_prices.append(avg_price)
property_df["avg_neighbor_price"] = avg_neighbor_prices
print(property_df["avg_neighbor_price"])

numeric_features = ["number_of_bedrooms",
                    "base_price", "bathrooms", "beds", "guests"]
numeric_df = property_df[numeric_features].fillna(
    property_df[numeric_features].mean())

categorical_features = ["location", "property_type", "option",
                        "amenities", "seasonality", "bed_type", "neighborhood", "guest_type"]
categorical_df = property_df[categorical_features].fillna(
    property_df[categorical_features].mode().iloc[0])
print(categorical_df)

label_encoder = LabelEncoder()
for feature in categorical_features:
    categorical_df[feature] = label_encoder.fit_transform(
        categorical_df[feature])
print(categorical_df[feature])

# Combine numeric and categorical DataFrames
combined_df = pd.concat([numeric_df, categorical_df], axis=1)
print(combined_df)

# Remove extreme outliers in base_price
price_df = property_df[combined_df['base_price'] < 5000]
print(price_df)

# Transformation
combined_df['log_base_price'] = np.log(combined_df['base_price'])
print(combined_df['log_base_price'])

X = combined_df.drop(columns=["base_price", "log_base_price"])
# X = combined_df.drop(columns=["base_price"])
# y = combined_df["base_price"]
y = combined_df["log_base_price"]
print(X)
print(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

ridge_model = Ridge()
ridge_model.fit(X_train_scaled, y_train)

y_pred = ridge_model.predict(X_test_scaled)
print(y_pred)
mse = mean_squared_error(y_test, y_pred)
# print("Ridge Regression Model:", ridge_model)
print("Ridge Regression Model:", y_pred)
print("Mean Squared Error:", mse)

joblib.dump(ridge_model, 'ridge_model.joblib')
joblib.dump(scaler, 'scaler.joblib')


# @app.route('/predict', methods=['OPTIONS'])
@app.route('/predict', methods=['POST', 'OPTIONS'])
@cross_origin(origin="localhost", headers=["Content-Type", "authorization"])
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add("Access-Control-Allow-Origin", "http://localhost:3003")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
        return response
    # else:
    #     # Handle other HTTP methods if needed
    #     resp = jsonify('Method not allowed')
    #     resp.status_code = 405
    #     return resp

    elif request.method == 'POST':
        data = request.json
        print("Received data:", data)
        # Extract the features from the request data
        location = data['location']
        # latitude = float(data['latitude'])
        # longitude = float(data['longitude'])
        latitude = data['latitude']
        longitude = data['longitude']
        property_type = data['property_type']
        # property_type = data.get('property_type', '')
        option = data['option']
        guests = int(data['guests'])
        number_of_bedrooms = int(data['number_of_bedrooms'])
        # amenities = data['amenities']
        # amenities = data.get('amenities', [])
        amenities = data.get('amenities', [])
        if isinstance(amenities, str):
            amenities = amenities.split(',')
        seasonality = data['seasonality']
        base_price = float(data['base_price'])
        bathrooms = int(data['bathrooms'])
        bed_type = data['bed_type']
        beds = int(data['beds'])
        neighborhood = data['neighborhood']
        guest_type = data['guest_type']
        description = data['description']
        title = data['title']
        # image = data['image']

        print("data:")
        print("Location:", location)
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        print("property_type:", property_type)
        print("option:", option)
        print("guests:", guests)
        print("number_of_bedrooms:", number_of_bedrooms)
        print("amenities:", amenities)
        print("seasonality:", seasonality)
        print("base_price:", base_price)
        print("bathrooms:", bathrooms)
        print("bed_type:", bed_type)
        print("beds:", beds)
        print("neighborhood:", neighborhood)
        print("guest_type:", guest_type)
        print("description:", description)
        print("title:", title)


        # Clean up amenities list (remove extra quotes)
        cleaned_amenities = [amenity.strip('"') for amenity in amenities]

        # predicted_price = get_predict(description)
        sentiment = get_predict(description)
        suggested_price = get_pred(X_test_scaled)
        nearest_price = get_nearest(latitude, longitude)

    #     if location and latitude and longitude and property_type and option and guests and number_of_bedrooms and cleaned_amenities and seasonality and base_price and bathrooms and bed_type and beds and neighborhood and guest_type and description and title and request.method == 'POST':
    #         # save details
    #         id = mongo.db.property_price.insert_one({"location": location, "latitude": latitude, "longitude": longitude, "property_type": property_type, "option": option, "guests": guests, "number_of_bedrooms": number_of_bedrooms, "amenities": cleaned_amenities, "seasonality": seasonality, "base_price": base_price,
    #                                                  "bathrooms": bathrooms, "bed_type": bed_type, "beds": beds, "neighbourhood": neighborhood, "guest_type": guest_type, "description": description, "title": title, "sentiment": predicted_price, "prdicted_price": suggested_price, "nearest_price": nearest_price})
    #         resp = jsonify('Suggested price successfully created!')
    #         resp.status_code = 200
    #         return resp
    #     else:
    #         resp = jsonify('Invalid data or missing values')
    #         resp.status_code = 400
    #         return resp
    # else:
    #     # Handle other HTTP methods if needed
    #     resp = jsonify('Method not allowed')
    #     resp.status_code = 405
    #     return resp

    if location and latitude and longitude and property_type and option and guests and number_of_bedrooms and cleaned_amenities and seasonality and base_price and bathrooms and bed_type and beds and neighborhood and guest_type and description and title and request.method == 'POST':
        id = mongo.db.property_price.insert_one({
            "location": location, "latitude": latitude, "longitude": longitude,
            "property_type": property_type, "option": option, "guests": guests,
            "number_of_bedrooms": number_of_bedrooms, "amenities": cleaned_amenities,
            "seasonality": seasonality, "base_price": base_price,
            "bathrooms": bathrooms, "bed_type": bed_type, "beds": beds,
            "neighbourhood": neighborhood, "guest_type": guest_type,
            "description": description, "title": title,
            "sentiment": sentiment, "suggested_price": suggested_price,
            "nearest_price": nearest_price
        })
        resp = jsonify({'message': 'Suggested price successfully created!', 'property_id': str(id.inserted_id), "sentiment": sentiment, "suggested_price": suggested_price, "nearest_price": nearest_price})
        resp.status_code = 201  # Created status code
        return resp
    else:
        resp = jsonify({'error': 'Invalid data or missing values'})
        resp.status_code = 400  # Bad Request status code
        return resp


def get_predict(description):
    sentiment_polarity = TextBlob(description).sentiment.polarity

    # Classify the sentiment based on the sentiment score
    if sentiment_polarity >= 0.05:
        return 'positive'
    elif sentiment_polarity <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def get_pred(X_test_scaled):
    # predicted_price = ridge_model.predict(X_test_scaled)[0]
    # formatted_price = round(np.exp(predicted_price), 2)

    suggested_price = ridge_model.predict(X_test_scaled)[0]
    formatted_price = round(np.exp(suggested_price), 2)
    return formatted_price


def get_nearest(latitude, longitude):
    location_data = np.array([[latitude, longitude]])
    neighbors_indices = nn_model.kneighbors(
        location_data, n_neighbors=k, return_distance=False)
    # avg_neighbor_price = property_df.loc[neighbors_indices[0], "base_price"].mean()
    avg_neighbor_price = round(
        property_df.loc[neighbors_indices[0], "base_price"].mean(), 2)
    return avg_neighbor_price


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)



# if __name__ == '__main__':
#     app.run('localhost', 5051)
