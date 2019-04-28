'''
    The drop algorithm assumes that we are perfectly headed towards the 

    Therefore, as a groundstation control member, we require both a drop algorithm and a method for lining up the plane with the target

    http://ijiet.com/wp-content/uploads/2017/01/5711.pdf
'''

import time
import math

class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

# Keep track of projectile properties prior to drop
class Projectile():
    # Temperature in Kelvin, Air pressure in PA=a
    def __init__(self, air_temperature, air_pressure, drag_coef, surface_area, mass, i_vel, i_alt, i_ws):

        gas_constant = 287.07

        self.air_density  = air_temperature / ( gas_constant * air_pressure )
        self.drag_coef    = drag_coef
        self.surface_area = surface_area
        self.mass = mass
        
        self.velocity     = i_vel # Can be estimated using IMU
        self.altitude     = i_alt # Can be estimated using Barometer 
        self.wind_speed   = i_ws  # Can be estimated using Pitot tube

    def _drag_force(self):
        '''
            Return drag force
        '''
        return (0.5) * self.air_density * self.drag_coef * self.surface_area

    def drag_mass_ratio(self):
        return ( ( self._drag_force() ) / self.mass )

# Compare accuracy of range based on time_step and iterations
def ProjectileRange(time_step, iterations, projectile):
    gravity = 9.806
    x,y = 0,1

    elapsed = 0

    # Initial kinematic states
    acc  = [0, 0]
    vel  = [projectile.velocity, 0]
    disp = [0, projectile.altitude]

    while iterations:
        # Calculate x and y acceleration based on velocity, drag, and mass
        acc[x] = -1 * projectile.drag_mass_ratio() * ( vel[x]**2 )
        acc[y] = gravity - ( projectile.drag_mass_ratio() * ( vel[y]**2 ) ) 

        # Update velocity based on acceleration
        vel[x] = vel[x] + ( acc[x] * time_step )
        vel[y] = vel[y] + ( acc[y] * time_step )

        # Update displacement
        disp[x] = disp[x] + ( vel[x] * time_step ) + ( 0.5 * acc[x] * (time_step**2) )
        disp[y] = disp[y] - ( vel[y] * time_step ) + ( 0.5 * acc[y] * (time_step**2) )

        # Update elapsed time
        elapsed += time_step

        # Update displacement
        iterations -= 1

        # Projectile range is determined when y-displacement equals or drops below 0
        if disp[y] <= 0:
            print('Projectile landed')
            return disp[x], elapsed, iterations

    raise Exception('Failed to reach altitude of 0. Modify initial projectile parameters or increase iterations') 

# Returns predicted ideal drop lat/lon based on current coordinates, target coordinates, and the range of the projectile
def DropCoordinates(current, target, range_value):
    # Range in kilometres
    delta_lat_rad =  math.radians( (target.lat - current.lat) )
    delta_lon_rad =  math.radians( (target.lon - current.lon) )

    print(delta_lat_rad, delta_lon_rad)

    theta = math.atan2( delta_lon_rad, delta_lat_rad )

    release_lat = ( target.lat - ( range_value * math.sin(theta) ) ) 
    release_lon = ( target.lon - ( range_value * math.cos(theta) ) ) 
 
    print(release_lat, release_lon)

    return Coordinate( release_lat, release_lon )

def CtoKelvin(c):
    return c + 273.15

def kPatoPa(kPa):
    return kPa*1000

def main():
    print('Projectile test')

    projectile = Projectile( 
                                air_temperature = CtoKelvin( 20 ), air_pressure = kPatoPa( 101.1 ), drag_coef = 1,
                                surface_area = 1,  mass = 0.250, 
                                i_vel = 15, i_alt = 100, i_ws = 5
                           )
    start = time.time()
    iterations = 3000
    results = ProjectileRange( 0.02, iterations, projectile ) 
    end = time.time()

    print('Range test. Range %f metres, Time %f seconds, Iterations %d, Running time %f milliseconds' % (results[0], results[1], (iterations - results[2]), (end-start) * 1000))

    # With the range in mind, we can approximate our lat/lon coordinates to x,y coordinates. Then abs(target.x - current.x) then we see the difference between our current predicted range and the distance between. Predicted
    # drop location is abs(target.x - current.x) - range

if __name__ == "__main__":
    main()





