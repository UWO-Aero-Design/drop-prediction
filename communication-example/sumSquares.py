import sys, json

last_timestep = 0

def get_Timestep(last_timestep):
    
    lines = sys.stdin.readline()
    while (lines == ""):
        lines = sys.stdin.readline()

    last_timestep = lines
    return last_timestep


#print("Output from Python")
#print("First Name: " + sys.argv[1])
#print("Last Name: " + sys.argv[2])
counter = sys.argv[3]
#print("Number of runs: " + counter)
counter = int(counter)

sum_of_squares = 0
for i in range(0, counter):
    last_timestep = get_Timestep(last_timestep)
    data = json.loads(last_timestep)
    data = int(data)
    sum_of_squares = sum_of_squares + (data ** 2)

response = {
        "First Name": sys.argv[1],
        "Last Name": sys.argv[2],
        "Sum of i Squares" : counter-1, 
        "Answer": sum_of_squares
    }

print(json.dumps(response), flush=True, end='')
