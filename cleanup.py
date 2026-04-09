import carla

def main():
    try:
        # connect to the client
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()

        # 1. destroy all vehicles
        actors = world.get_actors()
        vehicles = actors.filter('vehicle.*')
        
        count = 0
        for vehicle in vehicles:
            vehicle.destroy()
            count += 1
        
        print(f"Cleaned up {count} vehicles.")

        # 2. reset spectator
        # resets to a standard starting position so I am not stuck top-down
        spectator = world.get_spectator()
        spawn_points = world.get_map().get_spawn_points()
        if spawn_points:
            # pick the first spawn point as a neutral starting view
            neutral_transform = spawn_points[0].transform
            # lift the camera up slightly to look down at the road
            neutral_transform.location.z += 5 
            neutral_transform.rotation.pitch = -30
            spectator.set_transform(neutral_transform)
            print("Spectator camera reset.")

    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    main()