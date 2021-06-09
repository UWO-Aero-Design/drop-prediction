var x1 = "Aero";
var x2 = "Design";
var i;
var k = 10;

// Start the python process and give it some arguments
var spawn = require("child_process").spawn;
var process = spawn('python', ["./sumSquares.py", x1, x2, k]);

for (i = 0; i < k; i++){
    sendPython(i);
}

function sendPython (i){
    console.log("Sent " + i + " to python");
    process.stdin.write(JSON.stringify(i) +'\n');
}

// Intercepts whatever python outputs and displays it
process.stdout.on('data', data => {
    data = JSON.parse(data)
    console.log(data);
});

// If there is an error with the python code
process.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

process.on('error', (error) => {
    console.error(`error: ${error.message}`);
});

// When the python code is done running this will let us know
process.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
});