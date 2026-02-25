SmartSense: Emotion-Aware Activity & Location Suggester
SmartSense is a Python-based intelligence tool that provides personalized activity and location recommendations. By analyzing a user's emotional state—derived from social media data—and cross-referencing it with real-time local weather and geographic data, the app suggests the perfect "vibe" for the user's current situation.

🧠 How It Works
Data Ingestion: Processes CSV datasets containing Instagram captions and categorized location data.

Location & Weather Sensing: Automatically detects the user's current coordinates and fetches real-time weather conditions.

Emotion Analysis: Calculates emotion probabilities (e.g., Joy, Sadness, Adventurous) based on the user's textual input/history.

Recommendation Engine: A logic-based system that matches Emotion + Weather + Location Data to suggest the best activities.

🚀 Key Features
Emotion Probability Modeling: Uses Natural Language Processing (NLP) to study user sentiment.

Real-time Context Awareness: Integrates Geolocation and Weather APIs to ensure suggestions are practical (e.g., no outdoor hiking suggestions during a storm).

CSV Data Integration: Easily swap or update the locations.csv and captions.csv to customize the app for different cities or niches.

Smart Activity Mapping: Suggests specific locations from the database that match the user's predicted mood.

🛠️ Tech Stack
Language: Python 3.x

Data Handling: pandas (for CSV processing)

APIs: OpenWeatherMap API (Weather), IPStack/Geopy (Location)

NLP/AI: TextBlob, VADER, or Scikit-learn (for emotion probabilities)

Interface: CLI or Streamlit (specify which one you are using)
