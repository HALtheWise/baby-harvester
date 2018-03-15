$.urlParam = function(name){
	// Taken from https://www.sitepoint.com/url-parameters-jquery/
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results[1] || 0;
}

function now() {
	return (new Date()).getTime() / 1000.0
}

function print(name, token) {
	console.log('Submitted!')

	$.ajax
		({
		  type: "POST",
		  url: "https://baby-harvester-gateway.herokuapp.com/print/text",
		  dataType: 'json',
		  async: false,
		  headers: {
		    "Authorization": "Basic " + btoa(name + ":" + token)
		  },
		  data: JSON.stringify({
		  	'message':'Time\'s Up!'
		  }),
	      'processData': false,
	      'contentType': 'application/json'
		});

	return false;
}

$( document ).ready(
	function() {
		console.log("Hello World");

		try{
			var duration = parseInt($.urlParam('duration'));
		} catch(err){
			var duration = 10;
		}
		try{
			var name = $.urlParam('name');
			var token = $.urlParam('token');
		} catch(err){
			var name = "";
			var token = "";
		}
		console.log(duration);

		endTime = now() + duration;

		animate = function(argument) {
			t = now();
			console.log(endTime, t);

			dt = endTime - t;
			if (dt > 0){
				dtm = Math.floor(dt/60);
				dts = Math.floor(dt%60)
					.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false});

				$('#time').text(dtm+":"+dts);

				window.requestAnimationFrame(animate);
			} else {
				$('#time').text("Time's Up!");
				$('#time').parent().addClass('done');
				print(name, token);
			}
		}

		window.requestAnimationFrame(
				animate
			)
	}
	)