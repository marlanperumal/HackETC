from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import requests
from time import sleep
import json
import logging
import os
import dotenv

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

mode_icon = {
    "Bus": "🚌",
    "Walking": "🚶‍",
    "Rail": "🚉",
    "ShareTaxi": "🚐",
}

def get_wimt_token():
    CLIENT_ID = os.getenv("CLIENT_ID") 
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "transportapi:all"
    }

    r = requests.post( 'https://identity.whereismytransport.com/connect/token', data=payload)
    if r.status_code != 200:
        return None

    access_token = r.json()['access_token']
    return access_token

def get_wimt_route(start_point, end_point, retry=0, max_retries=2):
    global access_token
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

    logging.info(f"Getting route from {start_point} to {end_point}")
    r = requests.post("{ROOT}/journeys".format(ROOT=platformApiUrl), json=body, headers=headers)

    if r.status_code < 300:
        logging.info("Got route successfully")
        return r
    elif retry < max_retries:
        logging.info("Access token expired. Trying to get another one")
        access_token = get_wimt_token()
        logging.info("Trying to get route again")
        r = get_wimt_route(start_point, end_point, retry=retry+1)
        return r
    else:
        logging.info("Tried too many times. Giving up")
        return None
        

def build_route(start_point=[27.984117, -26.145339], end_point=[27.906734, -26.237348]):
    r = get_wimt_route(start_point, end_point)
    if r is None:
        return ["Oops! Something went wrong..."], []

    journey = r.json()
    itinerary = journey["itineraries"][0]
    legs = itinerary["legs"]
    num_legs = len(legs)
    start_reply = []
    directions = []
    start_reply.append("Start Route")
    start_reply.append(f"Legs: {num_legs}")

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

def get_coords_from_address(address):
    address = "+".join(address.split(" "))
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    country = "ZA"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}&components=country:{country}"
    response = requests.get(url)
    
    if response.status_code > 300 or response.json()["status"] != "OK":
        return None, None
    r = response.json()
    logging.info(r["status"])
    result = r["results"][0]
    formatted_address = result["formatted_address"]
    lng = result["geometry"]["location"]["lng"]
    lat = result["geometry"]["location"]["lat"]
    return formatted_address, [lng, lat]


@app.route("/message", methods=["POST"])
def parse_message():
    sleep(0.5)
    data = request.json
    message = data["message"]
    method = message.split()[0].lower()
    info = " ".join(message.split()[1:])
    response = {}
    logging.info(f"Received instruction {method} {info}")
    if method == "help":
        response = {
            "reply": [
                "This is just a demo so you have to be very specific for now",
                "Send a message starting with 'From' and then your origin, another message starting with 'To' and then your destination and then finally a third message saying 'Go'. Here's an example.",
                "From Cresta Mall",
                "To 23 Vilakazi Street",
                "Go"
            ]
        }
    elif method == "from":
        address, location = get_coords_from_address(info)
        if address is None:
            response = {
                "reply": ["I can't seem to find that address. Can you be more specific?"]
            }
        else:
            response = {
                "reply": [
                    f"Leaving from {address}"
                ],
                "origin_address": address,
                "origin_location": location
            }
    elif method == "to":
        address, location = get_coords_from_address(info)
        if address is None:
            response = {
                "reply": ["I can't seem to find that address. Can you be more specific?"]
            }
        else:
            response = {
                "reply": [
                    f"Going to {address}"
                ],
                "destination_address": address,
                "destination_location": location
            }
    elif method == "go":
        origin_address = data["origin_address"]
        origin_location = data["origin_location"]
        destination_address = data["destination_address"]
        destination_location = data["destination_location"]
        start_reply, legs = build_route(origin_location, destination_location)
        start_reply = [f"Route found from {origin_address} to {destination_address}"] + start_reply
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
            leg_directions = ["You're there!"]

        response = {
            "reply": leg_directions,
            "current_leg": current_leg
        }
    else:
        response = {
            "reply": ["Sorry I didn't understand that. Type \"Help\" to learn what I can do."] 
        }   

    return jsonify(response)

access_token = ""
print(access_token)
