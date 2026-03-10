import json
import folium
import requests
import os
from dotenv import load_dotenv
from geopy import distance


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance_gap(distance):
    return distance['distance']


def get_cafe_list(user_location):
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        cafes_list_raw = my_file.read()

        cafes_full_info = json.loads(cafes_list_raw)

    cafes_near = []

    for i in range(len(cafes_full_info)):
        picked_values = {
            'title': cafes_full_info[i]['Name'],
            'distance': 'None',
            'latitude': cafes_full_info[i]['Latitude_WGS84'],
            'longitude': cafes_full_info[i]['Longitude_WGS84'],
        }
        cafes_near.append(picked_values)

    for g in range(len(cafes_near)):
        coords = cafes_near[g]['latitude'], cafes_near[g]['longitude']
        cafes_near[g]['distance'] = distance.distance(user_location, coords).km

    return cafes_near


def pick_several_cafes(first):
    a = sorted(first, key=get_distance_gap)
    return a[:5]


def add_markers(user_location, second):
    m = folium.Map([user_location[0], user_location[1]], zoom_start=12)

    folium.Marker(
        location=[user_location[0], user_location[1]],
        tooltip="Click me!",
        popup="I am here",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    folium.Marker(
        location=[second[0]['latitude'], second[0]['longitude']],
        tooltip="Click me!",
        popup=second[0]['title'],
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        location=[second[1]['latitude'], second[1]['longitude']],
        tooltip="Click me!",
        popup=second[1]['title'],
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        location=[second[2]['latitude'], second[2]['longitude']],
        tooltip="Click me!",
        popup=second[2]['title'],
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        location=[second[3]['latitude'], second[3]['longitude']],
        tooltip="Click me!",
        popup=second[3]['title'],
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        location=[second[4]['latitude'], second[4]['longitude']],
        tooltip="Click me!",
        popup=second[4]['title'],
        icon=folium.Icon(color="green"),
    ).add_to(m)

    m.save("index.html")
    return m


def main():

    load_dotenv()

    apikey = os.getenv('YA_API_KEY')

    coords = fetch_coordinates(apikey, input('Введите местоположение: '))
    user_location = coords[::-1]

    first_step = get_cafe_list(user_location)

    second = pick_several_cafes(first_step)

    add_markers(user_location, second)


if __name__ == '__main__':
    main()
