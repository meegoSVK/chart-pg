$(document).ready(function() {

	/**
	 * call the data.php file to fetch the result from db table.
	 */
	var SensID = document.getElementById('sensID').value;
	$.ajax({
		url : "http://localhost/graphs/api/temperature-data-pg.php?id="+SensID,
		type : "GET",
		success : function(data){
			console.log(data);

			var temperature = {
				Sensor1 : [],
				Sensor2 : []
			};
			
			var timestamp = {
				Sensor1 : [],
				Sensor2 : []	
			};
			
			var nazov = {
				Sensor1 : data[0].name,
				Sensor2 : data[1].name
			};
			
			var len = data.length;

			for (var i = 0; i < len; i++) {
				if (data[i].name == nazov.Sensor1) {
					temperature.Sensor1.push(data[i].temperature);
				}
				else if (data[i].name == nazov.Sensor2) {
					temperature.Sensor2.push(data[i].temperature);
				}
			}
			
			for (var i = 0; i < len; i++) {
				if (data[i].name == nazov.Sensor1) {
					timestamp.Sensor1.push(data[i].timestamp);
				}
				else if (data[i].name == nazov.Sensor2) {
					timestamp.Sensor2.push(data[i].timestamp);
				}
			}

			//get canvas
			var ctx = $("#line-chartcanvas");

			var data = {
				labels :  timestamp.Sensor1 ,
				datasets : [
					{
						label : nazov.Sensor1,
						data : temperature.Sensor1,
						backgroundColor : "blue",
						borderColor : "lightblue",
						fill : false,
						lineTension : 0,
						pointRadius : 5
					},
					{
						label : nazov.Sensor2,
						data : temperature.Sensor2,
						backgroundColor : "green",
						borderColor : "lightgreen",
						fill : false,
						lineTension : 0,
						pointRadius : 5
					}
				]
			};

			var options = {
					responsive: true,
				title : {
					display : true,
					position : "top",
					text : "Vyvoj teplot pre senzor ",
					fontSize : 18,
					fontColor : "#111"
				},
				legend : {
					display : true,
					position : "bottom"
				}
			};

			var chart = new Chart( ctx, {
				type : "line",
				data : data,
				options : options
			} );

		},
		error : function(data) {
			console.log(data);
		}
	});

});