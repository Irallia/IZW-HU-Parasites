var fs = require("fs");
var Newick = require('newick');
// var data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
var data = fs.readFileSync("../opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre").toString();

var parsedData = Newick.parse(data);
console.log("---------------------------------")
console.log("Full data:");
console.log(parsedData);

console.log("---------------------------------")
parsedData = parsedData.branchset[0]
console.log("use only ", parsedData.name, ":");
parsedData = parsedData.branchset[1]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
console.log("---------------------------------")
console.log("only to get a small dataset:")
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[0]
console.log("-> ", parsedData.name, ":");
parsedData = parsedData.branchset[1]
console.log("-> ", parsedData.name, ":");
console.log("---------------------------------")
console.log(parsedData);
console.log("---------------------------------")

console.log("#otts =", JSON.stringify(parsedData).split("ott").length)

function readOttIds(obj, maxId, numberOfChildren) {
    // The == operator will compare for equality after doing any necessary type conversions. The === operator will not do the conversion, so if two values are not the same type === will simply return false. Both are equally quick.
    if (obj.name && obj.name != "") {
        var currentId = parseInt(obj.name.split("ott")[1])
        if (currentId > maxId) {
            maxId = currentId;
        }
    }
    if (obj.branchset) {
        numberOfChildren.push(obj.branchset.length);
        // if (obj.branchset.length > 2000) {
        //     console.log("# children=", obj.branchset.length);
        //     console.log(obj.name)
        // }
        var i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            result = readOttIds(obj.branchset[i], maxId, numberOfChildren);
            maxId = result[0];
            numberOfChildren = result[1];
            i++;
        }
    } // else is leaf
    return [maxId, numberOfChildren]
}

var numberOfChildren = [];

result = readOttIds(parsedData, 0, numberOfChildren);
maxId = result[0]
console.log("maxId =", maxId);

numberOfChildren = result[1];
var childrenPlotCsv = numberOfChildren.join("\n");

l_dataPath = "../data/labelled_supertree/"
g_dataPath = "../data/grafted_solution/"

// fs.writeFile((g_dataPath + "ottnames-childrenPlot.tsv"), nodesTsv.join(''), function (err) {
fs.writeFile((l_dataPath + "ottnames-childrenPlot.csv"), childrenPlotCsv, function (err) {
    if (err) {
        return console.log(err);
    }
});
console.log("childrenPlot csv saved");
console.log("---------------------------------")

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

var data = setOttIds(parsedData, maxId + 1, graphFormat, nodesTsv, edgesTsv);
var nextId = data[0]
graphFormat = data[1]
nodesTsv = data[2]
edgesTsv = data[3]

console.log("nextId - maxId =", nextId - maxId);
console.log("#otts Eukaryota =", JSON.stringify(parsedData).split("ott").length)

// var jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
var jsonData = JSON.stringify(parsedData);

// fs.writeFile((g_dataPath + "ottnames-prepared.json"), jsonData, function (err) {
fs.writeFile((l_dataPath + "ottnames-prepared.json"), jsonData, function (err) {
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

// fs.writeFile("grafted_solution_ottnames-nodes.tsv", nodesTsv.join(''), function (err) {
// fs.writeFile("labelled_supertree_ottnames-nodes.tsv", nodesTsv, function (err) {
//     if (err) {
//         return console.log(err);
//     }
// });

// fs.writeFile("grafted_solution_ottnames-edges.tsv", edgesTsv.join(''), function (err) {
// fs.writeFile("labelled_supertree_ottnames-edges.tsv", edgesTsv, function (err) {
//     if (err) {
//         return console.log(err);
//     }
// });