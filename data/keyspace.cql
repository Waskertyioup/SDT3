-- https://gist.github.com/derlin/0d4c98f7787140805793d6268dae8440
-- https://www.tutorialspoint.com/cassandra/cassandra_create_keyspace.htm

create keyspace pacientes with replication = {'class': 'SimpleStrategy', 'replication_factor': '2'};
create keyspace recetas with replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};