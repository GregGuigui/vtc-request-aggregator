var app = new Vue({
	el: '#app',
	data: {
		loading: false,
		results: [],
		placeFrom: null,
		placeTo: null
	},
	methods: {
		loadResults: function() {
			this.loading = true;
			if (this.placeFrom && this.placeTo) {
				var p1 = this.$http.get('/api/products', {
					params: {
						lat: this.placeFrom.lat(),
						lng: this.placeFrom.lng()
					}
				}).then(function(response) {
					this.results = response.body;
					this.loading = false;
					console.log(this.results);
				});
			}
		},
		updateEstimateTime: function() {
			if (this.placeFrom && this.placeTo && this.results.length) {
				var p2 = this.$http.get('/api/pickuptimes', {
					params: {
						lat: this.placeFrom.lat(),
						lng: this.placeFrom.lng()
					}
				}).then(function(response) {
					var estimates = response.body;
					var newResults = [];
					this.results.forEach(function(r) {
						var e = estimates.find(function(f) {
							return f.product_id === r.product_id;
						});
						if (e) {
							r.estimate_pickuptime = e.estimate
						}
						newResults.push(r);
					});
					this.results = newResults;
				});
			}
		},
		updateEstimatePrice: function(callback) {
			if (this.placeFrom && this.placeTo && this.results.length) {
				var p2 = this.$http.get('/api/prices', {
					params: {
						start_lat: this.placeFrom.lat(),
						start_lng: this.placeFrom.lng(),
						end_lat: this.placeTo.lat(),
						end_lng: this.placeTo.lng()
					}
				}).then(function(response) {
					var estimates = response.body;
					var newResults = [];
					this.results.forEach(function(r) {
						var e = estimates.find(function(f) {
							return f.product_id === r.product_id;
						});
						if (e) {
							r.estimate = e.estimate;
							r.duration = e.duration;
							r.distance = e.distance;
						}
						newResults.push(r);
					});
					this.results = newResults;
					
					if(callback){
						callback();
					}
				});
			}
		},
		setPlaces(from, to) {
			this.placeFrom = from;
			this.placeTo = to;
		}
	},
	created: function(){
		var that = this;
		window.setInterval(function(){
			that.updateEstimatePrice(this.updateEstimateTime);
		}, 5000);
	}
})

var map,
	autocompleteFrom,
	autocompleteTo,
	placeFrom,
	placeTo,
	userPosition;

function initMap() {
	var directionsService = new google.maps.DirectionsService;
	var directionsDisplay = new google.maps.DirectionsRenderer;

	var latlng = {
		lat: 48.862169,
		lng: 2.336826
	};
	if (userPosition) {
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
		placeFrom = autocompleteFrom.getPlace() || placeFrom;
		placeTo = autocompleteTo.getPlace();
		calculateAndDisplayRoute(placeFrom, placeTo, directionsService, directionsDisplay);
	};
	autocompleteFrom.addListener('place_changed', onChangeHandler);
	autocompleteTo.addListener('place_changed', onChangeHandler);
}

function calculateAndDisplayRoute(placeFrom, placeTo, directionsService, directionsDisplay) {
	if (!placeFrom || !placeTo) {
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
		}
		else {
			window.alert('Directions request failed due to ' + status);
		}
	});
}

function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(showPosition);
	}
}

function showPosition(position) {
	if (map) {
		map.setCenter({
			lat: position.coords.latitude,
			lng: position.coords.longitude
		})
	}
	geocodePosition(position);
}

function geocodePosition(position) {
	$.ajax({
		url: 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' +
			position.coords.latitude + ',' +
			position.coords.longitude + '&key=AIzaSyBBGLst2_5aTRSKZRw0RglUN0dX_Qtao60',
	}).done(function(response) {
		$("#from").val(response.results[0].formatted_address);
		placeFrom = response.results[0];
		placeFrom.geometry.location = new google.maps.LatLng(placeFrom.geometry.location.lat, placeFrom.geometry.location.lng);
	});
}

getLocation();
