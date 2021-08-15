## Neo4j exercises with Movies Graph DB

neo4j browser URL = http://localhost:7474

:play movies

### shortcuts
- Run queries with CMD (CTRL) + Enter
- Use :clear to clear past results
- CMD (CTRL) + Up Arrow to scroll through past queries

### [Cypher Styles](https://github.com/opencypher/openCypher/blob/master/docs/style-guide.adoc)
- Case Sensitive
    - Node labels (entity types)
    - Relationship types
    - Property keys (attributes)
- Case Insensitive
    - Cypher keywords
    
- Cypher keywords and clauses should be written in all caps and on their own line
- Functions should be written in lower camel case.


### MATCH (Read/Query) - (R)

// query
MATCH (m:Movie)
RETURN m;

MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
RETURN p, r, m;

// variable
MATCH p = (:Person)-[:ACTED_IN]->(:Movie)
RETURN p;

// filter
MATCH (p:Person)
WHERE p.name = 'Tom Hanks'
RETURN p;

// WHERE with pattern
MATCH (p:Person)-[:WROTE]->(m:Movie)
WHERE (p)-[:PRODUCED]->(m)
RETURN p.name, m.title;

// WHERE NOT
MATCH (p:Person)-[:WROTE]->(m:Movie)
WHERE NOT (p)-[:PRODUCED]->(m)
RETURN p.name, m.title;

MATCH (p:Person)
WHERE NOT (p)-[:ACTED_IN|:DIRECTED]->(:Movie)
RETURN p;


// string functions
MATCH (m:Movie)
WHERE m.title STARTS WITH 'The Matrix'
RETURN m.title;

MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name STARTS WITH 'To'
RETURN p, m;

// multiple Rel types
MATCH (p:Person)-[r:ACTED_IN|:DIRECTED]->(m:Movie)
WHERE p.name = 'Danny DeVito'
RETURN p.name, r, type(r), m.title;


MATCH (m:Movie)
WHERE m.title CONTAINS 'Matrix'
RETURN m.title;

MATCH (m:Movie)
WHERE m.title ENDS WITH 'Seattle'
RETURN m.title;

// regex
MATCH (m:Movie)
WHERE m.title =~ '.*[0-9].*'
RETURN m.title;

// aggregate, order by, limit
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
RETURN p.name, count(*) AS movies
ORDER BY movies DESC
LIMIT 5;

// multiple match - co-actors with Meg Ryan
MATCH (p:Person)-[:ACTED_IN]->(m:Movie),
      (other:Person)-[:ACTED_IN]->(m)
WHERE p.name = 'Meg Ryan'
RETURN other.name, m.title
ORDER BY other.name;

// multiple match
MATCH (p:Person)-[:ACTED_IN]->(m:Movie),
      (other:Person)-[:ACTED_IN]->(m),
      (director:Person)-[:DIRECTED]->(m)
WHERE p.name = 'Meg Ryan'
RETURN m.title AS movie, 
       director.name AS director,
       other.name AS coActor;

// OPTINOAL MATCH
MATCH (p:Person)
WHERE p.name STARTS WITH 'Tom'
OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)
RETURN p.name, m.title;

// WITH Clause
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WITH p, collect(m.title) AS movies
WHERE size(movies) > 5
RETURN p.name, movies;

// WITH Clause
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WITH p, m
ORDER BY m.title
WITH p, collect(m.title) AS movies
WHERE size(movies) > 5
RETURN p.name, movies;

// Get the two oldest people and their three most recent movies.
MATCH (actor:Person) 
WITH actor 
ORDER BY actor.born 
LIMIT 2 
MATCH (actor)-[:ACTED_IN]->(movie:Movie) 
WITH actor, movie 
ORDER BY movie.released DESC 
RETURN actor.name, 
       2016 - actor.born AS age, 
       collect(movie.title)[..3] AS movies;



// distinct
MATCH (p:Person)-[:ACTED_IN]->(m:Movie),
      (other:Person)-[:ACTED_IN]->(m)
WHERE p.name = 'Meg Ryan'
RETURN DISTINCT other.name;

// collect to array - movie title and actor list
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE m.title STARTS WITH 'The Matrix'
RETURN m.title, collect(p.name) AS actors;

// size - top 5 producers
MATCH (p:Person)
RETURN p.name, 
       size((p)-[:PRODUCED]->(:Movie)) AS prod
ORDER BY prod DESC
LIMIT 5;

// person produced more than 5 titles
MATCH (p:Person)
WHERE size((p)-[:PRODUCED]->(:Movie)) > 5
RETURN p.name;

// Find the top five actors by how many movies they’ve acted in and movies they’ve directed, if any
MATCH (p:Person)
WITH p, size((p)-[:ACTED_IN]->(:Movie)) AS movies
ORDER BY movies DESC
LIMIT 5
OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)
RETURN p.name, m.title;

// UNWIND: list into row
WITH [1, 2, 3] AS list
RETURN list;

WITH [1, 2, 3] AS list
UNWIND list AS row
RETURN row;

MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WITH p, m
ORDER BY m.released
WITH p, collect(m)[..3] AS topThree
UNWIND topThree AS m
MATCH (dir:Person)-[:DIRECTED]->(m)
RETURN p.name, m.title, dir.name;

// Variable length paths
MATCH p = (p1:Person)-[:ACTED_IN*..4]-(p2:Person)
WHERE p1.name = 'Tom Cruise' AND      
      p2.name = 'Kevin Bacon'
RETURN p;

MATCH p = (p1:Person)-[:ACTED_IN*4..6]-(p2:Person)
WHERE p1.name = 'Tom Hanks' AND      
      p2.name = 'Kevin Bacon'
RETURN p;

MATCH p = (p1:Person)-[:ACTED_IN*4..6]-(p2:Person)
WHERE p1.name = 'Tom Cruise' AND            
      p2.name = 'Kevin Bacon'
RETURN [x IN nodes(p) |  
  CASE WHEN x:Person THEN x.name       
       WHEN x:Movie  THEN x.title  
  ELSE '' END
];

// shortest path between 2 actors
MATCH p = shortestPath((p1:Person)-[*]-(p2:Person))
WHERE p1.name = 'Tom Cruise' AND      
      p2.name = 'Kevin Bacon'
RETURN p;

// shortest path between two movies via any rel type
MATCH p = shortestPath((m1:Movie)-[*]-(m2:Movie))
WHERE m1.title = 'Top Gun' AND      
      m2.title = 'The Matrix'
RETURN p;

// Bacon_Number
MATCH p = shortestPath((c:Person)-[:KNOWS*]->(bacon:Person))
WHERE c.name = 'Charlize Theron' AND      
      bacon.name = 'Kevin Bacon'
RETURN length(p) AS Bacon_Number, [n IN nodes(p) | n.name] AS Names;

// Recommend: 3 actors that Keanu Reeves should work with, but hasn’t
MATCH (p:Person)-[:ACTED_IN]->()<-[:ACTED_IN]-(c),
(c)-[:ACTED_IN]->()<-[:ACTED_IN]-(coc)
WHERE p.name = 'Keanu Reeves' 
	AND coc <> p
 	AND NOT (p)-[:ACTED_IN]->()<-[:ACTED_IN]-(coc) 
RETURN coc.name as Colleague_of_colleague, count(coc) as 
Weight
ORDER BY Weight DESC
LIMIT 3;


### CREATE & MERGE/Update (Write) - (C) (U)

// CREATE (INSERT)
CREATE (m:Movie {title:'Mystic River', released:2003})
RETURN m;

// CREATE Rel
MATCH (m:Movie {title: 'Mystic River'})
MATCH (p:Person {name: 'Kevin Bacon'})
CREATE (p)-[r:ACTED_IN {roles: ['Sean']}]->(m)
RETURN p, r, m;



// SET (UPDATE)
MATCH (m:Movie {title: 'Mystic River'})
SET m.tagline = 'We bury our sins here, Dave. We wash them clean.' 
RETURN m;

// MERGE
MERGE (p:Person {name: 'Tom Hanks'})
RETURN p;

// Update node property
MERGE (p:Person {name: 'Tom Hanks', oscar: true})
RETURN p;

MERGE (p:Person {name: 'Tom Hanks'})
SET p.oscar = true
RETURN p;

// Create a new movie and rel
MERGE (p:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m:Movie {title: 'The Terminal'})
RETURN p, m;

MERGE (p:Person {name: 'Tom Hanks'})
MERGE (m:Movie {title: 'The Terminal'})
MERGE (p)-[r:ACTED_IN]->(m)
RETURN p, r, m;

// MERGE ON CREATE / ON MATCH
MERGE (p:Person {name: 'Your Name'})
  ON CREATE SET p.created = timestamp(),
                p.updated = 0 
  ON MATCH SET p.updated = p.updated + 1
RETURN p.created, p.updated;

// Create KNOWS relationships between all actors who have worked together on the same movie
MATCH (a:Person)-[:ACTED_IN]->()<-[:ACTED_IN]-(b:Person)
MERGE (a)-[:KNOWS]-(b);

MATCH (a:Person)-[:ACTED_IN]->()<-[:ACTED_IN]-(b:Person)
MERGE (a)-[:KNOWS]->(b)
MERGE (a)<-[:KNOWS]-(b);



### Modeling (M)

// Labels are upper camel case.
- CREATE(n:Person);
- CREATE(n:GraphDatabase);
- CREATE(n:VeryDescriptiveLabel);

// Relationships are upper case with underscores to separate words.
- CREATE(n)-[:LOVES]->(m);
- CREATE(n)-[:REALLY_LOVES]->(m);
- CREATE(n)-[:IS_IN_LOVE_WITH]->(m);

// Properties are written in lower camel case
CREATE(n)
SET n.name = ’Dave';

CREATE(n)
SET n.firstName = ’Dave';
 
CREATE(n)
SET n.firstAndLastName = ’Dave Gordon';

// Adding Movie Genres
// Should we model them as properties or as nodes?

// Adding Genres As Properties
MATCH (m:Movie {title: 'The Matrix'})
SET m.genre = ['Action', 'Sci-Fi']
RETURN m;

// Pro: Accessing the genres of a movie is quick and easy
MATCH (m:Movie {title:"The Matrix"})
RETURN m.genre;

// Con: Finding movies that share genres is painful and we have a disconnected pattern in the MATCH clause—a sure sign you have a modeling issue
MATCH (m1:Movie), (m2:Movie)
WHERE any(x IN m1.genre WHERE x IN m2.genre)
      AND m1 <> m2
RETURN m1, m2;

// Adding Genres As Nodes
MATCH (m:Movie {title:"The Matrix"})
MERGE (action:Genre {name:"Action"})
MERGE (scifi:Genre {name:"Sci-Fi"})
MERGE (m)-[:IN_GENRE]->(action)
MERGE (m)-[:IN_GENRE]->(scifi);

// Pro: Finding movies that share genres is a natural graph pattern
MATCH (m1:Movie)-[:IN_GENRE]->(g:Genre),
      (m2:Movie)-[:IN_GENRE]->(g)
RETURN m1, m2, g;

// Con: Accessing the genres of a movie requires a bit more typing
MATCH (m:Movie {title:"The Matrix"}),
      (m)-[:IN_GENRE]->(g:Genre)
RETURN g.name;

### DELETE (D)

MATCH (p:Person {name: 'Emil Eifrem'})
DELETE p;

MATCH (p:Person {name: 'Emil Eifrem'})
DETACH DELETE p;


### CONSTRAINT and INDEX


:schema 

// unique
CREATE CONSTRAINT ON (p:Person) ASSERT p.name IS UNIQUE;

// exists
CREATE CONSTRAINT ON (p:Person) ASSERT exists(p.name);

// INDEX
CREATE INDEX ON :Person(born);
CREATE INDEX ON :Movie(released);

### Data Import

// Clear Database before load
MATCH (n) DETACH DELETE n;

// prepare .csv files
- movies.csv: id, title, country, year
- persons.csv: id, name
- roles.csv: personid, movieid, role


// Create Constrain first
- CREATE CONSTRAINT ON (n:Movie) ASSERT n.id IS UNIQUE;
- CREATE CONSTRAINT ON (n:Person) ASSERT n.id IS UNIQUE;

// Load
LOAD CSV WITH HEADERS 
FROM "http://neo4j.com/docs/stable/csv/intro/movies.csv"
AS line
RETURN line;

LOAD CSV WITH HEADERS 
FROM "http://neo4j.com/docs/stable/csv/intro/movies.csv"
AS line
RETURN line.title, line.year;

// Load movies
LOAD CSV WITH HEADERS 
FROM "http://neo4j.com/docs/stable/csv/intro/movies.csv"
AS line
CREATE (m:Movie {id: toInt(line.id)})
SET m.title = line.title,
    m.released = toInt(line.year)
RETURN m;

// Load persons
LOAD CSV WITH HEADERS 
FROM "http://neo4j.com/docs/stable/csv/intro/persons.csv"
AS line
CREATE (p:Person {id: toInt(line.id)})
SET p.name = line.name
RETURN p;

// Load roles
LOAD CSV WITH HEADERS 
FROM "http://neo4j.com/docs/stable/csv/intro/roles.csv"
AS line
MATCH (actor:Person {id: toInt(line.personId)})
MATCH (movie:Movie {id: toInt(line.movieId)})
CREATE (actor)-[acted:ACTED_IN]->(movie)
SET acted.roles = line.role
RETURN actor, acted, movie;


### Stored Procedures

// docs
- http://neo4j.com/docs/developer-manual/current/#procedures
- https://github.com/neo4j-contrib/neo4j-apoc-procedures


// Built in Procedures
- CALL db.schema.visualization();
- CALL db.labels();
- CALL db.relationshipTypes();
- CALL db.propertyKeys();


// User-defined procedures are written in Java, deployed into the database, and called from Cypher

CALL org.neo4j.examples.findDenseNodes(1000);






