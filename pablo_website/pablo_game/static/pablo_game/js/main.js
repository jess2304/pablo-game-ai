

var element1 = document.getElementById("human-card-1");
var element2 = document.getElementById("human-card-2");
var element3 = document.getElementById("human-card-3");
var element4 = document.getElementById("human-card-4");



var array = JSON.parse("[" + received_data + "]")[0];

let i = 0;

while (i < array.length) {
    if (array[i] == 1){
        array[i] = "ace"
    }
    i++;
}

var filePath1 = staticPath + "cards/" + array[0] + "_of_clubs.png";
var filePath2 = staticPath + "cards/" + array[1] + "_of_clubs.png";
var filePath3 = staticPath + "cards/" + array[2] + "_of_clubs.png";
var filePath4 = staticPath + "cards/" + array[3] + "_of_clubs.png";
// of clubs will change next time to make them mixed. We'll think about that.
// I think i should modify the environment to give me in views a human hand that contains the colour of the card too. 
// with this possibility i will erase the last part of the path.

// i have to make it in the init and drawing card in case of colours_considering in the env.


element1.style.backgroundImage = "url(" + filePath1 + ")";
element2.style.backgroundImage = "url(" + filePath2 + ")";
element3.style.backgroundImage = "url(" + filePath3 + ")";
element4.style.backgroundImage = "url(" + filePath4 + ")";
