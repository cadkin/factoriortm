// Set path information here.
var mapSeed = 1234567890
var gamePath = "factorio/"

//---------------------------

/*
// Check for new position every second.
setInterval(function() {
   $.ajax({
        url: "./tmp",
        async: true,
        dataType: "text",
        success: function(data) {
            console.log(data);
        },
        error: function() {
            console.log("Error");
        }
   });
}, 1000)
*/

var loadBoundary = function ()
{
	var qs = window.location.search;
	if (qs.length > 1) {
		qs = qs.substring(1);
		qs = qs.split(',');
	}
	if (qs.length === 3) {
		qs[0] = Number.parseFloat(qs[0]);
		qs[1] = Number.parseFloat(qs[1]);
		qs[2] = Number.parseInt(qs[2]);
	} else {
		qs = [0, 0, 10] // Set default center and zoom here
	}

	return qs;
}

var saveBoundary = function ()
{
	var center = mymap.getCenter();
	var zoom = Number.parseFloat(mymap.getZoom()).toPrecision(1);
	var url = '?' + center.lat.toPrecision(5) + ',' + center.lng.toPrecision(5) + ',' + zoom;
	window.history.replaceState({}, '', url);
}

var b = loadBoundary();
console.log(b);

var mymap = L.map(
	'mapid', {
		crs: L.CRS.Simple,
		maxZoom: 10,
		minZoom: 1,
		wheelPxPerZoomLevel: 500
	}).setView([b[0], b[1]], b[2]);

mymap.on('moveend', function (e) {
	saveBoundary();
});

// Set the tiles.
L.tileLayer(gamePath + "/script-output/mapdata/" + mapSeed + "/leaflet/{z}/{y}/{x}.jpg").addTo(mymap);

