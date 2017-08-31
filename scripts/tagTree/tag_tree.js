'use strict';

const db = require('arangojs')();

console.log("tag freeliving source");

db.query(`FOR doc IN interaction_tsv
    FILTER doc.freeliving == 1 && doc.directionF == "source"
    FOR doc2 IN nodes_otl
        FILTER CONTAINS(doc.targetTaxonIds, CONCAT("OTT:", doc2.ott))
        UPDATE doc2 WITH {
            freeliving: 1,
            directionF: "source",
            interactionTypeNameFL: doc.interactionTypeName
        } IN nodes_otl`
);

console.log("tag freeliving target");

db.query(`FOR doc IN interaction_tsv
    FILTER doc.freeliving == 1 && doc.directionF == "target"
    FOR doc2 IN nodes_otl
        FILTER CONTAINS(doc.targetTaxonIds, CONCAT("OTT:", doc2.ott))
        UPDATE doc2 WITH {
            freeliving: 1,
            directionF: "target",
            interactionTypeNameFL: doc.interactionTypeName
        } IN nodes_otl`
);

console.log("tag parasites source");

db.query(`FOR doc IN interaction_tsv
    FILTER doc.parasite == 1 && doc.directionP == "source"
    FOR doc2 IN nodes_otl
        FILTER CONTAINS(doc.targetTaxonIds, CONCAT("OTT:", doc2.ott))
        UPDATE doc2 WITH {
            parasite: 1,
            directionP: "source",
            interactionTypeNameP: doc.interactionTypeName
        } IN nodes_otl`
);

console.log("tag parasites target");

db.query(`FOR doc IN interaction_tsv
    FILTER doc.parasite == 1 && doc.directionP == "target"
    FOR doc2 IN nodes_otl
        FILTER CONTAINS(doc.targetTaxonIds, CONCAT("OTT:", doc2.ott))
        UPDATE doc2 WITH {
            parasite: 1,
            directionP: "target",
            interactionTypeNameP: doc.interactionTypeName
        } IN nodes_otl`
);