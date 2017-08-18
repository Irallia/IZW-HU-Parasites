'use strict';

const fs = require("fs");
const Newick = require('newick');
const parser = require("biojs-io-newick");
// const data = fs.readFileSync("../opentree9.1_tree/grafted_solution/grafted_solution_ottnames.tre").toString();
const data = fs.readFileSync("opentree9.1_tree/labelled_supertree/labelled_supertree_ottnames.tre").toString();
// const dataPath = "../data/grafted_solution/";
const dataPath = "tree/labelled_supertree/";
const databaseNameNodes = "nodes_otl/";

let parsedData = Newick.parse(data);

console.log("-------- 1) Full data         -------- --------");
console.log(parsedData);

console.log("-------- 2) analyse OTT Ids   -------- --------");
console.log("#otts = ", JSON.stringify(parsedData).split("ott").length);
let maxId = findMaxOttId(parsedData, 0);
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
    // console.log("-----------------------------------------------");
    // console.log("only to get a smaller dataset:")
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Chordata_ott125642
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // mrcaott42ott658
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Craniata_ott947318
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Vertebrata_ott801601
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Gnathostomata_ott278114
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Teleostomi_ott114656
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Euteleostomi_ott114654
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Sarcopterygii_ott458402
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Dipnotetrapodomorpha_ott4940726
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Tetrapoda_ott229562
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Amniota_ott229560
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Mammalia_ott244265
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Theria_ott229558
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Eutheria_ott683263
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Boreoeutheria_ott5334778
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Euarchontoglires_ott392222
    // data = data.branchset[1]
    // console.log("-> ", data.name, ":");         // mrcaott786ott112387
    // data = data.branchset[0]
    // console.log("-> ", data.name, ":");         // Primates_ott913935
    console.log("-----------------------------------------------");
    console.log(data);
    return data;
}

console.log("-------- 3) decrease data     -------- --------");
parsedData = decreaseData(parsedData);

console.log("-------- 4) analyse number of Children --------");
let numberOfChildren = [];
let analysedResult = analyseNumberOfChildren(parsedData, numberOfChildren, 0);
numberOfChildren = analysedResult[0];
let leaves = analysedResult[1];
console.log("#leaves = ", leaves);
saveFile((dataPath + "ottnames-childrenPlot.csv"), numberOfChildren.join("\n"))
console.log("childrenPlot csv saved");
console.log("-----------------------------------------------");

function setOttIds(obj, nextId, nodesTsv, edgesTsv, tre) {  
    if (obj.visited) {
        console.log("found a circle!");
    } else {
        obj.visited = true;
    }
    let name = obj.name;
    let ottArray = [];
    let ottArray_ = [];
    let ottArrayBlank = [];
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
        obj.ott = nextId;
        obj.name = "";
        // obj[name] = "ott" + nextId;
        nextId++;
    } else if (ottArray.length == 1) {
        obj.ott = nextId;
        nextId++;
    } else if (ottArray_.length > 1) {
        if (ottArray_.length == 2) {
            obj.ott = ottArray_[1];
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
            obj.ott = ottArray_[2];
            obj.name = ottArray_[0] + "_ott" + ottArray_[1];
        } else {
            console.log("some other _ott");
            console.log(name);
        }
    } else if (ottArrayBlank.length > 1) {
        if (ottArrayBlank.length == 2) {
            obj.ott = ottArrayBlank[1];
            obj.name = ottArrayBlank[0];
        } else if (name.includes("otter") || name.includes("otto")) {
            obj.ott = ottArrayBlank[2];
            obj.name = ottArrayBlank[0] + " ott" + ottArrayBlank[1];
        } else {
            console.log("some other ' 'ott");
            console.log(name);
        }
    } else if (ottArray.length == 2) {
        if (ottArray[0] == "") {
            obj.ott = ottArray[1];
            obj.name = "";
        } else if (name.includes("ottus") || name.includes("cott") || name.includes("Sympotthastia")) {
            obj.ott = nextId;
            nextId++;
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
    tre.name = obj.ott;
    if (obj.branchset) {
        let i = 0;
        tre.children = [];
        while (i < obj.branchset.length) {
            // go deeper:
            tre.children.push({});
            let result = setOttIds(obj.branchset[i], nextId, nodesTsv, edgesTsv, tre.children[i]);
            obj.branchset[i] = result[0]
            nextId = result[1];
            nodesTsv = result[2];
            edgesTsv = result[3];
            tre.children[i] = result[4];
            edgesTsv.push(databaseNameNodes + obj.ott + "\t" + databaseNameNodes + obj.branchset[i].ott + "\n");
            i++;
        }
    }
    return [obj, nextId, nodesTsv, edgesTsv, tre];
}

console.log("-------- 5) set OTT Ids & build graph files ---");

// nodes.tsv
let nodesTsv = ["_key\tname\n"];
// edges.tsv
let edgesTsv = ["_from\t_to\n"];
let tre = {};

let treeResult = setOttIds(parsedData, maxId + 1, nodesTsv, edgesTsv, tre);
let preparedData = treeResult[0];
let nextId = treeResult[1];
nodesTsv = treeResult[2];
edgesTsv = treeResult[3];
tre = treeResult[4];
console.log("-----------------------------------------------");
console.log("prepared data:")
console.log(preparedData);
console.log("-----------------------------------------------");


console.log("number of new Ids: nextId - maxId =", nextId - maxId);
console.log("-----------------------------------------------");
let nrOtt = JSON.stringify(parsedData).split("ott").length;
let nrMrcaott = JSON.stringify(parsedData).split("mrcaott").length;
console.log("#nodes in decreased data = ", nrOtt - nrMrcaott);
console.log("-----------------------------------------------");

// let jsonData = JSON.stringify(data2, null, 4); // Indented 4 spaces
let jsonData = JSON.stringify(parsedData);
fs.writeFile((dataPath + "ottnames-prepared.json"), jsonData, function (err) {
    if (err) {
        return console.log(err);
    }
});
console.log("json saved");

saveFile((dataPath + "preparedTree.tre"), parser.parse_json(tre)) 

console.log("tre saved");

let nodesTsvFile = fs.createWriteStream(dataPath + "ottnames-nodes.tsv");
nodesTsvFile.on('error', function(err) {
    return console.log(err);
});
nodesTsv.forEach(function(v) {
    nodesTsvFile.write(v);
});
nodesTsvFile.end();
console.log("nodes saved");

let edgesTsvFile = fs.createWriteStream(dataPath + "ottnames-edges.tsv");
edgesTsvFile.on('error', function(err) {
    return console.log(err);
});
edgesTsv.forEach(function(v) {
    edgesTsvFile.write(v);
});
edgesTsvFile.end();

console.log("edges saved");
console.log("-----------------------------------------------");

// ----------------------------------------------------------------------------------------------------
// basic functions:
// ----------------------------------------------------------------------------------------------------

function findMaxOttId(obj, maxId) {
    if (obj.name && obj.name != "") {
        let currentId = parseInt(obj.name.split("ott")[1])
        if (currentId > maxId) {
            maxId = currentId;
        }
    }
    if (obj.branchset) {
        let i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            maxId = findMaxOttId(obj.branchset[i], maxId);
            i++;
        }
    } // else is leaf
    return maxId;
}

function analyseNumberOfChildren(obj, numberOfChildren, leaves) {
    if (obj.branchset) {
        numberOfChildren.push(obj.branchset.length);
        // if (obj.branchset.length > 2000) {
        //     console.log("# children=", obj.branchset.length);
        //     console.log(obj.name)
        // }
        let i = 0;
        while (i < obj.branchset.length) {
            // go deeper:
            let result = analyseNumberOfChildren(obj.branchset[i], numberOfChildren, leaves);
            numberOfChildren = result[0];
            leaves = result[1];
            i++;
        }
    } else {
        leaves++;   // else is leaf
    }
    return [numberOfChildren, leaves];
}

function saveFile(path, data) {
    fs.writeFile(path, data, function (err) {
        if (err) {
            return console.log(err);
        }
    });
}