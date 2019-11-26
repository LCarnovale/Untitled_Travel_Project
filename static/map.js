var map;
var markerlist = [];
var circlelist = [];
var geocoder;
var distancevalues = [500,1000,1500,2000,3000,4000,5000,7500,10000,20000];

//Function to create the map in home.html or new_ad.html
function initMap() {
	if (document.getElementById('map')!=null){
		map = new google.maps.Map(document.getElementById('map'), {
		  center: {lat: -33.91538902145825 , lng: 151.11207767686824},
		  zoom: 13
		});
		geocoder = new google.maps.Geocoder;
		google.maps.event.addListener(map, 'click', function( event ){
			document.getElementById("geocodedvalue").value = event.latLng.lat()+", "+event.latLng.lng();
			
			for (i = 0;i<markerlist.length;i++){
				markerlist[i].setMap(null);
				circlelist[i].setMap(null);
			}
			var marker = new google.maps.Marker({position: event.latLng, map: map});
			markerlist.push(marker)
			var circle = new google.maps.Circle({map: map, radius: parseInt(document.getElementById("radiusrange").value), fillColor: '#AA0000'});
			circle.bindTo('center', marker, 'position');
			circlelist.push(circle)
			document.getElementById('radiusval').value = document.getElementById("radiusrange").value
			geocoder.geocode({'location': event.latLng}, function(results, status) {
					if (status === 'OK') {
						if (results[0]) {
							var searchBox = document.getElementById('searchgeocode');
							searchBox.value = results[0].formatted_address;
							document.getElementById("searchBtn").disabled = false; // enable search button
							M.updateTextFields(); // Raise the label in the search box

						} 
						else {
							alert('No results found');
							document.getElementById("searchBtn").disabled = true;
						}
					} 
					else {
						alert('Geocoder failed due to: ' + status);
						document.getElementById("searchBtn").disabled = true;
					}
				});
		});
	}
	else{
		map = new google.maps.Map(
		document.getElementById('map2'), {
			center: {lat: -33.91538902145825 , lng: 151.11207767686824},
			zoom: 13
			}
		);
		geocoder = new google.maps.Geocoder;
		google.maps.event.addListener(
			map, 'click', function( event ) {
				document.getElementById("hiddenlocation").value = event.latLng.lat() + ", " + event.latLng.lng();
				for (i = 0;i<markerlist.length;i++){
					markerlist[i].setMap(null);
				}
				markerlist.length = 0;
				var marker = new google.maps.Marker({position: event.latLng, map: map});
				markerlist.push(marker);
				geocoder.geocode({'location': event.latLng}, function(results, status) {
					if (status === 'OK') {
						if (results[0]) {
							document.getElementById("hiddenaddress").value = results[0].formatted_address;
						} 
						else {
							alert('No results found');
						}
					} 
					else {
						alert('Geocoder failed due to: ' + status);
					}
				});
			}
		);
				
	}
}

//Geocode functions for home.html
function getgeocode(){
			
			geocoder.geocode({
				'address': document.getElementById("searchgeocode").value,
				'componentRestrictions': {
					'country': 'AU'
				}
			}, function(results, status) {
						if (status === 'OK') {
							if (results[0] && results[0].geometry &&
								results[0].geometry.bounds) {
								for (i = 0;i<markerlist.length;i++){
									markerlist[i].setMap(null);
									circlelist[i].setMap(null);
								}
								document.getElementById("geocodedvalue").value = results[0].geometry.location.lat()+", "+results[0].geometry.location.lng();
								var marker = new google.maps.Marker({position: results[0].geometry.location, map: map});
								map.setCenter(results[0].geometry.location);
								markerlist.push(marker);
								console.log(document.getElementById('geocodedvalue').value);
								console.log(results[0].geometry.location);
								var radius = Math.round(google.maps.geometry.spherical.computeDistanceBetween(results[0].geometry.location,results[0].geometry.bounds.getSouthWest()));
								
								var maxdiff= 999999999;
								var currindex = 0;
								for(i = 0; i<distancevalues.length;i++){
									console.log(Math.abs(distancevalues[i]-radius))
									if (Math.abs(distancevalues[i]-radius) < maxdiff){
										console.log('changed')
										maxdiff = Math.abs(distancevalues[i]-radius)
										currindex = i
									}
									console.log(currindex)
								}
								document.getElementById("radiuschange").value = currindex;
								document.getElementById("radiusrange").value = distancevalues[currindex];
								document.getElementById("radiusval").value = distancevalues[currindex];
								var circle = new google.maps.Circle({map: map, radius: distancevalues[currindex], fillColor: '#AA0000'});
								circle.bindTo('center', marker, 'position');
								circlelist.push(circle);
								console.log('Result: ' + results);
								document.getElementById("searchBtn").disabled = false; // enable search button
							} else {
								console.log('No results found');
							}
						} else {
							console.log('Geocoder failed due to: ' + status);
						}
					});
}

//Geocode function for new_ad.html
function getgeocode2(){
	
	geocoder.geocode({
		'address': document.getElementById("hiddenaddress").value,
		'componentRestrictions': {
			'country': 'AU'
		}
	}, function(results, status) {
				if (status === 'OK') {
					if (results[0] && results[0].geometry &&
						results[0].geometry.bounds) {
						for (i = 0;i<markerlist.length;i++){
							markerlist[i].setMap(null);
							circlelist[i].setMap(null);
						}
						document.getElementById("hiddenlocation").value = results[0].geometry.location.lat()+", "+results[0].geometry.location.lng();
						var marker = new google.maps.Marker({position: results[0].geometry.location, map: map});
						map.setCenter(results[0].geometry.location)
						console.log(results[0].geometry.location)
						markerlist.push(marker)
					} else {
						console.log('No results found');
						//alert('No results found');
					}
				} else {
					console.log('Geocoder failed due to: ' + status);
					//alert('Geocoder failed due to: ' + status);
				}
			});
}

//function to update radius of the search
//Parameter = the index on the radius slider input
function updateRadius(newval) {
			document.getElementById("radiusval").value = distancevalues[newval];
}

//function to show the radius of the search in Google Map
//Parameter = the index on the radius slider input
function changeCircle(newval){
	document.getElementById("radiusrange").value = distancevalues[newval];
	for (i = 0;i<circlelist.length;i++){
		if(circlelist[i]==null)
			continue;
		circlelist[i].setRadius(parseInt(distancevalues[newval]));
	}
}

