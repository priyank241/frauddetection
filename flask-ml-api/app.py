import pandas as pd
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the preprocessor
with open("preprocessor.pkl", "rb") as f:
    preprocessor = pickle.load(f)

# Load the trained RandomForest model
with open("rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

print("Preprocessor and RandomForest model loaded successfully!")

# Define categorical and numerical columns
cat_cols = ['merchant', 'category', 'gender', 'city', 'state', 'is_weekend']
num_cols = ['amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long',
            'hour', 'day', 'weekday', 'day_of_year', 'week_of_year', 'month', 'quarter', 'year']

def preprocessing(df):
    """Preprocess incoming DataFrame"""
    cols_to_drop = ['cc_num', 'first', 'last', 'street', 'zip', 'job', 'trans_num', 'unix_time', 'dob']
    df = df.drop(columns=cols_to_drop, errors='ignore')

    df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
    df['year'] = df['trans_date_trans_time'].dt.year
    df['month'] = df['trans_date_trans_time'].dt.month
    df['day'] = df['trans_date_trans_time'].dt.day
    df['hour'] = df['trans_date_trans_time'].dt.hour
    df['weekday'] = df['trans_date_trans_time'].dt.weekday  # Monday=0, Sunday=6
    df['is_weekend'] = df['weekday'].isin([5, 6]).astype(int)  # 1 for Sat/Sun, 0 otherwise
    df['day_of_year'] = df['trans_date_trans_time'].dt.dayofyear
    df['week_of_year'] = df['trans_date_trans_time'].dt.isocalendar().week
    df['quarter'] = df['trans_date_trans_time'].dt.quarter

    df = df.drop(columns=['trans_date_trans_time'], errors='ignore')

    return df

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receive JSON data and convert it to DataFrame
        data = request.get_json()
        df = pd.DataFrame(data)

        # Apply preprocessing
        df = preprocessing(df)

        # Feature transformation
        X = df[num_cols + cat_cols]
        X_transformed = preprocessor.transform(X)
        X_transformed_df = pd.DataFrame(X_transformed.toarray(), columns=preprocessor.get_feature_names_out())

        # Make predictions
        y_pred = rf_model.predict(X_transformed_df)

        # Return JSON response
        return jsonify({"predictions": y_pred.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
