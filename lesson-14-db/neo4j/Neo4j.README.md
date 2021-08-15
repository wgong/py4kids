# Neo4j Graph DB

## Setup


### Download - https://neo4j.com/download

### Install 

#### Ubuntu
- https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-20-04

```
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
sudo add-apt-repository "deb https://debian.neo4j.com stable 4.1"
sudo apt install neo4j
sudo systemctl enable|disable neo4j.service
sudo systemctl status|start|stop neo4j.service

cd ~/neo4j
./neo4j-desktop-1.4.1-x86_64.AppImage &  # launch Desktop

which cypher-shell
/usr/bin/cypher-shell

cypher-shell
cypher-shell -a 'neo4j://localhost:7687'

Connected to Neo4j 4.1.0 at neo4j://localhost:7687 as user neo4j.

neo4j browser: http://localhost:7474/browser/

GraphQL server is running @ http://127.0.0.1:11001
Relate management API is running @ http://127.0.0.1:12630


:help

Available commands:
  :begin    Open a transaction
  :commit   Commit the currently open transaction
  :exit     Exit the logger
  :help     Show this help message
  :history  Print a list of the last commands executed
  :param    Set the value of a query parameter
  :params   Print all currently set query parameters and their values
  :rollback Rollback the currently open transaction
  :source   Interactively executes cypher statements from a file
  :use      Set the active database


:exit

```

#### AppImage
$ chmod a+x ~/Downloads/neo4j-desktop-1.4.1-x86_64.AppImage
$ mv ~/Downloads/neo4j-desktop-1.4.1-x86_64.AppImage ~/neo4j
$ cd ~/neo4j
$ ./neo4j-desktop-1.4.1-x86_64.AppImage


Install Guide - https://neo4j.com/download-thanks-desktop/?edition=desktop&flavour=unix&release=1.4.1&offline=true#installation-guide

[Explore New Worlds — Adding Plugins to Neo4j](https://medium.com/neo4j/explore-new-worlds-adding-plugins-to-neo4j-26e6a8e5d37e)


## Neo4j Browser

url=http://localhost:7474/browser/
neo4j/graphalgo

Neo4j Browser is a command driven client, like a web-based shell environment. It is perfect for running ad-hoc graph queries, with just enough ability to prototype a Neo4j-based application.

Neo4j is like a mashup of a REPL + lightweight IDE + graph visualization.

- Developer focused, for writing and running graph queries with Cypher
- Exportable tabular results of any query result
- Graph visualization of query results containing nodes and relationships
- Convenient exploration of Neo4j's REST API

```
Usage:	    :help <topic>
Topics:	    :help cypher 
            :help commands 
            :help keys
Guides:	    :play intro 
            :play start
            :play concepts 
            :play cypher
Examples:	:play movie graph 
            :play northwind graph

            :clear

:play intro-neo4j-exercises

:dbs  # list all available databases
:use system  # switch to a db
:use neo4j

:play movie

CALL db.labels() YIELD label
RETURN count(label) AS count;

CALL db.labels() YIELD label
RETURN label;

Movie
Person

match (p:Movie) return p.title;

CALL db.schema()
CALL db.schema.visualization()   // to view schema
CALL dbms.procedures()   // to view functions


```

:play intro

shift-enter to use multi-line editing

ctrl-enter to run a query


## Learn neo4j

### :play concept
A graph database can store any kind of data using a few simple concepts:

* Nodes - graph data records      :annotated by ()
* Relationships - connect nodes   :annotated by []
* Properties - named data values  :annotated by {}

Nodes can be grouped together by applying a Label to each member. 
In our social graph, we'll label each node that represents a Person.  (Label is like Node-type)

A node can have zero or more labels
Labels do not have any properties

Neo4j can store billions of nodes

Relationships always have direction;
Relationships always have a type;
Relationships form patterns of data;

Both Node and Rel can have properties

### Cypher Fundamentals
:play cypher

|  CYPHER  |  SQL  |
| ---------------------- | ----------- |
| CREATE   | INSERT  |
| RETURN   | SELECT  |
| MATCH                  | FROM, JOIN  |
| WHERE    | WHERE  |
| SET    | UPDATE  |
| MERGE    | INSERT, UPDATE  |
| DELETE, DETACH DELETE |  DELETE  |

Neo4j's Cypher language is purpose built for working with graph data.  
Like SQL in RDBMS, Cypher is declarative, describing what to find, not how to find it; 

```
CREATE (ee:Person { name: "Emil", from: "Sweden", klout: 99 })
```
CREATE clause to create data
() parenthesis to indicate a node
ee:Person : variable 'ee' and label 'Person' for the new node
curly brackets to add properties to the node

```
MATCH (ee:Person) WHERE ee.name = "Emil" RETURN ee;
```
MATCH clause to specify a pattern of nodes and relationships
(ee:Person) a single node pattern with label 'Person' which will assign matches to the variable 'ee'
WHERE clause to constrain the results
ee.name = "Emil" compares name property to the value "Emil"
RETURN clause used to request particular results

```
MATCH (ee:Person) WHERE ee.name = "Emil"
CREATE (js:Person { name: "Johan", from: "Sweden", learn: "surfing" }),
(ir:Person { name: "Ian", from: "England", title: "author" }),
(rvb:Person { name: "Rik", from: "Belgium", pet: "Orval" }),
(ally:Person { name: "Allison", from: "California", hobby: "surfing" }),
(ee)-[:KNOWS {since: 2001}]->(js),
(ee)-[:KNOWS {rating: 5}]->(ir),
(js)-[:KNOWS]->(ir),
(js)-[:KNOWS]->(rvb),
(ir)-[:KNOWS]->(js),
(ir)-[:KNOWS]->(ally),
(rvb)-[:KNOWS]->(ally)
```

```
MATCH (ee:Person)-[:KNOWS]-(friends)
WHERE ee.name = "Emil" RETURN ee, friends
```
MATCHclause to describe the pattern from known Nodes to found Nodes
(ee)starts the pattern with a Person (qualified by WHERE)
-[:KNOWS]-matches "KNOWS" relationships (in either direction)
(friends)will be bound to Emil's friends


```
MATCH (js:Person)-[:KNOWS]-()-[:KNOWS]-(surfer)
WHERE js.name = "Johan" AND surfer.hobby = "surfing"
RETURN DISTINCT surfer
```
()empty parenthesis to ignore these nodes
DISTINCTbecause more than one path will match the pattern
surferwill contain Allison, a friend of a friend who surfs


```
PROFILE MATCH (js:Person)-[:KNOWS]-()-[:KNOWS]-(surfer)
WHERE js.name = "Johan" AND surfer.hobby = "surfing"
RETURN DISTINCT surfer
```



### Movies Graph DB

:play movies

create database movies

:source movies.cql

// list  20 movies played by Tom Hanks with director

Match (a:Person {name:'Tom Hanks'})-[:ACTED_IN]->(m)<-[:DIRECTED]-(d) RETURN a,m,d LIMIT 20;

// list  20 movies played by Tom Hanks 

Match (a:Person {name:'Tom Hanks'})-[:ACTED_IN]->(m)RETURN a,m LIMIT 5;

// find actor Tom Hanks

MATCH (tom:Person {name: "Tom Hanks"}) RETURN tom;

return

```
{
  "identity": 71,
  "labels": [
    "Person"
  ],
  "properties": {
"name": "Tom Hanks",
"born": 1956
  }
}
```

// find movie by title
```
MATCH (m:Movie {title: "Cloud Atlas"}) RETURN m;

MATCH (m:Movie {title: "Cloud Atlas"})<-[:ACTED_IN]-(a:Person) RETURN m, a;

```
// find 10 person
```
MATCH (p:Person) RETURN p.name AS Name,p.born AS BirthYear limit 10;
```
// filter by release year
```
MATCH (nineties:Movie) WHERE nineties.released >= 1990 AND nineties.released < 2000 RETURN nineties.title limit 10;

MATCH (p:Person {name: "Tom Hanks"})-[:ACTED_IN]->(m) return m,p;
```
// find directors of a movie
```
MATCH (cloudAtlas {title: "Cloud Atlas"})<-[:DIRECTED]-(directors) RETURN directors.name
```
// find coActors
```
MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors) RETURN coActors.name

MATCH (people:Person)-[relatedTo]-(:Movie {title: "Cloud Atlas"}) RETURN people.name, Type(relatedTo), relatedTo;
```
// Movies and actors up to 4 "hops" away from Kevin Bacon
```
MATCH (bacon:Person {name:"Kevin Bacon"})-[*1..4]-(hollywood)
RETURN DISTINCT hollywood

// Bacon path, the shortest path of any relationships to Meg Ryan

MATCH p=shortestPath(
(bacon:Person {name:"Kevin Bacon"})-[*]-(meg:Person {name:"Meg Ryan"})
)
RETURN p;


[{"name":"Kevin Bacon","born":1958},{"roles":["Jack Swigert"]},{"tagline":"Houston, we have a problem.","title":"Apollo 13","released":1995}
,{"tagline":"Houston, we have a problem.","title":"Apollo 13","released":1995},{"roles":["Jim Lovell"]},{"name":"Tom Hanks","born":1956},{"name":"Tom Hanks","born":1956},{"roles":["Sam Baldwin"]},{"tagline":"What if someone you never met, someone you never saw, someone you never knew was the only someone for you?","title":"Sleepless in Seattle","released":1993},{"tagline":"What if someone you never met, someone you never saw, someone you never knew was the only someone for you?","title":"Sleepless in Seattle","released":1993},{"roles":["Annie Reed"]},{"name":"Meg Ryan","born":1961}]  

```

//Extend Tom Hanks co-actors, to find co-co-actors who haven't worked with Tom Hanks...
```
MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors),
  (coActors)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors)
WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors) AND tom <> cocoActors
RETURN cocoActors.name AS Recommended, count(*) AS Strength ORDER BY Strength DESC
```
//Find someone to introduce Tom Hanks to Tom Cruise
```
MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors),
  (coActors)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cruise:Person {name:"Tom Cruise"})
RETURN tom, m, coActors, m2, cruise;
```


collect() aggregates values into a list:

```
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name = 'Tom Cruise'
RETURN collect(m.title) AS `movies by Tom Cruise`

```


//Delete all Movie and Person nodes, and their relationships

MATCH (n) DETACH DELETE n;

//Prove that the Movie Graph is gone

MATCH (n) RETURN n;

### Migrate from RDBMS to Graph - Northwind dataset
:play northwind-graph


The Northwind Graph demonstrates how to migrate from a relational database to Neo4j. The transformation is iterative and deliberate, emphasizing the conceptual shift from relational tables to the nodes and relationships of a graph.


- Load: create data from external CSV files
- Index: index nodes based on label
- Relate: transform foreign key references into data relationships
- Promote: transform join records into relationships

#### Load records

// load products
```
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/products.csv" AS row
CREATE (n:Product)
SET n = row,
n.unitPrice = toFloat(row.unitPrice),
n.unitsInStock = toInteger(row.unitsInStock), n.unitsOnOrder = toInteger(row.unitsOnOrder),
n.reorderLevel = toInteger(row.reorderLevel), n.discontinued = (row.discontinued <> "0"); 
```
// load product categories
```
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/categories.csv" AS row
CREATE (n:Category)
SET n = row; 
```
// load suppliers
```
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/suppliers.csv" AS row
CREATE (n:Supplier)
SET n = row;
```
// load customers
```
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/customers.csv" AS row
CREATE (n:Customer)
SET n = row;
```
// load orders
```
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/orders.csv" AS row
CREATE (n:Order)
SET n = row;
```

// load order details
```
LOAD CSV WITH HEADERS FROM "http://data.neo4j.com/northwind/order-details.csv" AS row
MATCH (p:Product), (o:Order)
WHERE p.productID = row.productID AND o.orderID = row.orderID
CREATE (o)-[details:ORDERS]->(p)
SET details = row,
details.quantity = toInteger(row.quantity);
```

#### Create indexes
```
CREATE INDEX ON :Product(productID);
CREATE INDEX ON :Category(categoryID);
CREATE INDEX ON :Supplier(supplierID);

CREATE INDEX ON :Customer(customerID);
CREATE INDEX ON :Order(orderID);
```

#### Convert joins into data relationships
```
MATCH (p:Product),(c:Category)
WHERE p.categoryID = c.categoryID
CREATE (p)-[:PART_OF]->(c);

MATCH (p:Product),(s:Supplier)
WHERE p.supplierID = s.supplierID
CREATE (s)-[:SUPPLIES]->(p);

MATCH (c:Customer),(o:Order)
WHERE c.customerID = o.customerID
CREATE (c)-[:PURCHASED]->(o);

```
#### Query using patterns
```

MATCH (s:Supplier)-->(:Product)-->(c:Category)
RETURN s.companyName as Company, collect(distinct c.categoryName) as Categories;
//List the product categories provided by each supplier.


MATCH (c:Category {categoryName:"Produce"})<--(:Product)<--(s:Supplier)
RETURN DISTINCT s.companyName as ProduceSuppliers;
//Find the produce suppliers.

MATCH (cust:Customer)-[:PURCHASED]->(:Order)-[o:ORDERS]->(p:Product),
  (p)-[:PART_OF]->(c:Category {categoryName:"Produce"})
RETURN DISTINCT cust.contactName as CustomerName, SUM(o.quantity) AS TotalProductsPurchased;

```

### Python

#### py2neo and jupyter notebook

- https://github.com/elena/py2neo-quickstart
- https://community.neo4j.com/t/py2neo-tutorial-converting-movie-example/4458
- http://www.numericalexpert.com/blog/neo4j_python/
- https://nbviewer.jupyter.org/github/versae/ipython-cypher/blob/master/docs/examples.ipynb
- https://link.medium.com/aVCya6Pgneb
- https://nicolewhite.github.io/neo4j-jupyter/hello-world.html
- https://github.com/merqurio/neo4jupyter
- https://community.neo4j.com/t/neo4j-graph-visualization-in-jupyterlab/24219
- Py2neo V4: https://medium.com/neo4j/py2neo-v4-2bedc8afef2
- Py2neo Handbook: https://py2neo.org/2021.0/

#### neo4j-jupyter
installed at ~/projects/graph/graph-db/neo4j/neo4j-jupyter

https://ipython-cypher.readthedocs.io/en/latest/introduction.html


### Learning Resources

- Documentations:
  - [Developer guides](https://neo4j.com/developer/get-started/)
  - [Developer Manual](https://neo4j.com/docs/developer-manual/current/)
  - [Operations Manual](https://neo4j.com/docs/operations-manual/current/)
  - [Neo4j Cypher Refcard](https://neo4j.com/docs/cypher-refcard/4.2/)
  - [The Neo4j Cypher Manual v4.2](https://neo4j.com/docs/cypher-manual/4.2/)

- Training:
  - Intro to Graph Databases series: https://www.youtube.com/playlist?
list=PL9Hl4pk2FsvWM9GWaguRhlCQ-pa-ERd4U
  - Get started : https://neo4j.com/graphacademy/online-training/gettingstarted-graph-databases-using-neo4j/
  - [LearningNeo4j](https://github.com/Wabri/LearningNeo4j)

- Become Neo4j Certified: 
  - https://neo4j.com/graphconnect-2018/session/pass-like-pro-neo4j-certified-professional-exam 
  - https://data-xtractor.com/blog/databases/neo4j-certified-professionals/
  - https://medium.com/neo4j/neo4j-certification-how-to-pass-like-a-proeed6daa7c6f7  (by jennifer.reif@neo4j.com , @JMHReif)



# RedisGraph

https://docs.redis.com/latest/modules/redisgraph/redisgraph-quickstart/