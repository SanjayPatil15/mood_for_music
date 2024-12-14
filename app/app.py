from flask import Flask, render_template, request, jsonify
from keras.models import load_model
import numpy as np
import cv2
from keras.applications.vgg16 import preprocess_input
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# Load the mood classifier model
model = load_model('models/mood_classifier_model.h5')
label_encoder = LabelEncoder()

# Load the music recommendation model
import pandas as pd
music_df = pd.read_csv('data/raw_data/data_moods.csv')

# Function to process image and predict mood
def preprocess_image(image_path, target_size=(224, 224)):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

# Function to recommend music based on mood
def recommend_music(mood, features_df, knn_model):
    # Get the mood's row in the music dataset
    mood_features = features_df[music_df['mood'] == mood].mean().values.reshape(1, -1)
    # Find nearest neighbors
    distances, indices = knn_model.kneighbors(mood_features)
    return music_df.iloc[indices[0]]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    image_path = 'static/uploads/' + file.filename
    file.save(image_path)
    
    img = preprocess_image(image_path)
    features = model.predict(img).flatten()
    
    # Predict mood
    mood = label_encoder.inverse_transform([np.argmax(features)])[0]
    
    # Recommend music based on mood
    recommended_songs = recommend_music(mood, music_df[['danceability', 'energy', 'acousticness', 'valence', 'loudness', 'tempo']], NearestNeighbors(n_neighbors=5))
    
    song_list = recommended_songs[['name', 'artist', 'album']].to_dict(orient='records')
    return jsonify(mood=mood, recommendations=song_list)

if __name__ == '__main__':
    app.run(debug=True)
