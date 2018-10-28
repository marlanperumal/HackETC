from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import requests
from time import sleep

app = Flask(__name__)
CORS(app)

mode_icon = {
    "Bus": "🚌",
    "Walking": "🚶‍",
    "Rail": "🚉",
    "ShareTaxi": "🚐",
}

def get_wimt_token():
     # http://docs.python-requests.org/

    # replace with your client information: developer.whereismytransport.com/clients
    CLIENT_ID = '43585646-3366-4440-9604-7b46a1724933' 
    CLIENT_SECRET = 'w1L3g4PXLlDznw8rFkCJaTQYi9Q16QwFW+BeEQ/6Wmw='

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "transportapi:all"
    }

    r = requests.post( 'https://identity.whereismytransport.com/connect/token', data=payload)
    if r.status_code != 200:
        raise Exception("Failed to get token")

    access_token = r.json()['access_token']
    return access_token

def get_wimt_route(start_point=[27.984117, -26.145339], end_point=[27.906734, -26.237348]):
    platformApiUrl = "https://platform.whereismytransport.com/api"

    headers = {
        "Authorization": "Bearer {access_token}".format(access_token=access_token),
        "Accept" : "application/json",
        "Content-Type" : "application/json"
    }
    body = {
        "geometry": {
            "type": "Multipoint",
            "coordinates": [
                start_point,
                end_point
            ]
        }
    }

    r = requests.post("{ROOT}/journeys".format(ROOT=platformApiUrl), json=body, headers=headers)
    print(r.status_code)
    journey = r.json()
    itinerary = journey["itineraries"][0]

    
    legs = itinerary["legs"]
    start_reply = []
    directions = []
    start_reply.append("Start Route")

    distance = itinerary["distance"]["value"]/1000
    duration = itinerary["duration"]
    duration_hours = duration // 3600
    duration_minutes = (duration - duration_hours*3600) // 60
    start_reply.append("Distance: {} km".format(distance))
    start_reply.append("Duration: {} hours {} minutes".format(duration_hours, duration_minutes))
    start_reply.append("Type \"Next\" for the next step")

    for i_leg, leg in enumerate(legs):
        this_leg = []
        
        this_leg.append("Start Leg {}".format(i_leg + 1))
        mode = leg["type"]
        
        if mode == "Transit":
            mode = leg["line"]["mode"]
        this_leg.append("Transport mode: {} {}".format(mode, mode_icon[mode]))
        if mode == "Walking":
            for direction in leg["directions"]:
                this_leg.append(direction["instruction"] + 
                                " for {} {}".format(direction["distance"]["value"],
                                                    direction["distance"]["unit"]))
        elif mode == "Bus":
            line = leg["line"]
            this_leg.append("Go to the {} bus stop".format(leg["vehicle"]["headsign"]))
            this_leg.append(
                "Take the {} bus {}"\
                .format(line["agency"]["name"], line["name"]))
            this_leg.append("Get off after {} stops".format(len(leg["waypoints"])-1))
        elif mode == "ShareTaxi":
            line = leg["line"]
            this_leg.append("Go to the {} taxi rank".format(leg["vehicle"]["headsign"]))
            this_leg.append(
                "Take the {} taxi {}"\
                .format(line["agency"]["name"], line["name"]))
            this_leg.append("Get off after {} stops".format(len(leg["waypoints"])-1))
        elif mode == "Rail":
            line = leg["line"]
            this_leg.append("Go to the {} train station".format(leg["vehicle"]["headsign"]))
            this_leg.append(
                "Take the {} train {}"\
                .format(line["agency"]["name"], line["name"]))
            this_leg.append("Get off after {} stops".format(len(leg["waypoints"])-1))
        directions.append(this_leg)
    
    return start_reply, directions


@app.route("/message", methods=["POST"])
def parse_message():
    sleep(0.5)
    data = request.json
    message = data["message"]
    method = message.split()[0].lower()
    info = " ".join(message.split()[1:])
    response = {}
    if method == "help":
        response = {
            "reply": ["This is just a demo so type \"Go\" to get a route from Cresta Mall to 23 Vilakazi Street"]
        }
    elif method == "go":
        start_reply, legs = get_wimt_route()
        response = {
            "reply": start_reply,
            "legs": legs,
            "current_leg": 0
        }
    elif method == "new":
        pass
    elif "thank" in method:
        response = {
            "reply": ["You're welcome 😊"]
        }
    elif method == "next":
        num_legs = len(data["legs"])
        current_leg = int(data["current_leg"])
        if current_leg < num_legs:
            leg_directions = data["legs"][current_leg]
            current_leg += 1
        else:
            leg_directions = ["End Route"]

        response = {
            "reply": leg_directions,
            "current_leg": current_leg
        }
    else:
        response = {
            "reply": ["Sorry I didn't understand that. Type \"Help\" to learn what I can do."] 
        }   

    return jsonify(response)

# access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjkwODQ2MkI2MDVEM0NCNEVDQzQ1RDYyMjQwNDMwOTZGODBENjQ2QzMiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJrSVJpdGdYVHkwN01SZFlpUUVNSmI0RFdSc00ifQ.eyJuYmYiOjE1NDA3MTQ5NTMsImV4cCI6MTU0MDcxODU1MywiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS53aGVyZWlzbXl0cmFuc3BvcnQuY29tIiwiYXVkIjoiaHR0cHM6Ly9pZGVudGl0eS53aGVyZWlzbXl0cmFuc3BvcnQuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjQzNTg1NjQ2LTMzNjYtNDQ0MC05NjA0LTdiNDZhMTcyNDkzMyIsImNsaWVudF90ZW5hbnQiOiIwM2QyZGUyOS03MTRjLTRhMjktYWVmMi05MTBmN2Y3ZmFiMmYiLCJqdGkiOiJmNWFkMWEwMzg1MzU1MjA4YTA2ODMyZGVmYmQyMTQ2NCIsInNjb3BlIjpbInRyYW5zcG9ydGFwaTphbGwiXX0.IyWEOBV2jJuZZTNlqkylZx9dPeVKxGVfCOZwFZNxAhAnXgqXxhp0hSGc1-DSezuYDzfnDJ9k8Mjd1QPjxK5I9PmL6Pr0zSIraJopOzNHSql5CnCg_fwJCtz9ZtuF6H82423fUiR31KRn_PTWiEjpXaN5Dp5twRBuv5klAPecstoqoHH_oXnyaZDN6VtLuuYGDxbUkiTMBSKyn8reZAP2cFx1PWe1EvN9hmEJhVMQCiI0fElc2aq8TdMeJTo7U-cqZIg6Pb79UzEWw562Xsl1BbrP9zL6IjrEA28McqnH-E-Jkuqn9sQleG-UYOs_7m7f7_Eu61sFUTU8pafkDeM08g"
access_token = get_wimt_token()
print(access_token)