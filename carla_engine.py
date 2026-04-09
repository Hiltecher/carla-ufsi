import carla
import config
import time

def setup_simulation():
    client = carla.Client(config.HOST, config.PORT)
    client.set_timeout(config.TIMEOUT)
    world = client.get_world()
    
    # Ensure we are on Town05
    if not world.get_map().name.endswith(config.MAP_NAME):
        world = client.load_world(config.MAP_NAME)
    
    # Cleanup logic
    for actor in world.get_actors().filter('vehicle.*'):
        actor.destroy()
    time.sleep(0.5)
    
    return client, world