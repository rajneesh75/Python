from neo4j import GraphDatabase

uri = "bolt://localhost:7687"        # or from Aura dashboard
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

with driver.session() as session:
    session.run("CREATE (n:Person {name:'Tinu'})")
    result = session.run("MATCH (n:Person) RETURN n.name AS name")
    for record in result:
        print(record["name"])

driver.close()