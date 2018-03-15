$.urlParam = function(name){
	// Taken from https://www.sitepoint.com/url-parameters-jquery/
	var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	return results[1] || 0;
}

function now() {
	return (new Date()).getTime() / 1000.0
}

$( document ).ready(
	function() {
		console.log("Hello World");

		try{
			duration = parseInt($.urlparam('duration'));
		} catch(err){
			duration = 10;
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
			}
		}

		window.requestAnimationFrame(
				animate
			)
	}
	)