'''

    Ignore this for now. Thinking out loud in the comments:
    
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

from collections import namedtuple
import math

# Takes in three namedtuples
def colinear(a, b, c):
    '''
        Colinear if area of a triangle formed by these 3 points is 0
    '''
    colinear = a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)

    if colinear == 0:
        return True
    else:
        return False

def direction(a, b, c):
    '''
        Given a,b,c cartesian coordinates. Return the direction that we must turn currently to head towards the target 
        Works by calculating the angle between the current location b and the midpoint of the line between target c and prev location a
    '''

    mid_x = (a.x + c.x) / 2
    mid_y = (a.y + c.y) / 2

    theta = math.atan2( (mid_y - b.y), (mid_x - b.x) )
    theta2 = math.atan2( (c.y - a.y), (c.x - a.x) )

    print((mid_x, mid_y), theta, theta2)
    
    # Hahahaha figure this one out
    if colinear(a,b,c):
        return "Straight"
    elif theta*theta2 + theta2 < 0:
        return "Left"
    elif theta*theta2 + theta2  > 0:
        return "Right"
    else:
        return None

def main():
    Coord = namedtuple('Coord', 'x y')

    prev   = Coord( 1, 1 )
    curr   = Coord( -2, 7)
    target = Coord( 3, -3 )

    print( colinear( prev, curr, target ) )

    prev   = Coord( 1, -1 )
    curr   = Coord( 6, 4)
    target = Coord( 4, 2 )

    print( colinear( prev, curr, target ) )

    target   = Coord( -1, 1 )
    curr   = Coord( -4, 3 )
    prev = Coord( -5, 5 )

    print( colinear( prev, curr, target ) )
    print( direction( prev, curr, target ) )

if __name__ == "__main__":
    main()