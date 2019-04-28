'''
    The goal of this algorithm is to direct the pilot to line the plane up with the target
    In order to line up the plane with the target, we attempt to make three data points colinear
    The three data points will be [last_position, current_position, target_position]
    We will assume small area for map projection purposes, this means we can use a simple equirectangular projection
    
    Reference: http://wuciawe.github.io/transform/2014/09/30/simple-convertion-from-longitude,-latitude-to-x,-y-in-small-area.html
    
    lat, lon in radians
    r is the Earth radius in kilometres

    x = r * long * cos ( average latitudes ) 
    y = r * latitudes

    According to source, error in the scope of 10's kms in barely 1% 

    What should happen with the colinearity algorithm should be:

        Replace our current 

        heading ( current, previous) == heading( target, current)

        Solve for current and compare it to the actull current direction to give which direction we need to turn in order to correct
'''