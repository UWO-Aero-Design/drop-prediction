// I think something like this will work

const spawn = require("child_process").spawn;
const grep = spawn('grep', ['Drop_Algorithm.py', drop_item]);          //create python process


//Receiving from browser and sending to Python:
socket.on('messageFromBrowser', function(data) {
    py.stdin.setEncoding('utf-8');
    py.stdin.write(JSON.stringify(data.browser_value+'\n'));
    py.stdin.end();   //<--- Error happens here
});



// To receive data back from python
grep.stdout.on('data', (data) => {                          
    myjson = JSON.parse(data.toString());
    console.log(myjson.Response);
  });