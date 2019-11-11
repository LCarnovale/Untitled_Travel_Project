var map;
function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
	  center: {lat: -33.91538902145825 , lng: 151.11207767686824},
	  zoom: 13
	});
	google.maps.event.addListener(map, 'click', function( event ){
		document.getElementById("hiddenlocation").value = event.latLng.lat()+", "+event.latLng.lng();
		console.log(document.getElementById("hiddenlocation")); 
	});
}