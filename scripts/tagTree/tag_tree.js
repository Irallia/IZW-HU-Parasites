'use strict';

const db = require('arangojs')();

db.query(`FOR doc IN interaction_tsv
    FILTER doc.freeliving == 1 && doc.directionF == "source"
    UPDATE doc WITH {
        freeliving: 1,
        directionF: "source",
        interactionTypeNameFL: doc.interactionTypeName
    } IN nodes_otl`
);

db.query(`FOR doc IN interaction_tsv
    FILTER doc.freeliving == 1 && doc.directionF == "target"
    UPDATE doc WITH {
        freeliving: 1,
        directionF: "target",
        interactionTypeNameFL: doc.interactionTypeName
    } IN nodes_otl`
);

db.query(`FOR doc IN interaction_tsv
    FILTER doc.parasite == 1 && doc.directionP == "source"
    UPDATE doc WITH {
        parasite: 1,
        directionP: "source",
        interactionTypeNameP: doc.interactionTypeName
    } IN nodes_otl`
);

db.query(`FOR doc IN interaction_tsv
    FILTER doc.parasite == 1 && doc.directionP == "target"
    UPDATE doc WITH {
        parasite: 1,
        directionP: "target",
        interactionTypeNameP: doc.interactionTypeName
    } IN nodes_otl`
);