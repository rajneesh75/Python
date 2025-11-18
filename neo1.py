from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))


def add_friend(tx, name, friend_name):
    tx.run("CREATE (a:Person {name: $name})-[:FRIEND]->(b:Person {name: $friend_name})",
           name=name, friend_name=friend_name)


with driver.session() as session:
    session.execute_write(add_friend, "Rajneesh", "John")

driver.close()
