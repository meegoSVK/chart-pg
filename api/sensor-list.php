<?php
/**
 * filename: temperature-data-pg.php
 * description: Vrati hodnoty z databazky
 */

//setting header to json
header('Content-Type: application/json');

//get connection

$dbconn = pg_connect("host=localhost port=5432 dbname=test user=test password=test");

if(!$dbconn){
	die("Connection failed: " . $dbconn->error);
}

if(!isset($_POST['searchTerm'])){
    $fetchData = pg_query($dbconn,"select * from sensors order by sensor limit 5");
}else{
    $search = $_POST['searchTerm'];
    $fetchData = pg_query($dbconn,"select * from sensors where sensor_name like '%".$search."%' limit 5");
}

$sensor_list = array();
while ($row = pg_fetch_array($fetchData)) {
    $sensor_list[] = array("id"=>$row['sensor'], "text"=>$row['sensor_name']);
}

//close connection
pg_close($dbconn);

//now print the data
print json_encode($sensor_list);