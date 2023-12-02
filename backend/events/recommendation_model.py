import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import EventRegistration, Event


# from models import Event
# Assume you have a DataFrame `events` with 'title', 'description', and 'category'
# And a DataFrame `user_profiles` with a 'liked_events' column containing event titles
# Function to get recommendations based on a user profile
def get_recommendations(user_email):
    try:
        # Retrieve all events and registrations
        event_objects = Event.objects.all()
        registration_objects = EventRegistration.objects.filter(user__email=user_email)

        # Convert to DataFrames
        events = pd.DataFrame(list(event_objects.values('id', 'description')))
        user_profiles = pd.DataFrame(list(registration_objects.values('event_id')))

        # Rename the 'event_id' column to 'event' to match the expected column name
        user_profiles.rename(columns={'event_id': 'event'}, inplace=True)

        # Check if the DataFrame is empty or if 'description' column is missing
        if events.empty or 'description' not in events.columns:
            raise ValueError("No event data available or missing 'description' column.")

        # Create TF-IDF vectors for your event descriptions
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(events['description'])

        # Compute the cosine similarity between all events
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get the list of event IDs the user has liked/registered for
        user_likes = user_profiles['event'].tolist()
        sim_scores = []

        for event_id in user_likes:
            # Check if the event ID is in the events DataFrame
            if event_id in events['id'].values:
                idx = events.index[events['id'] == event_id].tolist()
                # If the event ID exists, get the pairwise similarity scores of all events with that event
                if idx:
                    sim_scores.extend(list(enumerate(cosine_sim[idx[0]])))

        # Sort the events based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar events
        sim_scores = sim_scores[1:4]

        # Get the event indices
        event_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar events
        return events['id'].iloc[event_indices].tolist()

    except ValueError as ve:
        # Handle specific error
        print(f"Value Error: {ve}")
        return []
    except ObjectDoesNotExist:
        # Handle the case where the Event does not exist
        print("No event found for the given user.")
        return []
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {e}")
        return []