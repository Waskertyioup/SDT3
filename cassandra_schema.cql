-- https://www.tutorialspoint.com/cassandra/cassandra_create_table.htm

CREATE TABLE pacientes (
  id int PRIMARY KEY,
  nombre text,
  apellido text,
  rut text,
  email text,
  fecha_nacimiento text;
  )

CREATE TABLE recetas (
  id int PRIMARY KEY,
  id_paciente int,
  comentario text,
  farmacos text,
  doctor text;
  )