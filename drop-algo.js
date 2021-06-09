
// Call this function to spawn and start the drop algorithm process
function spawnDrop(){
    // The variables to send to the drop algo at the very beginning
    // Some how set these variables
    var targetLat = 0
    var targetLong = 0
    var dropItem = 0

    // Start the algorithm and give it some arguments
    var spawn = require("child_process").spawn;
    var myDropAlgo = spawn('python', ["./drop-algorithm.py", targetLat, targetLong, dropItem]);
}

// Call this function to send updated data to the drop algorithm
function sendSensorData (data){
    sensorData = JSON.stringify(data)
    myDropAlgo.stdin.write(sensorData +'\n');
}

// Intercepts whatever python outputs and displays it
myDropAlgo.stdout.on('data', data => {
    data = JSON.parse(data)
    console.log(data);
});

// If there is an error with the python code
myDropAlgo.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

myDropAlgo.on('error', (error) => {
    console.error(`error: ${error.message}`);
});

// When the python code is done running this will let us know
myDropAlgo.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
});