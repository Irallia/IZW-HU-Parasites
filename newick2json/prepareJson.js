var fs = require("fs");
var Newick = require('newick');
var data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
// var data = fs.readFileSync("../opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre").toString();

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
        // if (obj.branchset.length > 50) {
        //     console.log("# children=", obj.branchset.length);
        // }
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
var graphFormat = {
    nodes: [],
    edges: []
}
// nodes.tsv
var nodesTsv = ["_key\tname\n"];
// edges.tsv
var edgesTsv = ["_from\t_to\n"];

function setOttIds(obj, nextId, graphFormat, nodesTsv, edgesTsv) {
    // The == operator will compare for equality after doing any necessary type conversions. The === operator will not do the conversion, so if two values are not the same type === will simply return false. Both are equally quick.
    if (obj.name == undefined) {
        obj[name] = "ott" + nextId;
        nextId++;
    } else if (obj.name === "") {
        obj.name = "ott" + nextId;
        nextId++;
    }
    // Fill graphFormat nodes:
    graphFormat.nodes.push({id: obj.name})
    var id = "ott" + obj.name.split("ott")[1];
    var name = obj.name.split("ott")[0].slice(0, -1);
    nodesTsv.push(id, "\t", name, "\n");
    if (obj.branchset) {
        var i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            data = setOttIds(obj.branchset[i], nextId, graphFormat, nodesTsv, edgesTsv);
            nextId = data[0];
            graphFormat = data[1];
            nodesTsv = data[2];
            edgesTsv = data[3];
            // Fill graphFormat edges:
            graphFormat.edges.push({_from: "nodes/" + obj.name, _to: "nodes/" + obj.branchset[i].name});
            data[3].push("nodes/ott", obj.name.split("ott")[1], "\t", "nodes/ott", obj.branchset[i].name.split("ott")[1] + "\n");
            i++;
        }
    }
    return [nextId, graphFormat, nodesTsv, edgesTsv];
}

var data = setOttIds(preparedData, maxId + 1, graphFormat, nodesTsv, edgesTsv);
var nextId = data[0]
graphFormat = data[1]
nodesTsv = data[2]
edgesTsv = data[3]

console.log("nextId - maxId =", nextId - maxId);
console.log("#otts Eukaryota =", JSON.stringify(preparedData).split("ott").length)

// var jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
var jsonData = JSON.stringify(preparedData);

fs.writeFile("grafted_solution_ottnames-prepared.json", jsonData, function (err) {
// fs.writeFile("labelled_supertree_ottnames-prepared.json", jsonData, function (err) {
    if (err) {
        return console.log(err);
    }
});

// var jsonGraphData = JSON.stringify(graphFormat);
// // fs.writeFile("grafted_solution_ottnames-graph_prepared.json", jsonGraphData, function (err) {
// fs.writeFile("labelled_supertree_ottnames-graph_prepared.json", jsonGraphData, function (err) {
//     if (err) {
//         return console.log(err);
//     }
// });

fs.writeFile("grafted_solution_ottnames-nodes.tsv", nodesTsv.join(''), function (err) {
// fs.writeFile("labelled_supertree_ottnames-nodes.tsv", nodesTsv, function (err) {
    if (err) {
        return console.log(err);
    }
});

fs.writeFile("grafted_solution_ottnames-edges.tsv", edgesTsv.join(''), function (err) {
// fs.writeFile("labelled_supertree_ottnames-edges.tsv", edgesTsv, function (err) {
    if (err) {
        return console.log(err);
    }
});