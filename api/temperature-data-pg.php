<?php
/**
 * filename: temperature-data-pg.php
 * description: Vrati hodnoty z databazky
 */

//setting header to json
header('Content-Type: application/json');

//get connection

$pgsql = pg_connect("host=localhost port=5432 dbname=test user=test password=test");

if(!$pgsql){
	die("Connection failed: " . $pgsql->error);
}


$sensorid = $_GET["id"];

//query to get data from the table

$query = sprintf("SELECT name, timestamp, temperature FROM pohlad where sensid=%s order by timestamp;", $sensorid);

//execute query
$result = pg_query($pgsql, $query);

$fetch = pg_fetch_all($result);


//loop through the returned data
$data = array();
foreach ($fetch as $row) {
	$data[] = $row;
}

//close connection
pg_close($pgsql);

//now print the data
print json_encode($data);