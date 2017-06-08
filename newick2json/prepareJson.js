var fs = require("fs");
var Newick = require('newick');

var data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
var parsedData = Newick.parse(data);



// delete Bacteria_ott844192 and Archaea_ott996421:
var preparedData = parsedData.branchset[0]

console.log(preparedData);

function readOttIds(branchset, values) {
    var maxId = values[0]
    var counter = values[1]
    console.log(branchset.length)
    for (i = 0; i < branchset.length; i++) {
        if (i>0) {console.log("i=",i)}
        // The == operator will compare for equality after doing any necessary type conversions. The === operator will not do the conversion, so if two values are not the same type === will simply return false. Both are equally quick.
        if (branchset[i].name === "" || branchset[i].name == undefined) {
            console.log("no name")
        } else {
            var currentId = parseInt(branchset[i].name.split("ott")[1])
            console.log(currentId)
            if (currentId > maxId) {
                maxId = currentId;
                console.log("maxId=", maxId);
            }
        }
        if (branchset[i].branchset) {
            // go deeper:
            values = readOttIds(branchset[i].branchset, [maxId, counter+1]);
        } else {
            values = [maxId, counter+1] 
            console.log("------------------------------------------------------------");
            console.log("is leaf: ")
            console.log(branchset);
            console.log("------------------------------------------------------------");
        }
    }
    console.log("counter=",counter)
    return values
}

readOttIds(preparedData.branchset, [0,0])


// var jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
var jsonData = JSON.stringify(preparedData);
console.log("#ottIds: ", jsonData.split("ott").length)

fs.writeFile("grafted_solution_ottnames-prepared.json", jsonData, function(err) {
    if(err) {
        return console.log(err);
    }
});


