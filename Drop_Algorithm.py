"""
Must input the target gps coordinates
For the entire algorithm, North and East are positive, South and West are negative
"""
import math
import sys
import json
"""
    Surface Area is in m^2, and Mass is in kg
    Drag Coeffiecients estimated using SolidWorks
    Need to know the model of the water bottle or material to determine mass
"""
class waterBottle:
    def __init__(self):
        self.q = 0
        self.mass = 0.51091
        self.surface_Area = 0.03828028
        self.drag_coef_Values = {
            0:0.025,
            1:0.032,
            2:0.039,
            3:0.039,
            4:0.035,
            5:0.011,
            6:0.01,
            7:0.063,
            8:0.165,
            9:1
        }
        self.drag_Coef = self.drag_coef_Values[0]
    
    def calc_Drag_Coef(self, angle_of_attack):                                       # Calculates new drag coefficient and sets it
        angle_of_attack = angle_of_attack/10
        angle_of_attack = round(angle_of_attack)                                     # Performs a Bankers rounding
        self.drag_Coef = self.drag_coef_Values[angle_of_attack]

class nerf:
    def __init__(self):
        self.q = 0
        self.mass = 0.2902991
        self.surface_Area = 0.05693814
        self.drag_coef_Values = {
            0:0.012,
            1:0.016,
            2:0.016,
            3:0.017,
            4:0.027,
            5:0.037,
            6:0.078,
            7:0.046,
            8:0.3,
            9:1
        }
        self.drag_Coef = self.drag_coef_Values[0]
    
    def calc_Drag_Coef(self, angle_of_attack):                              # Calculates new drag coefficient and sets it
        angle_of_attack = angle_of_attack/10
        angle_of_attack = round(angle_of_attack)                            # Performs a Bankers rounding
        self.drag_Coef = self.drag_coef_Values[angle_of_attack]

class timeStep:
    def __init__(self):
        self.current = 0
        self.old = 0

    def getAltitude(self):
        # Insert code to take apart json for altitude
        return 0

    def getCoordinates(self):
        return 0, 0

    def getDensity(self):  
        return 0

    def getPlaneHeading(self):
        return 0

    def getPlaneSpeed(self):
        return 0

    def getWindHeading(self):
        return 0

    def getWindSpeed(self):
        return 0

def I_Need_New_Data(time_step):
    time_step.current = sys.stdin.read()                                                   # Hopefully
    while(time_step.current == time_step.old) or (time_step.current == []):
        time_step.current = sys.stdin.read()    
    time_step.old = time_step.current

def get_current_wind_Properties(time_step):
    wind_speed = time_step.getWindSpeed()                                     # Read in current wind speed
    wind_dir = time_step.getWindHeading()                                     # Read in wind direction (heading)
    cur_windspeed_x = wind_speed * math.sin(wind_dir)
    cur_windspeed_y = wind_speed * math.cos(wind_dir)
    return cur_windspeed_x, cur_windspeed_y                                 # Positive if wind is going North or East handled by sin and cos

def run_Simulation(item, time_step):
    # This loop simulates the drop to determine where the payload would land currently

    I_Need_New_Data(time_step)
    altitude = time_step.getAltitude()                                        # Read in current Height
    time_Total = 0                                                          # Time for drop completion
    wind_speed_x = 0
    wind_speed_y = 0

    disp_u = 0
    disp_z = 0
    vel_u = time_step.getPlaneSpeed()                                         # Velocity relative to ground, Need to read it in
    vel_z = 0                                                               # Velocity up or down (Change in height/altitude)

    t = 0.02                                                                # Time Interval
    g = 9.80665

    for i in range(0,3000,1):

        I_Need_New_Data(time_step)
        acc_u = -1 * (item.q/item.mass) * (vel_u**2)                               # Drag force in the x direction, will slow down the item over time
        acc_z =  g - (item.q/item.mass) * (vel_z**2)                               # Second part is drag force which acts upwards as the part falls down
        
        vel_u = vel_u + acc_u * t
        vel_z = vel_z + acc_z * t
        if vel_u  <= 0:
            vel_u = 0

        disp_u = disp_u + (vel_u * t) + (0.5 * (acc_u)*(t**2))
        disp_z = disp_z + (vel_z * t) + (0.5 * (acc_z)*(t**2))

        angle_of_attack = math.atan(vel_z/vel_u)                                # Gives the angle that the object is falling at
        current_drag_coef = item.drag_Coef                                      # Remember old drag coef
        item.calc_Drag_Coef(angle_of_attack)                                    # Calculate new drag coef
        item.q = (item.q/current_drag_coef) * item.drag_Coef                    # Update q

        time_Total = time_Total + t
        (cwx, cwy) = get_current_wind_Properties(time_step)
        wind_speed_x = wind_speed_x + cwx                                         
        wind_speed_y = wind_speed_y + cwy                                         

        if(disp_z >= altitude):
            wind_speed_x = wind_speed_x/i                                       # Average wind speed throughout the flight simulation in x and y
            wind_speed_y = wind_speed_y/i
            break 
    
    return wind_speed_x, wind_speed_y, disp_u, time_Total


def get_dir_from_Displacement(disp_x, disp_y):
    xdir = 0
    ydir = 0
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


def compute_Wind_Offset(plane_dir, wind_disp_x, wind_disp_y, release_Lat, release_Long, target_Lat, target_Long, theta, time_step):
    """
    Use the displacement caused by wind to adjust the release longitude and latitude
    Assuming x increase going towards the right(east) and y increases going forwards(north)
    Longitude and Latitude is assumed to be in North America
    Therefore Longitude increases going upwards (North or +y) and Latitude increase going West (Left or -x)

    These may be useful
    Length in meters of 1° of latitude = always 111.32 km
    Length in meters of 1° of longitude = 40075 km * cos( latitude ) / 360
    """

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


"""
drop_Item should be an integer 0, or 1 for the Water Bottle, or Fowler
"""
def calc_Drop(drop_Item):

    target_Lat = 0                                                                  # Somehow get these (Maybe add to function call?)
    target_Long = 0
    time_step = timeStep()

    I_Need_New_Data(time_step)
    air_Density = time_step.getDensity()                                            # Read in air density
    plane_dir = time_step.getPlaneHeading()                                         # Read in current heading, assume on same heading entire time

    if(drop_Item == 0):
        item = waterBottle()
        item.q = item.drag_Coef * item.surface_Area * air_Density/2
    else:
        item = nerf()
        item.q = item.drag_Coef * item.surface_Area * air_Density/2

    (avg_wind_Speed_x, avg_wind_Speed_y, dist_To_Target,
        sim_Time) = run_Simulation(item, time_step)

    # Find the actual drop location
    wind_disp_x = sim_Time * avg_wind_Speed_x                                       # How far in one direction the wind will add to the current displacement
    wind_disp_y = sim_Time * avg_wind_Speed_y                                       # We can do this within the run_simulation method
    
    I_Need_New_Data(time_step)
    current_Lat, current_Long = time_step.getCoordinates()                          # Read coordinates from GPS used for approximations                                                        

    theta = math.atan((target_Long - current_Long)/(target_Lat - target_Long))
    release_Lat = target_Lat - (dist_To_Target * math.sin(theta))                   # Apparently a great approximation
    release_Long = target_Long - (dist_To_Target * math.cos(theta))

    
    release_Lat, release_Long = compute_Wind_Offset(plane_dir, wind_disp_x, wind_disp_y,
        release_Lat, release_Long, target_Lat, target_Long, theta, time_step)

    response = {
        "heading": plane_dir,
        "release_Lat": release_Lat,
        "release_Long": release_Long
    }

    sys.stdout.write(json.dumps(response))
    sys.stdout.flush()


calc_Drop(sys.argv[1])                                                          # Actually begin the calculation