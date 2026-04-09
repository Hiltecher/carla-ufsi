import carla, config, carla_engine, math, time, sys, csv, os
from datetime import datetime

def log_following_gap(speed_mph, prt, initial_gap, collision_occurred, final_gap):
    folder = 'results_data'
    if not os.path.exists(folder): os.makedirs(folder)
    path = os.path.join(folder, 'following_distance_results.csv')
    exists = os.path.isfile(path)
    with open(path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(['Timestamp', 'Speed_mph', 'PRT_s', 'Start_Gap_m', 'Collided', 'Final_Gap_m'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), speed_mph, prt, initial_gap, collision_occurred, round(final_gap, 2)])

def run_test(target_mph, prt_value):
    client, world = carla_engine.setup_simulation()
    actor_list = []; has_collided = False
    def collision_callback(event): nonlocal has_collided; has_collided = True

    try:
        bp = world.get_blueprint_library().find(config.VEHICLE_BP)
        hc_gap = config.HIGHWAY_CODE_DATA.get(int(target_mph), {}).get('total', 23)
        
        # FIXED: Both cars moved back by 100m to preserve the gap and provide stopping room
        lead_start_x = -100
        lead_car = world.spawn_actor(bp, carla.Transform(carla.Location(x=lead_start_x, y=-5, z=2), carla.Rotation(yaw=0)))
        ego_car = world.spawn_actor(bp, carla.Transform(carla.Location(x=lead_start_x - hc_gap, y=-5, z=2), carla.Rotation(yaw=0)))
        actor_list.extend([lead_car, ego_car])

        # CAMERA RELOCATION: Moves to the new starting area
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(ego_car.get_location() + carla.Location(x=-20, z=10), 
        carla.Rotation(pitch=-25, yaw=0)))

        # Collision Sensor
        col_sensor = world.spawn_actor(world.get_blueprint_library().find('sensor.other.collision'), carla.Transform(), attach_to=ego_car)
        col_sensor.listen(collision_callback); actor_list.append(col_sensor)

        # Acceleration
        for car in [lead_car, ego_car]: car.apply_control(carla.VehicleControl(throttle=1.0))
        while (math.sqrt(ego_car.get_velocity().x**2 + ego_car.get_velocity().y**2)) / config.MPH_TO_MS < target_mph:
            time.sleep(0.05)

        print(f"\n--- HAZARD EVENT: {target_mph} MPH | GAP: {hc_gap}M ---")
        lead_car.apply_control(carla.VehicleControl(brake=1.0, hand_brake=True))
        
        start_reaction = time.time()
        while (time.time() - start_reaction) < prt_value:
            dist = lead_car.get_location().distance(ego_car.get_location()) - 4.8
            print(f"REACTION PHASE: Time: {time.time()-start_reaction:.2f}s | Bumper Gap: {max(0, dist):.2f}m")
            if has_collided: break
            time.sleep(0.1)

        if not has_collided:
            print("!!! EGO BRAKES APPLIED !!!")
            ego_car.apply_control(carla.VehicleControl(brake=1.0, hand_brake=True))
            while not has_collided and (math.sqrt(ego_car.get_velocity().x**2 + ego_car.get_velocity().y**2)) > 0.1:
                time.sleep(0.05)

        final_dist = lead_car.get_location().distance(ego_car.get_location()) - 4.8
        status = "COLLISION" if has_collided else "SAFE"
        print(f"\n--- SAFETY REPORT: HAZARD FOLLOWING ---")
        print(f"Outcome: {status}")
        print(f"Final Bumper Gap: {max(0, final_dist):.2f}m")

        log_following_gap(target_mph, prt_value, hc_gap, has_collided, final_dist)
    finally:
        for actor in actor_list: actor.destroy()

if __name__ == "__main__":
    run_test(float(sys.argv[1]), float(sys.argv[2]))