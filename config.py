import carla

# Server Connection
HOST = 'localhost'
PORT = 2000
TIMEOUT = 10.0

# Simulation Settings
MAP_NAME = 'Town05'
VEHICLE_BP = 'vehicle.tesla.model3' # Reliable physics for braking

# Conversion factor
MPH_TO_MS = 0.44704 

# UK Highway Code Constants (Speed in mph : distances in meters)
# Official benchmarks (20-70) and Extrapolated (80-100)
HIGHWAY_CODE_DATA = {
    20:  {"thinking": 6,  "braking": 6,   "total": 12},
    30:  {"thinking": 9,  "braking": 14,  "total": 23},
    40:  {"thinking": 12, "braking": 24,  "total": 36},
    50:  {"thinking": 15, "braking": 38,  "total": 53},
    60:  {"thinking": 18, "braking": 55,  "total": 73},
    70:  {"thinking": 21, "braking": 75,  "total": 96},
}