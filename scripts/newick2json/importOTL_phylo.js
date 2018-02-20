var fs = require("fs");
var Newick = require('newick');

var data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
var parsedData = Newick.parse(data);
// var jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
var jsonData = JSON.stringify(parsedData);
fs.writeFile("grafted_solution_ottnames.json", jsonData, function(err) {
    if(err) {
        return console.log(err);
    }
});

console.log("1/4");

data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution.tre").toString();
parsedData = Newick.parse(data);
// jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
jsonData = JSON.stringify(parsedData);
fs.writeFile("grafted_solution.json", jsonData, function(err) {
    if(err) {
        return console.log(err);
    }
});

console.log("2/4");

data = fs.readFileSync("../opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre").toString();
parsedData = Newick.parse(data);
// jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
jsonData = JSON.stringify(parsedData);
fs.writeFile("labelled_supertree_ottnames.json", jsonData, function(err) {
    if(err) {
        return console.log(err);
    }
});

console.log("3/4");

// data = fs.readFileSync("../opentree9.1_tree/labelled_supertree/labelled_supertree.tre").toString();
// parsedData = Newick.parse(data);
// // jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
// jsonData = JSON.stringify(parsedData);
// fs.writeFile("labelled_supertree.json", jsonData, function(err) {
//     if(err) {
//         return console.log(err);
//     }
// });

console.log("4/4");
console.log("labelled_supertree.tre was skipped")





