var fs = require("fs");
var Newick = require('newick');
// var data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
var data = fs.readFileSync("../opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre").toString();

var parsedData = Newick.parse(data);

console.log(parsedData);

console.log("#otts =", JSON.stringify(parsedData).split("ott").length)

function readOttIds(obj, maxId) {
    // The == operator will compare for equality after doing any necessary type conversions. The === operator will not do the conversion, so if two values are not the same type === will simply return false. Both are equally quick.
    if (obj.name && obj.name != "") {
        var currentId = parseInt(obj.name.split("ott")[1])
        if (currentId > maxId) {
            maxId = currentId;
        }
    }
    if (obj.branchset) {
        if (obj.branchset.length > 50) {
            console.log("# children=", obj.branchset.length);
        }
        var i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            maxId = readOttIds(obj.branchset[i], maxId);
            i++;
        }
    } // else is leaf
    return maxId
}

maxId = readOttIds(parsedData, 0);
console.log("maxId =", maxId);

// delete Bacteria_ott844192 and Archaea_ott996421:
var preparedData = parsedData.branchset[0]

function setOttIds(obj, nextId) {
    // The == operator will compare for equality after doing any necessary type conversions. The === operator will not do the conversion, so if two values are not the same type === will simply return false. Both are equally quick.
    if (obj.name == undefined) {
        obj[name] = "ott" + nextId;
        nextId++;
    } else if (obj.name === "") {
        obj.name = "ott" + nextId;
        nextId++;
    }
    if (obj.branchset) {
        var i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            nextId = setOttIds(obj.branchset[i], nextId);
            i++;
        }
    }
    return nextId;
}

nextId = setOttIds(preparedData, maxId + 1);

console.log("nextId - maxId =", nextId - maxId);
console.log("#otts Eukaryota =", JSON.stringify(preparedData).split("ott").length)

// var jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
var jsonData = JSON.stringify(preparedData);

fs.writeFile("labelled_supertree_ottnames-prepared.json", jsonData, function (err) {
    if (err) {
        return console.log(err);
    }
});


