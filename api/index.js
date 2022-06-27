const express = require("express");
const cors = require('cors');



const app = express();

const port = 3000;


app.use(cors());
app.use(express.json());

let cassandra = require('cassandra-driver');
 // Replace 'Username' and 'Password' with the username and password from your cluster settings
let authProvider = new cassandra.auth.PlainTextAuthProvider('cassandra', 'cassandra');
// Replace the PublicIPs with the IP addresses of your clusters
let contactPoints = ['127.0.0.1:9042','127.0.0.1:9043','127.0.0.1:9044'];
// Replace DataCenter with the name of your data center, for example: 'AWS_VPC_US_EAST_1'

let client1 = new cassandra.Client({contactPoints: contactPoints, authProvider: authProvider, keyspace:'pacientes'});

let client2 = new cassandra.Client({contactPoints: contactPoints, authProvider: authProvider, keyspace:'recetas'});



app.get("/", (req, res) => {
  res.send("Hello World!");
});


app.get("/all", (req, res) => {
  const query = 'SELECT * FROM pacientes';
  client1.eachRow(query, [], { autoPage: true }, function (n, row) {
    // This function will be invoked per each of the rows in all the table
  });
});

app.get("/keyspaces", (req, res) => {
  const query = 'SELECT * FROM system_schema.keyspaces';
  client1.execute(query).then(result => console.log('', result.rows[0]));
});

app.get("/create", (req, res) => {
  const query = 'SELECT * FROM recetas';
  client2.execute(query).then(result => console.log('', result.rows[0]));
});


/*

      - ./cassandra_schema.cql:/schema.cql
    command: /bin/bash -c "echo loading cassandra keyspace && cqlsh cassandra -f /schema.cql"

app.get("/test", (req, res) => {

    // Define and execute the queries
    let query = 'SELECT name, price_p_item FROM grocery.fruit_stock WHERE name=? ALLOW FILTERING';
    let q1 = client.execute(query, ['oranges']).then(result => {console.log('The cost per orange is ' + result.rows[0].price_p_item);}).catch((err) => {console.log('ERROR oranges:', err);});
    let q2 = client.execute(query, ['pineapples']).then(result => {console.log('The cost per pineapple is ' + result.rows[0].price_p_item);}).catch((err) => {console.log('ERROR pineapples:', err);});
    let q3 = client.execute(query, ['apples']).then(result => {console.log('The cost per apple is ' + result.rows[0].price_p_item);}).catch((err) => {console.log('ERROR apples:', err);});
    
    // Exit the program after all queries are complete
    Promise.allSettled([q1,q2,q3]).finally(() => client.shutdown());
});

*/


app.listen(port, () => {
  console.log(`http://localhost:${port}`);
});
