var app = new Vue({
  el: '#app',
  data: {
    results: [{
	  distance: 50,
	  type: 'UberX',
	  price: '30 €'
	}, {
	  distance: 30,
	  type: 'Le Cab pool',
	  price: '25 €'
	}],
	placeFrom: null,
	placeTo: null
  },
  methods: {
	  loadResults: function(){
		  console.log(this.placeFrom);
		  console.log(this.placeTo);
		  
		  if(this.placeFrom && this.placeTo){			  
			  this.results = [{
				  distance: Math.round(Math.random() * 40),
				  type: 'UberX',
				  price: '30 €'
			  }];
		  }
	  },
	  setPlaces(from, to){
		  this.placeFrom = from;
		  this.placeTo = to;
	  }
  }
})
	
var map,
	autocompleteFrom, 
	autocompleteTo,
	userPosition;

function initMap() {
	var directionsService = new google.maps.DirectionsService;
	var directionsDisplay = new google.maps.DirectionsRenderer;
	
	var latlng = {lat: 0, lng: 0};
	if(userPosition){
		latlng.lat = userPosition.coords.latitude;
		latlng.lng = userPosition.coords.longitude;
	}
	
	map = new google.maps.Map(document.getElementById('map'), {
		center: latlng,
		zoom: 13
	});
	directionsDisplay.setMap(map);

	var inputFrom = $('#from');
	var inputTo = $('#to');

	autocompleteFrom = new google.maps.places.Autocomplete(inputFrom[0]);
	autocompleteTo = new google.maps.places.Autocomplete(inputTo[0]);
	
	var onChangeHandler = function() {		
		var placeFrom = autocompleteFrom.getPlace();
		var placeTo = autocompleteTo.getPlace();
		calculateAndDisplayRoute(placeFrom, placeTo, directionsService, directionsDisplay);
	};
	autocompleteFrom.addListener('place_changed', onChangeHandler);
	autocompleteTo.addListener('place_changed', onChangeHandler);
}

function calculateAndDisplayRoute(placeFrom, placeTo, directionsService, directionsDisplay) {
	if(!placeFrom || !placeTo){
	  return;
	}
	
	directionsService.route({
		origin: placeFrom.geometry.location,
		destination: placeTo.geometry.location,
		travelMode: google.maps.TravelMode.DRIVING
	}, 
	function(response, status) {
		if (status === google.maps.DirectionsStatus.OK) {
		  directionsDisplay.setDirections(response);
		  
		  // load cab results from vuejs
		  app.setPlaces(placeFrom.geometry.location, placeTo.geometry.location);
		  app.loadResults();
		} else {
		  window.alert('Directions request failed due to ' + status);
		}
	});
}

function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(showPosition);
	} else {
		x.innerHTML = "Geolocation is not supported by this browser.";
	}
}

function showPosition(position) {
	userPosition = position;
	if(map){		
		map.setCenter({
			lat: userPosition.coords.latitude,
			lng: userPosition.coords.longitude
		})
	}
}

getLocation();