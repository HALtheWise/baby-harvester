function submitted() {
	console.log('Submitted!')

	var USERNAME = $('#name').val()
	var PASSWORD = $('#password').val()
	var duration = $('#duration').val()

	$.ajax
		({
		  type: "POST",
		  url: "https://baby-harvester-gateway.herokuapp.com/display/url",
		  dataType: 'json',
		  async: true,
		  headers: {
		    "Authorization": "Basic " + btoa(USERNAME + ":" + PASSWORD)
		  },
		  data: JSON.stringify({
		  	'message':'https://halthewise.github.io/baby-harvester/sampleapp/timer.html?duration='+duration
		  }),
	      'processData': false,
	      'contentType': 'application/json',
		  
		  success: function (){
		    alert('Thanks for your comment!'); 
		  },
		  error: function(){
		  	alert('Something went wrong, do you have the correct token?');
		  }
		});

	return false;
}