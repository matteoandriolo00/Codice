import requests
import sys

def get_coordinates(address):
    """
    Recupera le coordinate (latitudine e longitudine) di un indirizzo utilizzando il servizio Nominatim.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json"
    }
    headers = {"User-Agent": "PythonGeocoder/1.0"}
    response = requests.get(url, params=params, headers=headers)
    
    try:
        data = response.json()
    except Exception as e:
        print("Errore nella risposta di Nominatim:", e)
        return None
    
    if not data:
        return None

    # Utilizza il primo risultato
    lat = float(data[0]['lat'])
    lon = float(data[0]['lon'])
    return (lat, lon)

def get_driving_distance(coord1, coord2):
    """
    Calcola la distanza come strada tra due punti (coord1 e coord2) usando l'API di OSRM.
    Le coordinate devono essere fornite come tuple (latitudine, longitudine).
    """
    # OSRM richiede le coordinate nel formato: lon,lat
    url = f"http://router.project-osrm.org/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}"
    params = {"overview": "false"}
    response = requests.get(url, params=params)
    
    try:
        data = response.json()
    except Exception as e:
        print("Errore nella risposta di OSRM:", e)
        return None

    if data.get("code") != "Ok":
        return None

    # Prende la prima rotta
    route = data["routes"][0]
    # La distanza è in metri
    return route["distance"]

def dist(A,B):

    coordinates_A = get_coordinates(A)
    coordinates_B = get_coordinates(B)

    if coordinates_A and coordinates_B:
        distance_km = (get_driving_distance(coordinates_A, coordinates_B))/1000
        return distance_km
    else:
        distance_km = 1000
        return distance_km
