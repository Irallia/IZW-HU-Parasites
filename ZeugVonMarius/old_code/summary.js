'use strict';

const http = require('request-easy').http;
const req  = new http({hostname:'api.globalbioticinteractions.org'});

const input = encodeURIComponent('homo sapiens');
const interaction = 'hasPathogen';

const limit = 100000;
const printThreshold = 10;

const tree = { _species: {} };

//method get from object req. Input is a object parameter and 3 variables. And the "value" of an annonymous function.
req.get({path: `/interaction?type=json.v2&interactionType=${interaction}&limit=${limit}&offset=0&sourceTaxon=${input}&field=target_taxon_path&field=target_taxon_external_id&field=target_taxon_path_ranks`}, (status, headers, body)=>{
    body = JSON.parse(body);



    //console.log(body);

    /*
        { target_taxon_path: 'Ascomycota | Sordariomycetes | Ophiostomatales | Ophiostomataceae | Sporothrix | Sporothrix schenckii',
          target_taxon_path_ranks: 'Phylum | Class | Order | Family | Genus | Species',
          target_taxon_external_id: 'NBN:BMSSYS0000017767' }
    */

/*

'superkingdom |  |  | family | genus | species |  |'
'Viruses | ssRNA viruses | ssRNA negative-strand viruses | Orthomyxoviridae | Influenzavirus A | Influenza A virus | H2N2 subtype | Influenza A virus (A/Albany/1/63(H2N2))'
'superkingdom |  |  | family | genus | species |  |'
'Viruses | ssRNA viruses | ssRNA negative-strand viruses | Orthomyxoviridae | Influenzavirus A | Influenza A virus | H2N2 subtype | Influenza A virus (A/Albany/1/65(H2N2))'
'superkingdom |  |  | family | genus | species |  |'
'Viruses | ssRNA viruses | ssRNA negative-strand viruses | Orthomyxoviridae | Influenzavirus A | Influenza A virus | H2N2 subtype | Influenza A virus (A/Albany/6/58(H2N2))'

'superkingdom |  |  | family | genus | species |'
'Viruses | ssRNA viruses | ssRNA negative-strand viruses | Orthomyxoviridae | Influenzavirus B | Influenza B virus | Influenza B virus (B/Thailand/clinical isolate SA29/2002)'
'superkingdom |  |  | family | genus | species |'
'Viruses | ssRNA viruses | ssRNA negative-strand viruses | Orthomyxoviridae | Influenzavirus B | Influenza B virus | Influenza B virus (B/Thailand/clinical isolate SA3/2002)'
'superkingdom |  |  | family | genus | species |'
'Viruses | ssRNA viruses | ssRNA negative-strand viruses | Orthomyxoviridae | Influenzavirus B | Influenza B virus | Influenza B virus (B/Thailand/clinical isolate SA30/2002)'

*/


/*
    console.log( body.map(speci => {

        if ('|' === speci.target_taxon_path_ranks.slice(-1)) speci.target_taxon_path_ranks += ' ';

        console.dir(speci.target_taxon_path);
        console.dir(speci.target_taxon_path_ranks);

        return [speci.target_taxon_external_id.split(':')[0], speci.target_taxon_path.split(' | ').length];

    }).reduce( (prev, [id, len]) => {
        if (!prev[id]) {
            prev[id] = {};
        }
        if(undefined === prev[id][len]) {
            prev[id][len] = 1;
        } else {
            prev[id][len]++;
        }
        return prev;
    }, {}) );
*/


    for (const interactionResult of body) {
        try {
            if ('|' === interactionResult.target_taxon_path_ranks.slice(-1)) interactionResult.target_taxon_path_ranks += ' ';
            if ('|' === interactionResult.target_taxon_path.slice(-1)) interactionResult.target_taxon_path += ' ';

            if ('|' === interactionResult.target_taxon_path_ranks[0]) interactionResult.target_taxon_path_ranks = ' ' + interactionResult.target_taxon_path_ranks;
            if ('|' === interactionResult.target_taxon_path[0]) interactionResult.target_taxon_path = ' ' + interactionResult.target_taxon_path;

            interactionResult.key = interactionResult.target_taxon_path_ranks.split(' | ');
            interactionResult.val = interactionResult.target_taxon_path.split(' | ');

            // console.log(interactionResult.key, '#', interactionResult.val);
            // console.log(interactionResult.target_taxon_path_ranks, '#', interactionResult.target_taxon_path);
            
        } catch(e) {
            console.log('Rank does not match value for:');
            console.log(interactionResult);
            continue;
        }

        insertIntoTree(tree, interactionResult);
        calcSums(tree);
    }

// 'superkingdom |  |  | family | genus | species |  | '
    
    console.log(JSON.stringify(tree, false, 6));

});


function calcSums(node) {

    node.sum = 0;
    for(const key in node) {
        if (key === 'sum') continue;
        if ('number' === typeof node[key]) {
            node.sum += node[key];
        } else {
            node.sum += calcSums(node[key]);
        }
    }
    return node.sum;
}

function insertIntoTree(tree, speci) {

    if (speci.key.length === 0) {
        console.log('No rank definition for:');
        console.log(speci);
        return;
    } // if

    if ('species' === speci.key[0].toLowerCase() ) {

        let val;
        try {
            val = speci.val.shift().toLowerCase();
        } catch(e) { val = 'unknown'; }

        const genusIdx  = speci.target_taxon_path_ranks.split(' | ').indexOf('genus');
        const genusName = speci.target_taxon_path.split(' | ')[genusIdx];
        
        if (undefined === tree[genusName]) tree[genusName] = {};

        if (undefined === tree[genusName][val]) {
            tree[genusName][val] = 0;
        } // if
        
        tree[genusName][val]++; // .push(speci);

        return;
    } // if

    const key = speci.key.shift();
    speci.val.shift();

    if (!tree[key]) {
        tree[key] = { };
    }

    insertIntoTree(tree[key], speci);
}

//------------------------------------------------------------------------------------------------------------------------

/*
function get_lowest_depth(){}
    return lowestDepth;

function getMostCommonHits(tree){


    if total depth is > then lowestDepth; kill useless ranks (go through specific loop for results with more depth) (maybe track total depth bei hit?, append counter to species level)

    loop through genus/rank and get number of duplicates

    add number of hits in one depth; get % for every rank

    when no %rank < printThreshold then go 1 depth higher and add #hits 

    if %rank is > printThreshold -> print 3 of the highest ranks, save 10 after (mouseover);




}

"The Human eats the organisms of the Phylla Paarhufer(3232/13%), Delphine(3532/4%), Pilze(2435/2%) and others." (mouseover >others< lists 10 next Phylla at the same way)
mouseover the % result lists the ranks under it in % Paarhufer -> %Kühe, %Pferde..

*/

function input_field(){
/*
##      interaction     source     target
## 1        preysOn   predator       prey
## 2   preyedUponBy       prey   predator
## 3     parasiteOf   parasite       host
## 4    hasParasite       host   parasite
## 5     pollinates pollinator      plant
## 6   pollinatedBy      plant pollinator
## 7     pathogenOf   pathogen       host
## 8    hasPathogen      plant pollinator
## 9     symbiontOf     source     target
## 10 interactsWith     source     target
*/
}


function append_field(field_name){
/*
	LATITUDE("latitude"),
    LONGITUDE("longitude"),
    ALTITUDE("altitude"),
    FOOTPRINT_WKT("footprintWKT"),
    LOCALITY("locality"),
    COLLECTION_TIME_IN_UNIX_EPOCH("collection_time_in_unix_epoch"),
    STUDY_TITLE("study_title"),
    INTERACTION_TYPE("interaction_type"),

    TARGET_TAXON_NAME("target_taxon_name"),
    SOURCE_TAXON_NAME("source_taxon_name"),

    TARGET_TAXON_COMMON_NAMES("target_taxon_common_names"),
    SOURCE_TAXON_COMMON_NAMES("source_taxon_common_names"),

    TARGET_TAXON_EXTERNAL_ID("target_taxon_external_id"),
    SOURCE_TAXON_EXTERNAL_ID("source_taxon_external_id"),

    TARGET_TAXON_PATH("target_taxon_path"),
    SOURCE_TAXON_PATH("source_taxon_path"),

    TARGET_TAXON_PATH_RANKS("target_taxon_path_ranks"),
    SOURCE_TAXON_PATH_RANKS("source_taxon_path_ranks"),

    TARGET_TAXON_PATH_IDS("target_taxon_path_ids"),
    SOURCE_TAXON_PATH_IDS("source_taxon_path_ids"),

    TARGET_SPECIMEN_TOTAL_FREQUENCY_OF_OCCURRENCE("target_specimen_frequency_of_occurrence"),
    TARGET_SPECIMEN_TOTAL_FREQUENCY_OF_OCCURRENCE_PERCENT("target_specimen_frequency_of_occurrence_percent"),
    TARGET_SPECIMEN_TOTAL_VOLUME_ML("target_specimen_total_volume_ml"),
    TARGET_SPECIMEN_TOTAL_VOLUME_PERCENT("target_specimen_total_volume_ml_percent"),
    TARGET_SPECIMEN_TOTAL_COUNT("target_specimen_total_count"),
    TARGET_SPECIMEN_TOTAL_COUNT_PERCENT("target_specimen_total_count_percent"),

    TARGET_SPECIMEN_ID("tmp_and_unique_target_specimen_id"),
    SOURCE_SPECIMEN_ID("tmp_and_unique_source_specimen_id"),

    TARGET_SPECIMEN_PHYSIOLOGICAL_STATE("target_specimen_physiological_state"),
    SOURCE_SPECIMEN_PHYSIOLOGICAL_STATE( "source_specimen_physiological_state"),

    TARGET_SPECIMEN_BODY_PART("target_specimen_body_part"),
    SOURCE_SPECIMEN_BODY_PART("source_specimen_body_part"),

    SOURCE_SPECIMEN_LIFE_STAGE("source_specimen_life_stage"),
    TARGET_SPECIMEN_LIFE_STAGE("target_specimen_life_stage"),

    SOURCE_SPECIMEN_BASIS_OF_RECORD("source_specimen_basis_of_record"),
    TARGET_SPECIMEN_BASIS_OF_RECORD("target_specimen_basis_of_record"),

    TAXON_NAME("taxon_name"),
    TAXON_COMMON_NAMES("taxon_common_names"),
    TAXON_EXTERNAL_ID("taxon_external_id"),

    TAXON_EXTERNAL_URL("taxon_external_url"),
    TAXON_PATH("taxon_path"),
    TAXON_PATH_IDS("taxon_path_ids"),
    TAXON_PATH_RANKS("^"),
    STUDY_URL("study_url"),
    STUDY_DOI("study_doi"),
    STUDY_CITATION("study_citation"),
    STUDY_SOURCE_CITATION("study_source_citation"),
    STUDY_SOURCE_ID("study_source_id"),
    NUMBER_OF_DISTINCT_TAXA("number_of_distinct_taxa", "only available for /reports/* queries"),
    NUMBER_OF_DISTINCT_TAXA_NO_MATCH("number_of_distinct_taxa_no_match", "only available for /reports/* queries"),
    NUMBER_OF_SOURCES("number_of_sources", "only available for /reports/* queries"),
    NUMBER_OF_STUDIES("number_of_studies", "only available for /reports/* queries"),
    NUMBER_OF_INTERACTIONS("number_of_interactions", "available for /interaction queries by source/target taxon name and/or interactionType only"),
    STUDY_SOURCE_DOI("study_source_doi"),
    STUDY_SOURCE_FORMAT("study_source_format"),
    STUDY_SOURCE_ARCHIVE_URI("study_source_archive_uri");
    */
}

