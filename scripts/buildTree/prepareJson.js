var fs = require("fs");
var Newick = require('newick');
// var data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
var data = fs.readFileSync("opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre").toString();
// var dataPath = "../data/grafted_solution/";
var dataPath = "tree/labelled_supertree/";
var databaseNameNodes = "nodes_otl/";

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
    // data = data.branchset[1];
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

function setOttIds(obj, nextId, nodesTsv, edgesTsv) {
    var name = obj.name;
    var ottArray = [];
    var ottArray_ = [];
    var ottArrayBlank = [];
    if (name != undefined) {
        if (name.startsWith("'")) {
            name = name.slice(1);
        }
        if (name.endsWith("'")) {
            name = name.slice(0, -1);
        }
        ottArray = name.split("ott");
        ottArray_ = name.split("_ott");
        ottArrayBlank = name.split(" ott");
    }

    if (name == undefined) {
        obj.ott = "ott" + nextId;
        obj.name = "";
        // obj[name] = "ott" + nextId;
        nextId++;
    } else if (ottArray.length == 1) {
        obj.ott = "ott" + nextId;
        nextId++;
    } else if (ottArray_.length > 1) {
        if (ottArray_.length == 2) {
            obj.ott = "ott" + ottArray_[1];
            obj.name = ottArray_[0];
        } else if (name.includes("otta") 
                || name.includes("otte")
                || name.includes("otthi")
                || name.includes("otti")
                || name.includes("ottkei")
                || name.includes("ottleyi")
                || name.includes("ottnangensis")
                || name.includes("otto")
                || name.includes("ottu")
                || name.includes("ottwayensis")) {
            obj.ott = "ott" + ottArray_[2];
            obj.name = ottArray_[0] + "_ott" + ottArray_[1];
            // console.log("extra case: " + name);
        } else {
            // console.log("some other _ott");
            console.log(name);
        }
    } else if (ottArrayBlank.length > 1) {
        if (ottArrayBlank.length == 2) {
            obj.ott = "ott" + ottArrayBlank[1];
            obj.name = ottArrayBlank[0];
        } else if (name.includes("otter") || name.includes("otto")) {
            obj.ott = "ott" + ottArrayBlank[2];
            obj.name = ottArrayBlank[0] + " ott" + ottArrayBlank[1];
            // console.log("extra case: " + name);
        } else {
            console.log("some other ' 'ott");
            console.log(name);
        }
    } else if (ottArray.length == 2) {
        if (ottArray[0] == "") {
            obj.ott = name;
            obj.name = "";
        } else if (name.includes("ottus") || name.includes("cott") || name.includes("Sympotthastia")) {
            obj.ott = "ott" + nextId;
            nextId++;
            // console.log("extra case: " + name);
        } else {
            console.log("one ott inside:");
            console.log(name);
        }
    } else if (ottArray.length > 2) {
        if (name.includes("mrcaott")) {
            obj.ott = name;
            obj.name = "";
            if (name.split("mrcaott")[0] > 0) {
                console.log("there is a name with mrcaott:");
                console.log(name);
            }
        } else {
            console.log("more than one ott inside:");
            console.log(name);
        }
    } else {
        console.log("other problems:");
        console.log(name);
    }

    nodesTsv.push(obj.ott + "\t" + obj.name + "\n");
    if (obj.branchset) {
        var i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            data = setOttIds(obj.branchset[i], nextId, nodesTsv, edgesTsv);
            nextId = data[0];
            nodesTsv = data[1];
            edgesTsv = data[2];
            edgesTsv.push(databaseNameNodes + obj.ott + "\t" + databaseNameNodes + obj.branchset[i].ott + "\n");
            i++;
        }
    }
    return [nextId, nodesTsv, edgesTsv];
}

console.log("-------- 5) set OTT Ids & build graph files ---");

// nodes.tsv
var nodesTsv = ["_key\tname\n"];
// edges.tsv
var edgesTsv = ["_from\t_to\n"];

var data = setOttIds(parsedData, maxId + 1, nodesTsv, edgesTsv);
var nextId = data[0]
nodesTsv = data[1]
edgesTsv = data[2]

console.log("number of new Ids: nextId - maxId =", nextId - maxId);
console.log("-----------------------------------------------");
nrOtt = JSON.stringify(parsedData).split("ott").length;
nrMrcaott = JSON.stringify(parsedData).split("mrcaott").length;
console.log("#nodes in decreased data = ", nrOtt - nrMrcaott);
console.log("-----------------------------------------------");

// var jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
var jsonData = JSON.stringify(parsedData);

fs.writeFile((dataPath + "ottnames-prepared.json"), jsonData, function (err) {
    if (err) {
        return console.log(err);
    }
});

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