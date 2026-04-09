import carla
import config
import carla_engine
import math
import time
import sys
import csv
import os
from datetime import datetime

def log_motorway(speed_mph, prt, total_dist, ke_kj):
    """Saves high-speed motorway data to its own CSV file."""
    folder = 'results_data'
    if not os.path.exists(folder): 
        os.makedirs(folder)
    
    path = os.path.join(folder, 'motorway_results.csv')
    exists = os.path.isfile(path)
    
    with open(path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(['Timestamp', 'Speed_mph', 'PRT_s', 'Stop_Dist_m', 'Kinetic_Energy_KJ'])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            speed_mph, 
            prt, 
            round(total_dist, 2), 
            round(ke_kj, 2)
        ])

def run_test(target_mph, prt):
    client, world = carla_engine.setup_simulation()
    actor_list = []
    
    try:
        bp = world.get_blueprint_library().find(config.VEHICLE_BP)
        spawn_point = carla.Transform(carla.Location(x=-150, y=0, z=2), carla.Rotation(yaw=0))
        vehicle = world.spawn_actor(bp, spawn_point)
        actor_list.append(vehicle)
        
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(spawn_point.location + carla.Location(x=-15, z=8), 
        carla.Rotation(pitch=-25, yaw=0)))

        target_ms = target_mph * config.MPH_TO_MS
        vehicle.apply_control(carla.VehicleControl(throttle=1.0))
        
        while (math.sqrt(vehicle.get_velocity().x**2 + vehicle.get_velocity().y**2)) < target_ms:
            time.sleep(0.05)

        start_loc = vehicle.get_location()
        time.sleep(prt)
        vehicle.apply_control(carla.VehicleControl(brake=1.0, hand_brake=True))
        
        while (math.sqrt(vehicle.get_velocity().x**2 + vehicle.get_velocity().y**2)) > 0.1:
            time.sleep(0.05)
            
        total_dist = start_loc.distance(vehicle.get_location())
        
        # SCIENTIFIC CALCULATIONS
        mass = 1800 # Tesla Model 3 kg
        ke_j = 0.5 * mass * (target_ms**2)
        ke_kj = ke_j / 1000
        
        # Parallel 1: Energy vs 30mph (161kJ baseline)
        energy_multiple = ke_kj / 161
        
        # Parallel 2: Height of Fall Equivalency (h = E / mg)
        fall_height = ke_j / (mass * 9.81)

        print(f"\n--- MOTORWAY KINETIC ENERGY REPORT ---")
        print(f"Cruising Speed: {target_mph} mph ({target_ms:.2f} m/s)")
        print(f"Total Stop Distance: {total_dist:.2f} meters")
        print(f"Kinetic Energy: {ke_kj:.2f} kJ")
        print(f"------------------------------------------")
        print(f"REAL-WORLD PARALLELS:")
        print(f"1. This speed has {energy_multiple:.2f}x the lethal energy of a 30 mph impact.")
        print(f"2. Stopping this car is equivalent to catching an object falling from a {fall_height:.1f}m building.")
        print(f"3. Infrastructure at this speed must absorb {ke_kj:.2f} kJ to protect occupants.")
        print(f"------------------------------------------")

        log_motorway(target_mph, prt, total_dist, ke_kj)
    finally:
        for actor in actor_list: actor.destroy()

if __name__ == "__main__":
    run_test(float(sys.argv[1]), float(sys.argv[2]))