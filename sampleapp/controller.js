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
		  async: false,
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
		  failure: function(){
		  	alert('Something went wrong');
		  }
		});

	return false;
}