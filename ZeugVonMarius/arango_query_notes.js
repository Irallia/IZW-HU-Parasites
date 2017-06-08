#arango db queries

/* Please insert some values for the @@collection1 and @@collection2 bind parameters */
//FOR doc1 IN @@collection1
//  FOR doc2 IN @@collection2
//    FILTER doc1.`attribute` == doc2.`attribute`
//    RETURN { doc1, doc2 }


//for doc in nodes_otl
//filter lower(doc.name) == "metazoa"
//return doc


return count (
for doc in interaction_tsv
filter contains(doc.sourceTaxonIds, "OTT:")
return doc
)

/* Please insert some values for the @@collection1 and @@collection2 bind parameters */
//FOR doc1 IN @@collection1
//  FOR doc2 IN @@collection2
//    FILTER doc1.`attribute` == doc2.`attribute`
//    RETURN { doc1, doc2 }


//for doc in nodes_otl
//filter lower(doc.rank) == "domain"
//return doc


//for doc in nodes_otl
//filter contains(doc.name, "sapiens")
//return doc

//for doc in  (FOR v,e IN OUTBOUND SHORTEST_PATH 'nodes_otl/304358' TO 'nodes_otl/5341349' GRAPH 'otl' return e)
//filter doc
//insert merge({_id:concat('aosdf/', doc._key)}, doc) in aosdf { ignoreErrors: true }
//
//
//for doc in  (FOR v,e IN OUTBOUND SHORTEST_PATH 'nodes_otl/304358' TO 'nodes_otl/5341349' GRAPH 'otl' return v)
//filter doc
//insert merge({_id:concat('aosdf/', doc._key)}, doc) in aosdf { ignoreErrors: true }

//for doc in interaction_tsv limit 100 return doc


//FOR v,e IN OUTBOUND SHORTEST_PATH 'nodes_otl/304358' TO 'nodes_otl/5341349' GRAPH 'otl' return v



//
//for v,e,p in 1..n outbound startid edgescol
//
//Filter p.vertices[-1] == homosapiensid
//
//Return p