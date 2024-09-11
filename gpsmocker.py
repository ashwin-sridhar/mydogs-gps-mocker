import time
import random
import json
import websocket
import _thread as thread
import math

# Earth's radius in meters
EARTH_RADIUS = 6371000

def generate_initial_gps_data():
    return {
        "type": "gps_data",
        "timestamp": time.time(),
        "latitude": random.uniform(-90, 90),
        "longitude": random.uniform(-180, 180)
    }

def calculate_new_position(lat, lon, distance, bearing):
    """Calculate new position given distance and bearing."""
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    angular_distance = distance / EARTH_RADIUS

    lat2 = math.asin(
        math.sin(lat1) * math.cos(angular_distance) +
        math.cos(lat1) * math.sin(angular_distance) * math.cos(bearing)
    )

    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(angular_distance) * math.cos(lat1),
        math.cos(angular_distance) - math.sin(lat1) * math.sin(lat2)
    )

    return math.degrees(lat2), math.degrees(lon2)

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")

def on_open(ws):
    def run(*args):
        # Generate initial GPS data
        gps_data = generate_initial_gps_data()
        
        while True:
            ws.send(json.dumps(gps_data))
            print(f"Sent GPS data: {gps_data}")
            
            # Calculate new position (500 meters in a random direction)
            bearing = math.radians(random.uniform(0, 360))
            new_lat, new_lon = calculate_new_position(
                gps_data["latitude"], 
                gps_data["longitude"], 
                500, 
                bearing
            )
            
            # Update GPS data
            gps_data["latitude"] = new_lat
            gps_data["longitude"] = new_lon
            gps_data["timestamp"] = time.time()
            
            time.sleep(30)  # Wait for 30 seconds before sending the next data point

    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:4000",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.run_forever()
