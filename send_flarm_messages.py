#!/usr/bin/env python3

import asyncio
import random
from mavsdk import System
from mavsdk.transponder import AdsbVehicle, AdsbEmitterType

def generate_nearby_position(latitude, longitude, distance_in_meters=100):
    # Convert distance in meters to an approximate angular distance
    angular_distance = distance_in_meters / 111320

    # Generate random position within the specified range
    nearby_latitude = latitude + random.uniform(-angular_distance, angular_distance)
    nearby_longitude = longitude + random.uniform(-angular_distance, angular_distance)

    return nearby_latitude, nearby_longitude

async def send_flarm_message(drone, latitude, longitude):
    while True:
        # Generate random FLARM data
        latitude_deg, longitude_deg = generate_nearby_position(latitude, longitude)
        absolute_altitude_m = generate_random_altitude()
        velocity_north_m_s = generate_random_velocity()
        velocity_east_m_s = generate_random_velocity()
        velocity_down_m_s = generate_random_velocity()
        squawk = random.randint(1000, 7777)  # Generate a random squawk code

        print(f"Generated FLARM data: Latitude: {latitude_deg}, Longitude: {longitude_deg}, Altitude: {absolute_altitude_m}, Velocity North: {velocity_north_m_s}, Velocity East: {velocity_east_m_s}, Velocity Down: {velocity_down_m_s}")

        # Create the FLARM message
        adsb_vehicle = AdsbVehicle(
            icao_address=1,
            latitude_deg=latitude_deg,
            longitude_deg=longitude_deg,
            absolute_altitude_m=absolute_altitude_m,
            heading_deg=0.0,
            horizontal_velocity_m_s=velocity_north_m_s,
            vertical_velocity_m_s=velocity_down_m_s,
            callsign="test",
            emitter_type=AdsbEmitterType.NO_INFO,
            squawk=squawk,
            tslc_s=0
        )

        print(f"Generated FLARM message: {adsb_vehicle}")

        # Sleep for 1 second
        await asyncio.sleep(1)

def generate_random_altitude():
    # Generate random altitude value
    value = random.uniform(0.0, 1000.0)
    print(f"Generated random altitude: {value}")
    return value

def generate_random_velocity():
    # Generate random velocity value
    value = random.uniform(-10.0, 10.0)
    print(f"Generated random velocity: {value}")
    return value

async def main():
    # Create the drone object
    drone = System()

    # Connect to the drone
    await drone.connect(system_address="udp://:14540")
    print("Connected to drone")

    # Specify latitude and longitude
    latitude = 47.3977
    longitude = 8.5456

    # Set the transponder update rate
    await drone.transponder.set_rate_transponder(1)  # Set the rate to 1 Hz

    # Start sending FLARM messages
    await send_flarm_message(drone, latitude, longitude)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
