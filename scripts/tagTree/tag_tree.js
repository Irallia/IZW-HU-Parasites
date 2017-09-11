'use strict';

const db = require('arangojs')();

console.log("tag freeliving source");

db.query(`FOR interaction IN interaction_tsv
    FILTER interaction.freeliving == 1 && interaction.directionF == "source"
        FOR node IN nodes_otl
            FILTER CONTAINS(interaction.sourceTaxonIds, CONCAT("OTT:", node._key, " ")) == true
                UPDATE node WITH {
                    freeliving: 1,
                    directionF: "source",
                    interactionTypeNameFL: interaction.interactionTypeName
                } IN nodes_otl`
);

console.log("tag freeliving target");

db.query(`FOR interaction IN interaction_tsv
FILTER interaction.freeliving == 1 && interaction.directionF == "target"
    FOR node IN nodes_otl
        FILTER CONTAINS(interaction.targetTaxonIds, CONCAT("OTT:", node._key, " ")) == true
            UPDATE node WITH {
                freeliving: 1,
                directionF: "target",
                interactionTypeNameFL: interaction.interactionTypeName
            } IN nodes_otl`
);

console.log("tag parasites source");

db.query(`FOR interaction IN interaction_tsv
FILTER interaction.parasite == 1 && interaction.directionP == "source"
    FOR node IN nodes_otl
        FILTER CONTAINS(interaction.sourceTaxonIds, CONCAT("OTT:", node._key, " ")) == true
            UPDATE node WITH {
                parasite: 1,
                directionP: "source",
                interactionTypeNameP: interaction.interactionTypeName
            } IN nodes_otl`
);

console.log("tag parasites target");

db.query(`FOR interaction IN interaction_tsv
FILTER interaction.parasite == 1 && interaction.directionP == "target"
    FOR node IN nodes_otl
        FILTER CONTAINS(interaction.targetTaxonIds, CONCAT("OTT:", node._key, " ")) == true
            UPDATE node WITH {
                parasite: 1,
                directionP: "target",
                interactionTypeNameP: interaction.interactionTypeName
            } IN nodes_otl`
);