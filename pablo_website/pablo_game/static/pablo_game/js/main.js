

var element1 = document.getElementById("human-card-1");
var element2 = document.getElementById("human-card-2");
var element3 = document.getElementById("human-card-3");
var element4 = document.getElementById("human-card-4");

console.log(received_data)



var array = JSON.parse("[" + received_data + "]")[0];

let i = 0;

while (i < array.length) {
    if (array[i] == 1){
        array[i] = "ace"
    }
    i++;
}

var filePath1 = staticPath + "cards/" + array[0] + ".png";
var filePath2 = staticPath + "cards/" + array[1] + ".png";
var filePath3 = staticPath + "cards/" + array[2] + ".png";
var filePath4 = staticPath + "cards/" + array[3] + ".png";


element1.style.backgroundImage = "url(" + filePath1 + ")";
element2.style.backgroundImage = "url(" + filePath2 + ")";
element3.style.backgroundImage = "url(" + filePath3 + ")";
element4.style.backgroundImage = "url(" + filePath4 + ")";
