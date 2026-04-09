import carla
import config
import carla_engine
import math
import time
import sys
import csv
import os
from datetime import datetime

def log_straight_line(speed_mph, prt, think_dist, brake_dist, total_dist, benchmark):
    """Saves test data to a specific CSV inside a results folder."""
    folder = 'results_data'
    if not os.path.exists(folder): os.makedirs(folder)
    path = os.path.join(folder, 'straight_line_results.csv')
    exists = os.path.isfile(path)
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(['Timestamp', 'Speed_mph', 'PRT_s', 'Think_m', 'Brake_m', 'Total_m', 'Official_m', 'Margin_m'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), speed_mph, prt, round(think_dist, 2), 
        round(brake_dist, 2), round(total_dist, 2), benchmark, round(benchmark - total_dist, 2)])

def run_test(target_mph, prt):
    client, world = carla_engine.setup_simulation()
    actor_list = []
    
    try:
        bp = world.get_blueprint_library().find(config.VEHICLE_BP)
        spawn_point = carla.Transform(carla.Location(x=-130, y=-5, z=2), carla.Rotation(yaw=0))
        vehicle = world.spawn_actor(bp, spawn_point)
        actor_list.append(vehicle)

        # --- CAMERA RELOCATION ---
        spectator = world.get_spectator()
        v_trans = vehicle.get_transform()
        # Teleports camera 15m behind and 8m above the car
        spectator.set_transform(carla.Transform(v_trans.location + carla.Location(x=-15, z=8), 
        carla.Rotation(pitch=-25, yaw=v_trans.rotation.yaw)))

        target_ms = target_mph * config.MPH_TO_MS
        official_benchmark = config.HIGHWAY_CODE_DATA.get(int(target_mph), {}).get('total', 0)

        vehicle.apply_control(carla.VehicleControl(throttle=1.0))
        while True:
            v = vehicle.get_velocity()
            if math.sqrt(v.x**2 + v.y**2 + v.z**2) >= target_ms: break
            time.sleep(0.05)

        think_start = vehicle.get_location()
        time.sleep(prt)
        think_end = vehicle.get_location()
        thinking_dist = think_start.distance(think_end)

        vehicle.apply_control(carla.VehicleControl(brake=1.0, hand_brake=True))
        brake_start = vehicle.get_location()
        while True:
            v = vehicle.get_velocity()
            if math.sqrt(v.x**2 + v.y**2 + v.z**2) < 0.1: break
            time.sleep(0.05)
            
        brake_end = vehicle.get_location()
        braking_dist = brake_start.distance(brake_end)
        total_sim_dist = thinking_dist + braking_dist

        margin = official_benchmark - total_sim_dist
        status = "PASS (SAFE)" if margin > 0 else "FAIL (DANGEROUS)"
        
        print(f"\n--- SAFETY REPORT: STRAIGHT LINE STOP ---")
        print(f"Outcome: {status}")
        print(f"Total Stop Dist: {total_sim_dist:.2f}m | Benchmark: {official_benchmark}m")
        print(f"Safety Margin: {margin:.2f}m")

        log_straight_line(target_mph, prt, thinking_dist, braking_dist, total_sim_dist, official_benchmark)

    finally:
        for actor in actor_list: actor.destroy()

if __name__ == "__main__":
    run_test(float(sys.argv[1]), float(sys.argv[2]))