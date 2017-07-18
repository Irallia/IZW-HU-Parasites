var fs = require("fs");
var Newick = require('newick');
// var data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
var data = fs.readFileSync("../opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre").toString();
// var dataPath = "../data/grafted_solution/";
var dataPath = "../data/labelled_supertree/";

var parsedData = Newick.parse(data);

console.log("-------- 1) Full data         -------- --------");
console.log(parsedData);

function findMaxOttId(obj, maxId) {
    if (obj.name && obj.name != "") {
        var currentId = parseInt(obj.name.split("ott")[1])
        if (currentId > maxId) {
            maxId = currentId;
        }
    }
    if (obj.branchset) {
        var i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            maxId = findMaxOttId(obj.branchset[i], maxId);
            i++;
        }
    } // else is leaf
    return maxId;
}

console.log("-------- 2) analyse OTT Ids   -------- --------");
console.log("#otts = ", JSON.stringify(parsedData).split("ott").length);
maxId = findMaxOttId(parsedData, 0);
console.log("maxId = ", maxId);

/** decrease date from all cellular organisms to eukaryotes or less */
function decreaseData(data) {
    data = data.branchset[0];
    console.log("use only ", data.name, ":");   // Eukaryota_ott304358
    data = data.branchset[1];
    // console.log("-> ", data.name, ":");         // Opisthokonta_ott332573
    // data = data.branchset[0];
    // console.log("-> ", data.name, ":");         // mrcaott24ott98036
    // data = data.branchset[0];
    // console.log("-> ", data.name, ":");         // Holozoa_ott5246131
    // data = data.branchset[0];
    // console.log("-> ", data.name, ":");         // mrcaott24ott34294
    // data = data.branchset[0];
    // console.log("-> ", data.name, ":");         // Metazoa_ott691846
    // console.log("-----------------------------------------------");
    // console.log("only to get a small dataset:")
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // mrcaott24ott3989
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // mrcaott24ott212873
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // mrcaott24ott150
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Bilateria_ott117569
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // mrcaott24ott42
    // data = data.branchset[1]
    // console.log("-> ", data.name, ":");         // Deuterostomia_ott147604
    console.log("-----------------------------------------------");
    console.log(data);
    return data;
}

console.log("-------- 3) decrease data     -------- --------");
parsedData = decreaseData(parsedData);
console.log("-----------------------------------------------");
console.log("#nodes in decreased data = ", JSON.stringify(parsedData).split("ott").length)

function analyseNumberOfChildren(obj, numberOfChildren, leaves) {
    if (obj.branchset) {
        numberOfChildren.push(obj.branchset.length);
        // if (obj.branchset.length > 2000) {
        //     console.log("# children=", obj.branchset.length);
        //     console.log(obj.name)
        // }
        var i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            result = analyseNumberOfChildren(obj.branchset[i], numberOfChildren, leaves);
            numberOfChildren = result[0];
            leaves = result[1];
            i++;
        }
    } else {
        leaves++;   // else is leaf
    }
    return [numberOfChildren, leaves];
}

console.log("-------- 4) analyse number of Children --------");
var numberOfChildren = [];
result = analyseNumberOfChildren(parsedData, numberOfChildren, 0);
numberOfChildren = result[0];
leaves = result[1];
console.log("#leaves = ", leaves);
var childrenPlotCsv = numberOfChildren.join("\n");

fs.writeFile((dataPath + "ottnames-childrenPlot.csv"), childrenPlotCsv, function (err) {
    if (err) {
        return console.log(err);
    }
});

console.log("childrenPlot csv saved");
console.log("-----------------------------------------------");

function setOttIds(obj, nextId, graphFormat, nodesTsv, edgesTsv) {
    if (obj.name == undefined) {
        obj[name] = "ott" + nextId;
        nextId++;
    } else if (obj.name.split("ott").length = 1) {
        obj.name = obj.name + "ott" + nextId;
        nextId++;
    }
    // Fill graphFormat nodes:
    graphFormat.nodes.push({id: obj.name});

    var id = "ott" + obj.name.split("ott")[1];
    var name = obj.name.split("ott")[0].slice(0, -1);
    if (obj.name.split("mrcaott").length > 1) {
        id = "mrcaott" + obj.name.split("mrcaott")[1];
        name = obj.name.split("mrcaott")[0].slice(0, -1);
    }

    nodesTsv.push(id + "\t" + name + "\n");
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
            edgesTsv.push("nodes/ott" + obj.name.split("ott")[1] + "\t" + "nodes/ott" + obj.branchset[i].name.split("ott")[1] + "\n");
            i++;
        }
    }
    return [nextId, graphFormat, nodesTsv, edgesTsv];
}

console.log("-------- 5) set OTT Ids & build graph files ---");

var graphFormat = {
    nodes: [],
    edges: []
}
// nodes.tsv
var nodesTsv = ["_key\tname\n"];
// edges.tsv
var edgesTsv = ["_from\t_to\n"];

var data = setOttIds(parsedData, maxId + 1, graphFormat, nodesTsv, edgesTsv);
var nextId = data[0]
graphFormat = data[1]
nodesTsv = data[2]
edgesTsv = data[3]

console.log("number of new Ids: nextId - maxId =", nextId - maxId);

// var jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
var jsonData = JSON.stringify(parsedData);

fs.writeFile((dataPath + "ottnames-prepared.json"), jsonData, function (err) {
    if (err) {
        return console.log(err);
    }
});

// var jsonGraphData = JSON.stringify(graphFormat);
// fs.writeFile(dataPath + "ottnames-graph_prepared.json", jsonGraphData, function (err) {
//     if (err) {
//         return console.log(err);
//     }
// });

var nodesTsvFile = fs.createWriteStream(dataPath + "ottnames-nodes.tsv");
nodesTsvFile.on('error', function(err) {
    return console.log(err);
});
nodesTsv.forEach(function(v) {
    nodesTsvFile.write(v);
});
nodesTsvFile.end();


var edgesTsvFile = fs.createWriteStream(dataPath + "ottnames-edges.tsv");
edgesTsvFile.on('error', function(err) {
    return console.log(err);
});
edgesTsv.forEach(function(v) {
    edgesTsvFile.write(v);
});
edgesTsvFile.end();