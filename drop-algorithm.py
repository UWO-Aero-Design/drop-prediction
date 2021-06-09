"""
Must input the target gps coordinates
North (Up) and East (Right) are positive
South (Down) and West (Left) are negative
"""
import math
import sys
import json


# Class to define the waterbottle being dropped from the plane
class waterBottle:
    def __init__(self):
        self.q = 0
        self.mass = 0.51091                 # Surface Area is in m^2 
        self.surface_Area = 0.03828028      # Mass is in kg
        self.drag_coef_Values = {
            0:0.025, 1:0.032, 2:0.039, 3:0.039,
            4:0.035, 5:0.011, 6:0.01, 7:0.063,
            8:0.165, 9:1
        }
        self.drag_Coef = self.drag_coef_Values[0]
    
    # Calculates new drag coefficient and sets it
    def calc_Drag_Coef(self, angle_of_attack):                                       
        angle_of_attack = angle_of_attack/10
        angle_of_attack = round(angle_of_attack)
        self.drag_Coef = self.drag_coef_Values[angle_of_attack]


# Class to define the nerf football being dropped from the plane
class nerf:
    def __init__(self):
        self.q = 0
        self.mass = 0.2902991               # Surface Area is in m^2 
        self.surface_Area = 0.05693814      # Mass is in kg
        self.drag_coef_Values = {
            0:0.012, 1:0.016, 2:0.016, 3:0.017,
            4:0.027, 5:0.037, 6:0.078, 7:0.046,
            8:0.3, 9:1
        }
        self.drag_Coef = self.drag_coef_Values[0]
    
    # Calculates new drag coefficient and sets it
    def calc_Drag_Coef(self, angle_of_attack):                              
        angle_of_attack = angle_of_attack/10
        angle_of_attack = round(angle_of_attack)
        self.drag_Coef = self.drag_coef_Values[angle_of_attack]


# This class holds a copy of the most recent data sent from the plane
# Current is the most recently receieved data through stdin (Held as a json)
# Each method will disect the json for its specific data
class timeStep:
    def __init__(self):
        self.current = 0

    def getAltitude(self):
        return self.current.altitude

    def getCoordinates(self):
        return self.current.coordinates

    def getDensity(self):  
        return self.current.density

    def getPlaneHeading(self):
        return self.current.planeheading

    def getPlaneSpeed(self):
        return self.current.planespeed

    def getWindHeading(self):
        return self.current.windheading

    def getWindSpeed(self):
        return self.current.windspeed


# This function waits for new data in the form of a JSON through stdin
# It loops untill new data is recieved
def I_Need_New_Data(time_step):
    lines = sys.stdin.readline()
    while(lines == ""):
        lines = sys.stdin.readline()
    time_step.current = json.loads(lines)


def get_dir_from_Displacement(disp_x, disp_y):
    xdir = ydir = 0
    if(disp_x > 0):
        xdir = "east"
    else:
        xdir = "west"
    if(disp_y > 0):
        ydir = "north"
    else:
        ydir = "south"
    return xdir, ydir

def get_dir_from_Heading(heading):   
    if (heading >= 0) and (heading <= 90):
        return "east", "north"
    if (heading >= 90) and (heading <= 180):
        return "east", "south"
    if (heading >= 180) and (heading <= 270):
        return "west", "south"
    if (heading >= 270) and (heading <= 360):
        return "west", "north"

# Function that gets the current wind properties for the drop algorithm loop
def get_current_wind_Properties(time_step):
    wind_speed = time_step.getWindSpeed()
    wind_dir = time_step.getWindHeading()
    cur_windspeed_x = wind_speed * math.sin(wind_dir)
    cur_windspeed_y = wind_speed * math.cos(wind_dir)
    return cur_windspeed_x, cur_windspeed_y


"""
    Use the displacement caused by wind to adjust the release longitude and latitude
    Assuming x increase going towards the right(east) and y increases going forwards(north)
    Longitude and Latitude is assumed to be in North America
    Therefore Longitude increases going upwards (North or +y) and Latitude increase going West (Left or -x)

    These may be useful
    Length in meters of 1° of latitude = always 111.32 km
    Length in meters of 1° of longitude = 40075 km * cos( latitude ) / 360
"""
def compute_Wind_Offset(plane_dir, wind_disp_x, wind_disp_y, release_Lat, release_Long, target_Lat, target_Long, theta, time_step):

    plane_direction_x, plane_direction_y = get_dir_from_Heading(plane_dir)
    wind_direction_x, wind_direction_y = get_dir_from_Displacement(wind_disp_x, wind_disp_y)

    if (wind_direction_x == plane_direction_x) and (release_Lat <= target_Lat):         # Plane approaches from the right and is moving in -x
        release_Lat = release_Lat - wind_disp_x * math.sin(theta)                       # Shift release point further right

    if (wind_direction_x == plane_direction_x) and (release_Lat >= target_Lat):         # Plane approaches from the left and is moving in +x
        release_Lat = release_Lat + wind_disp_x * math.sin(theta)                       # Shift release point further left

    if (wind_direction_x != plane_direction_x) and (release_Lat <= target_Lat):         # Plane approaches from the right and is moving in -x
        release_Lat = release_Lat + wind_disp_x * math.sin(theta)                       # Shift release point to the left (Towards target)

    if (wind_direction_x != plane_direction_x) and (release_Lat >= target_Lat):         # Plane approaches from the left and is moving in +x
        release_Lat = release_Lat - wind_disp_x * math.sin(theta)                       # Shift release point to the right (Towards target)
    
    if (wind_direction_y == plane_direction_y) and (release_Long <= target_Long):       # Plane approaches from the bottom and is moving in +y
        release_Long = release_Long - wind_disp_y * math.cos(theta)                     # Shift release point away from target (Downwards)

    if (wind_direction_y == plane_direction_y) and (release_Long >= target_Long):       # Plane approaches from the top and is moving in -y
        release_Long = release_Long + wind_disp_y * math.cos(theta)                     # Shift release point away from target (Upwards)

    if (wind_direction_y != plane_direction_y) and (release_Long <= target_Long):       # Plane approaches from the bottom and is moving in +y
        release_Long = release_Long + wind_disp_y * math.cos(theta)                     # Shift release point towards target (Upwards)

    if (wind_direction_y != plane_direction_y) and (release_Long >= target_Long):       # Plane approaches from the top and is moving in -y
        release_Long = release_Long - wind_disp_y * math.cos(theta)                     # Shift release point towards target (Downwards)

    return release_Lat, release_Long



# This loop simulates the drop to determine where the payload would land currently
# x and y are from perspective of the ground (Forward, Backwards, Left, and Right)
# z is with respect to height
def run_Simulation(item, time_step):
    
    # Wait for updated telemetry readings
    I_Need_New_Data(time_step)
    altitude = time_step.getAltitude()
    vel_u = time_step.getPlaneSpeed()
    
    # Defining initial conditions
    time_Total = 0                                                  # Time for drop completion
    wind_speed_x = wind_speed_y = 0
    disp_u = disp_z = vel_z =0  
    t = 0.02                                                        # Time Interval
    g = 9.80665

    for i in range(0, 3000, 1):

        # Only get new data every 5 loops 
        # (depends on how often it will be sent)
        if (i % 5 == 0):
            I_Need_New_Data(time_step)
        
        # Update accelerations
        acc_u = -1 * (item.q/item.mass) * (vel_u**2)                # Drag force in the x direction, will slow down the item over time
        acc_z =  g - (item.q/item.mass) * (vel_z**2)                # Second part is drag force which acts upwards as the part falls down    
        
        # Update Velocities
        vel_u = vel_u + acc_u * t
        vel_z = vel_z + acc_z * t
        # Makes sure velocity in x direction is never backwards
        if vel_u  <= 0:
            vel_u = 0
        
        # Update Displacements
        disp_u = disp_u + (vel_u * t) + (0.5 * (acc_u)*(t**2))
        disp_z = disp_z + (vel_z * t) + (0.5 * (acc_z)*(t**2))

        # Find updated q and drag coeffiecients
        angle_of_attack = math.atan(vel_z/vel_u)                    # Gives the angle that the object is falling at
        old_drag_coef = item.drag_Coef                              # Remember old drag coef
        item.calc_Drag_Coef(angle_of_attack)                        # Calculate new drag coef (Updates item.drag_Coef)
        item.q = (item.q/old_drag_coef) * item.drag_Coef            # Update q

        # Update timekeeper, wind properties, and total affect of wind
        time_Total = time_Total + t
        # Due to constraint at beginning, gets new values every 5 iterations.
        cwx, cwy = get_current_wind_Properties(time_step)
        wind_speed_x = wind_speed_x + cwx                           # Accumulated wind speed                               
        wind_speed_y = wind_speed_y + cwy                                         
        avg_wind_speed_x = wind_speed_x/i
        avg_wind_speed_y = wind_speed_y/i
        
        if(disp_z >= altitude):
            break 
    
    return avg_wind_speed_x, avg_wind_speed_y, disp_u, time_Total


# Begin Drop Algorithm
drop_Item = int(sys.argv[1])
target_Lat = sys.argv[2]            # Need to figure out how lat and long should be interpreted (int, double etc)
target_Long = sys.argv[3]

# Create timeStep object to hold telemetry
time_step = timeStep()
# Get first telemetry readings
I_Need_New_Data(time_step)

# Read in air density and heading, these are assumed to be unchanged for the
# duration of the algorithm
air_Density = time_step.getDensity()
plane_dir = time_step.getPlaneHeading()

if(drop_Item == 0):
    item = waterBottle()
    item.q = item.drag_Coef * item.surface_Area * air_Density/2
else:
    item = nerf()
    item.q = item.drag_Coef * item.surface_Area * air_Density/2

# Start the actual simulation
(avg_wind_Speed_x, avg_wind_Speed_y,
     dist_To_Target, sim_Time) = run_Simulation(item, time_step)

# How far in one direction the wind will add to the current displacement
wind_disp_x = sim_Time * avg_wind_Speed_x         
wind_disp_y = sim_Time * avg_wind_Speed_y

# Read coordinates from GPS used for approximations
I_Need_New_Data(time_step)
current_Lat, current_Long = time_step.getCoordinates()

# Approximates drop coordinates (Before wind is accounted for)
theta = math.atan((target_Long - current_Long)/(target_Lat - target_Long))
release_Lat = target_Lat - (dist_To_Target * math.sin(theta))
release_Long = target_Long - (dist_To_Target * math.cos(theta))

# Find drop coordinates while accounting for wind
release_Lat, release_Long = compute_Wind_Offset(
    plane_dir, wind_disp_x,  wind_disp_y,  release_Lat, 
    release_Long, target_Lat, target_Long, theta
)

response = {
        "heading": plane_dir,
        "release_Lat": release_Lat,
        "release_Long": release_Long
    }

print(json.dumps(response), flush=True, end='')