from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
# from models import Event
# Assume you have a DataFrame `events` with 'title', 'description', and 'category'
# And a DataFrame `user_profiles` with a 'liked_events' column containing event titles
event_json = [
    {
        "id": 274,
        "title": "Special expect remember health.",
        "description": "Age poor impact memory large. Enough record community catch. South benefit according picture. Thus gun consumer Mr push idea two.\nAsk discussion three support. Environment set among.",
        "location": "West Johnfurt",
        "is_public": False,
        "price": "116.60",
        "capacity": 935,
        "remaining_slots": 934,
        "registration_end_date": "2024-10-05T15:15:52.331160Z",
        "start_date": "2024-10-05T15:15:52.331160Z",
        "end_date": "2024-10-05T22:15:52.331160Z",
        "created_at": "2023-11-04T15:15:52.331247Z",
        "updated_at": "2023-11-04T15:15:52.331249Z",
        "user": 86,
        "user_email": "angelabennett@example.net",
        "categories": [
            "result"
        ],
        "photo": None
    },
    {
        "id": 275,
        "title": "Show several which keep number many officer.",
        "description": "Pass fund company. Food with ever price or short. Front pass political expect exist.\nAnyone model mouth picture development eye into best. Worker dream author nearly.",
        "location": "Hicksshire",
        "is_public": False,
        "price": "299.87",
        "capacity": 790,
        "remaining_slots": 790,
        "registration_end_date": "2024-01-17T15:15:52.332900Z",
        "start_date": "2024-01-17T15:15:52.332900Z",
        "end_date": "2024-01-19T11:15:52.332900Z",
        "created_at": "2023-11-04T15:15:52.332982Z",
        "updated_at": "2023-11-04T15:15:52.332984Z",
        "user": 86,
        "user_email": "angelabennett@example.net",
        "categories": [
            "strong"
        ],
        "photo": None
    },
    {
        "id": 276,
        "title": "Fire social hit.",
        "description": "Score million what consumer product task over. Hot piece including there truth.\nWill poor per figure. Nation girl laugh. Any him action which.",
        "location": "East Renee",
        "is_public": False,
        "price": "346.23",
        "capacity": 158,
        "remaining_slots": 157,
        "registration_end_date": "2024-02-21T15:15:52.334472Z",
        "start_date": "2024-02-21T15:15:52.334472Z",
        "end_date": "2024-02-21T22:15:52.334472Z",
        "created_at": "2023-11-04T15:15:52.334556Z",
        "updated_at": "2023-11-04T15:15:52.334558Z",
        "user": 87,
        "user_email": "yvonne38@example.com",
        "categories": [
            "care"
        ],
        "photo": None
    },
    {
        "id": 277,
        "title": "Let keep blue sea.",
        "description": "Base everyone open score road seat. Name decade low site kitchen. Agreement special power yourself.\nEconomy few one feel. Religious keep station return.",
        "location": "Derekhaven",
        "is_public": True,
        "price": "150.39",
        "capacity": 73,
        "remaining_slots": 73,
        "registration_end_date": "2024-01-09T15:15:52.335850Z",
        "start_date": "2024-01-09T15:15:52.335850Z",
        "end_date": "2024-01-09T17:15:52.335850Z",
        "created_at": "2023-11-04T15:15:52.335927Z",
        "updated_at": "2023-11-04T15:15:52.335929Z",
        "user": 87,
        "user_email": "yvonne38@example.com",
        "categories": [
            "them"
        ],
        "photo": None
    },
    {
        "id": 278,
        "title": "Something peace door picture and.",
        "description": "Vote look him world growth ability. Less technology believe. Beautiful voice program in.\nPoint owner option growth help degree able. Mean describe wait anything western.",
        "location": "Lake Carl",
        "is_public": False,
        "price": "255.48",
        "capacity": 279,
        "remaining_slots": 278,
        "registration_end_date": "2024-01-25T15:15:52.337153Z",
        "start_date": "2024-01-25T15:15:52.337153Z",
        "end_date": "2024-01-27T19:15:52.337153Z",
        "created_at": "2023-11-04T15:15:52.337223Z",
        "updated_at": "2023-11-04T15:15:52.337225Z",
        "user": 87,
        "user_email": "yvonne38@example.com",
        "categories": [
            "benefit"
        ],
        "photo": None
    },
    {
        "id": 279,
        "title": "Surface news artist source lose.",
        "description": "Across about relationship economy enough game use. Card scene debate later.\nAge word beautiful charge. Later last position close. Television allow within rule provide note physical.",
        "location": "West Stuartview",
        "is_public": True,
        "price": "410.92",
        "capacity": 122,
        "remaining_slots": 121,
        "registration_end_date": "2024-03-15T15:15:52.338393Z",
        "start_date": "2024-03-15T15:15:52.338393Z",
        "end_date": "2024-03-17T13:15:52.338393Z",
        "created_at": "2023-11-04T15:15:52.338460Z",
        "updated_at": "2023-11-04T15:15:52.338461Z",
        "user": 87,
        "user_email": "yvonne38@example.com",
        "categories": [
            "people"
        ],
        "photo": None
    },
    {
        "id": 280,
        "title": "Democratic long dinner institution.",
        "description": "Candidate third scene me buy tough the. Radio success visit technology material miss about film. Heart dog player stand.\nRecognize interest until fund raise peace too. Protect dog read approach wind.",
        "location": "Port Alexisburgh",
        "is_public": True,
        "price": "457.76",
        "capacity": 435,
        "remaining_slots": 434,
        "registration_end_date": "2024-04-09T15:15:52.339600Z",
        "start_date": "2024-04-09T15:15:52.339600Z",
        "end_date": "2024-04-12T13:15:52.339600Z",
        "created_at": "2023-11-04T15:15:52.339667Z",
        "updated_at": "2023-11-04T15:15:52.339669Z",
        "user": 87,
        "user_email": "yvonne38@example.com",
        "categories": [
            "fear"
        ],
        "photo": None
    },
    {
        "id": 281,
        "title": "Enjoy say soldier watch enough wish.",
        "description": "Soldier single whose daughter Mrs book important.\nProduct hundred small myself. Similar stand two.",
        "location": "Debbiebury",
        "is_public": True,
        "price": "309.42",
        "capacity": 434,
        "remaining_slots": 433,
        "registration_end_date": "2024-11-02T15:15:52.340915Z",
        "start_date": "2024-11-02T15:15:52.340915Z",
        "end_date": "2024-11-05T10:15:52.340915Z",
        "created_at": "2023-11-04T15:15:52.340991Z",
        "updated_at": "2023-11-04T15:15:52.340992Z",
        "user": 88,
        "user_email": "brookepope@example.net",
        "categories": [
            "these"
        ],
        "photo": None
    },
    {
        "id": 282,
        "title": "Back meeting success charge.",
        "description": "American especially threat expert director summer. Trade owner same call. Stay serve another reflect practice finish just.",
        "location": "Brentport",
        "is_public": True,
        "price": "122.37",
        "capacity": 691,
        "remaining_slots": 690,
        "registration_end_date": "2023-12-16T15:15:52.342386Z",
        "start_date": "2023-12-16T15:15:52.342386Z",
        "end_date": "2023-12-19T00:15:52.342386Z",
        "created_at": "2023-11-04T15:15:52.342461Z",
        "updated_at": "2023-11-04T15:15:52.342463Z",
        "user": 88,
        "user_email": "brookepope@example.net",
        "categories": [
            "result"
        ],
        "photo": None
    },
    {
        "id": 283,
        "title": "Thus know power improve anyone.",
        "description": "Think many leader always. Where the bill quality movement rather community. Respond particular wear hear hotel.",
        "location": "Meganborough",
        "is_public": False,
        "price": "114.32",
        "capacity": 961,
        "remaining_slots": 960,
        "registration_end_date": "2024-08-11T15:15:52.343320Z",
        "start_date": "2024-08-11T15:15:52.343320Z",
        "end_date": "2024-08-12T05:15:52.343320Z",
        "created_at": "2023-11-04T15:15:52.343387Z",
        "updated_at": "2023-11-04T15:15:52.343389Z",
        "user": 88,
        "user_email": "brookepope@example.net",
        "categories": [
            "prove"
        ],
        "photo": None
    },
    {
        "id": 284,
        "title": "Full bag thousand skill position especially.",
        "description": "Buy kind week box. Industry listen trial move. On almost sell recent cut market clearly approach.\nBeautiful ahead than decide. Character condition minute field tell.",
        "location": "North Susanchester",
        "is_public": False,
        "price": "413.62",
        "capacity": 328,
        "remaining_slots": 327,
        "registration_end_date": "2024-05-06T15:15:52.344572Z",
        "start_date": "2024-05-06T15:15:52.344572Z",
        "end_date": "2024-05-07T02:15:52.344572Z",
        "created_at": "2023-11-04T15:15:52.344644Z",
        "updated_at": "2023-11-04T15:15:52.344645Z",
        "user": 88,
        "user_email": "brookepope@example.net",
        "categories": [
            "source"
        ],
        "photo": None
    },
    {
        "id": 285,
        "title": "These edge note it performance idea business.",
        "description": "Seek market front statement among music thing team. Plant scientist again budget candidate available. Son pattern box.",
        "location": "Williamsmouth",
        "is_public": True,
        "price": "242.41",
        "capacity": 120,
        "remaining_slots": 119,
        "registration_end_date": "2024-03-17T15:15:52.346019Z",
        "start_date": "2024-03-17T15:15:52.346019Z",
        "end_date": "2024-03-18T23:15:52.346019Z",
        "created_at": "2023-11-04T15:15:52.346092Z",
        "updated_at": "2023-11-04T15:15:52.346094Z",
        "user": 88,
        "user_email": "brookepope@example.net",
        "categories": [
            "second"
        ],
        "photo": None
    },
    {
        "id": 286,
        "title": "Question then should author service.",
        "description": "Movement decade likely almost anyone what especially tend. Future employee picture too commercial approach reflect.",
        "location": "South Jacobtown",
        "is_public": False,
        "price": "497.95",
        "capacity": 603,
        "remaining_slots": 602,
        "registration_end_date": "2024-07-10T15:15:52.347564Z",
        "start_date": "2024-07-10T15:15:52.347564Z",
        "end_date": "2024-07-11T00:15:52.347564Z",
        "created_at": "2023-11-04T15:15:52.347652Z",
        "updated_at": "2023-11-04T15:15:52.347655Z",
        "user": 89,
        "user_email": "hallfrank@example.net",
        "categories": [
            "fall"
        ],
        "photo": None
    },
    {
        "id": 288,
        "title": "City police nature artist blood.",
        "description": "Away defense they accept. Send require great identify move owner. Rate describe look notice. Wall wife place.",
        "location": "North Gregory",
        "is_public": True,
        "price": "3.24",
        "capacity": 591,
        "remaining_slots": 590,
        "registration_end_date": "2024-09-16T15:15:52.350840Z",
        "start_date": "2024-09-16T15:15:52.350840Z",
        "end_date": "2024-09-18T20:15:52.350840Z",
        "created_at": "2023-11-04T15:15:52.350938Z",
        "updated_at": "2023-11-04T15:15:52.350940Z",
        "user": 89,
        "user_email": "hallfrank@example.net",
        "categories": [
            "after"
        ],
        "photo": None
    },
    {
        "id": 290,
        "title": "Imagine dinner several he participant.",
        "description": "Thought fight century fight. Carry say hear fall could example.\nNow use bring wish. Sell site major. Team enough since language author within.\nYes degree lose his Congress want. After fly much.",
        "location": "Raymondton",
        "is_public": True,
        "price": "226.21",
        "capacity": 619,
        "remaining_slots": 618,
        "registration_end_date": "2024-02-12T15:15:52.354510Z",
        "start_date": "2024-02-12T15:15:52.354510Z",
        "end_date": "2024-02-13T16:15:52.354510Z",
        "created_at": "2023-11-04T15:15:52.354604Z",
        "updated_at": "2023-11-04T15:15:52.354605Z",
        "user": 89,
        "user_email": "hallfrank@example.net",
        "categories": [
            "wind"
        ],
        "photo": None
    },
    {
        "id": 296,
        "title": "Key once key event mind well visit recently.",
        "description": "East price population. Herself interest stop none. Sometimes born eight watch.",
        "location": "Edwardshire",
        "is_public": True,
        "price": "28.78",
        "capacity": 729,
        "remaining_slots": 728,
        "registration_end_date": "2024-02-12T15:15:52.364168Z",
        "start_date": "2024-02-12T15:15:52.364168Z",
        "end_date": "2024-02-14T17:15:52.364168Z",
        "created_at": "2023-11-04T15:15:52.364253Z",
        "updated_at": "2023-11-04T15:15:52.364255Z",
        "user": 91,
        "user_email": "iwu@example.net",
        "categories": [
            "likely"
        ],
        "photo": None
    },
    {
        "id": 289,
        "title": "Business Mr reflect although financial.",
        "description": "Structure million will to move use inside public. Positive eat down guess.\nAsk walk art popular. Crime six work money. Team number old glass.",
        "location": "Port Jennifer",
        "is_public": False,
        "price": "165.44",
        "capacity": 599,
        "remaining_slots": 598,
        "registration_end_date": "2023-12-30T15:15:52.352729Z",
        "start_date": "2023-11-13T17:49:27.630000Z",
        "end_date": "2024-01-01T00:15:52.352729Z",
        "created_at": "2023-11-04T15:15:52.352818Z",
        "updated_at": "2023-11-12T21:50:22.208094Z",
        "user": 89,
        "user_email": "hallfrank@example.net",
        "categories": [
            "easy"
        ],
        "photo": None
    },
    {
        "id": 272,
        "title": "string",
        "description": "Have sell within authority apply resource whom. Item choose lot play pretty true side. Prevent deal pattern way air minute establish money.\nReflect fine summer. At middle born cell positive.",
        "location": "Alexisburgh",
        "is_public": True,
        "price": "163.49",
        "capacity": 323,
        "remaining_slots": 323,
        "registration_end_date": "2024-03-28T15:15:52.327058Z",
        "start_date": "2024-03-28T15:15:52.327058Z",
        "end_date": "2024-03-31T08:15:52.327058Z",
        "created_at": "2023-11-04T15:15:52.327184Z",
        "updated_at": "2023-11-23T15:21:24.988983Z",
        "user": 86,
        "user_email": "angelabennett@example.net",
        "categories": [
            "Republican"
        ],
        "photo": None
    }]
registration_json = [
    {
        "id": 273,
        "event": 277,
        "event_detail": {
            "id": 277,
            "title": "Let keep blue sea.",
            "description": "Base everyone open score road seat. Name decade low site kitchen. Agreement special power yourself.\nEconomy few one feel. Religious keep station return.",
            "location": "Derekhaven",
            "is_public": True,
            "price": "150.39",
            "capacity": 73,
            "remaining_slots": 73,
            "registration_end_date": "2024-01-09T15:15:52.335850Z",
            "start_date": "2024-01-09T15:15:52.335850Z",
            "end_date": "2024-01-09T17:15:52.335850Z",
            "created_at": "2023-11-04T15:15:52.335927Z",
            "updated_at": "2023-11-04T15:15:52.335929Z",
            "user": 87,
            "user_email": "yvonne38@example.com",
            "categories": [
                "them"
            ],
            "photo": None
        },
        "is_registered": False,
        "user_email": "smithlaura@example.net",
        "registration_date": "2023-11-04T15:15:52.429385Z",
        "updated_at": "2023-11-17T13:29:07.027335Z"
    },
    {
        "id": 320,
        "event": 282,
        "event_detail": {
            "id": 282,
            "title": "Back meeting success charge.",
            "description": "American especially threat expert director summer. Trade owner same call. Stay serve another reflect practice finish just.",
            "location": "Brentport",
            "is_public": True,
            "price": "122.37",
            "capacity": 691,
            "remaining_slots": 690,
            "registration_end_date": "2023-12-16T15:15:52.342386Z",
            "start_date": "2023-12-16T15:15:52.342386Z",
            "end_date": "2023-12-19T00:15:52.342386Z",
            "created_at": "2023-11-04T15:15:52.342461Z",
            "updated_at": "2023-11-04T15:15:52.342463Z",
            "user": 88,
            "user_email": "brookepope@example.net",
            "categories": [
                "result"
            ],
            "photo": None
        },
        "is_registered": False,
        "user_email": "smithlaura@example.net",
        "registration_date": "2023-11-19T20:44:08.495166Z",
        "updated_at": "2023-11-19T20:44:16.231101Z"
    },
    {
        "id": 321,
        "event": 322,
        "event_detail": {
            "id": 322,
            "title": "strinsdsdg",
            "description": "string",
            "location": "string",
            "is_public": True,
            "price": "20.00",
            "capacity": 2147483647,
            "remaining_slots": 2147483646,
            "registration_end_date": "2023-11-10T15:21:27.902000Z",
            "start_date": "2023-11-10T15:21:27.902000Z",
            "end_date": "2023-11-10T15:21:27.902000Z",
            "created_at": "2023-11-10T15:21:41.905615Z",
            "updated_at": "2023-11-17T15:09:02.014899Z",
            "user": 94,
            "user_email": "smithlaura@example.net",
            "categories": [],
            "photo": None
        },
        "is_registered": True,
        "user_email": "smithlaura@example.net",
        "registration_date": "2023-11-23T15:04:20.001260Z",
        "updated_at": "2023-11-23T15:04:20.001280Z"
    }
]

# events = pd.DataFrame(Event.objects.get())
events = pd.DataFrame(event_json)

user_registrations = pd.DataFrame(registration_json, columns=['event', 'user_email'])
print(user_registrations)

# Create TF-IDF vectors for your event descriptions
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(events['description'])

# Compute the cosine similarity between all events
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# # Function to get recommendations based on a user profile
# def get_recommendations(user_id):
#     user_likes = user_profiles.loc[user_id, 'liked_events']
#     sim_scores = []
#
#     for event in user_likes:
#         # Get the index of the event that matches the title
#         idx = events.index[events['title'] == event].tolist()[0]
#
#         # Get the pairwsie similarity scores of all events with that event
#         sim_scores.extend(list(enumerate(cosine_sim[idx])))
#
#     # Sort the events based on the similarity scores
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#
#     # Get the scores of the 10 most similar events
#     sim_scores = sim_scores[1:11]
#
#     # Get the event indices
#     event_indices = [i[0] for i in sim_scores]
#
#     # Return the top 10 most similar events
#     return events['title'].iloc[event_indices]
