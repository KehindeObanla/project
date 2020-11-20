mapboxgl.accessToken = 'pk.eyJ1Ijoia2VoaW5kZW9iYW5sYSIsImEiOiJja2ZuNm42b3kxamwzMndrdXIyNHkzOG8wIn0.qe4TrmVMMfi1Enpcvk5GfQ';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-69.0297, 7.61],
    zoom: 2,
    attributionControl: true,
    preserveDrawingBuffer: true,
});

// handles click/touch event across devices 
let touchEvent = 'ontouchstart' in window ? 'touchstart' : 'click';

// navigation controls
map.addControl(new mapboxgl.NavigationControl()); // zoom controls

// scale bar
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 90,
    unit: 'imperial',
    position: 'bottom-right'
}));

// geolocate control
map.addControl(new mapboxgl.GeolocateControl());

//This overides the Bootstrap modal "enforceFocus" to allow user interaction with main map
$.fn.modal.Constructor.prototype.enforceFocus = function() {};

// Geocoder API
// Geocoder API
// Geocoder API
var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken
});

var addressTool = document.getElementById('addressAppend');
addressTool.appendChild(geocoder.onAdd(map))
var deleteLayer = [];
map.on('load', function() {
    map.addSource('geocode-point', {
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": []
        }
    });

    map.addLayer({
        "id": "geocode-point",
        "source": "geocode-point",
        "type": "circle",
        "paint": {
            "circle-radius": 20,
            "circle-color": "dodgerblue",
            'circle-opacity': 0.5,
            'circle-stroke-color': 'white',
            'circle-stroke-width': 3,
        }
    });

    geocoder.on('result', function(ev) {
        map.getSource('geocode-point').setData(ev.result.geometry);
    });

});

//Enter Lat Long
//Enter Lat Long
//Enter Lat Long

map.on('load', function() {

    $(document).ready(function() {


        //clear
        $('#findLLButtonClear').click(function() {

            map.removeLayer("enterLL");
            map.removeSource("enterLL");

            if (map.getLayer("enterLL")) {
                map.removeLayer("enterLL");
                map.removeSource("enterLL");
            }

        });

        //create
        $('#findLLButton').click(function() {

            var enterLng = +document.getElementById('lngInput').value
            var enterLat = +document.getElementById('latInput').value

            var enterLL = turf.point([enterLng, enterLat]);

            map.addSource('enterLL', {
                type: 'geojson',
                data: enterLL
            });

            map.addLayer({
                id: 'enterLL',
                type: 'circle',
                source: 'enterLL',
                layout: {

                },
                paint: {
                    "circle-color": 'red',
                    "circle-radius": 8,
                },
            });

            map.flyTo({
                center: [enterLng, enterLat]
            });

        });
    });
});
//random string generator
//random string generator
//random string generator
/*https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript */
function makeid(length, uniqueue) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    result += uniqueue;
    for (var i = 0; i < length; i++) {

        result += characters.charAt(Math.floor(Math.random() * charactersLength));

    }
    return result;
}
/* https://stackoverflow.com/questions/1484506/random-color-generator */
/* random color generator */
/* random color generator */
/* random color generator */
/* random color generator */
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
//enter Lat Long for nearest neghibour
//enter Lat Long for nearest neghibour
//enter Lat Long for nearest neghibour

//clear nearest neghibour lat lng
$('#findClearNearest').click(function() {
    $("#lngInputs").val('');
    $("#latInputs").val('');
    lineAnswers = document.getElementById('latlngonclick');
    lineAnswers.innerHTML = " ";


    document.getElementById("addPolygon").checked = false;

});
// find nearest and load layer
$('#findNearest').click(function() {

    var enterLng = $("#lngInputs").val()
    var enterLat = $("#latInputs").val()

    var enterLL = turf.point([enterLng, enterLat]);
    /* generate a unique layer id */
    var random = 'near'
    var generate = makeid(6, random);
    paint = getRandomColor();
    deleteLayer.push(generate)
    $.getJSON("http://localhost:8080/nearestNeighbors/?lngLat=" + enterLng + "," + enterLat)
        .done(function(json) {


            map.addSource(generate, {
                'type': 'geojson',
                'data': json
                    // poly
            });
            map.addLayer({
                'id': generate,
                'source': generate,
                'type': 'circle',
                'paint': {
                    'circle-radius': 6,
                    'circle-color': paint
                }
            });
            if (document.getElementById("addPolygon").checked == true) {
                addpolygonlayer(addPolygon(json))

            }

        });

    map.flyTo({
        center: [enterLng, enterLat],
        zoom: 8
    });


});


// function to add polygon to nearest points
function addPolygon(feature) {
    // creates a bbox for the given geojson
    var hull = turf.concave(feature);
    var bbox = turf.bbox(feature);
    //creates a polygon with the bouning box
    var poly = turf.bboxPolygon(bbox);
    return hull;
}
// adds a layer for a polygon
function addpolygonlayer(json) {
    paint = getRandomColor();
    /* generate a unique layer id */
    var random = 'near'
    var generate = makeid(6, random);
    deleteLayer.push(generate)
    map.addSource(generate, {
        'type': 'geojson',
        'data': json
            // poly
    });
    map.addLayer({
        'id': generate,
        'type': 'fill',
        'source': generate,
        'paint': {
            'fill-color': paint,
            'fill-opacity': 0.7
        },
        'filter': ['==', '$type', 'Polygon']
    });

}
// draw line between two points and calc distance
// draw line between two points and calc distance
// draw line between two points and calc distance

// hides drop down menu for city A and B
$('#CitySelectA').hide();
$('#CitySelectB').hide();
// clear texbox for selected state A And B
$("#clearCity").click(function(event) {
    $("#PickCityA").val("");
    $('#CitySelectA').html("");
    $("#PickCityB").val("");
    $('#CitySelectB').html("");
    lineAnswers = document.getElementById('calculated-length2');
    lineAnswers.innerHTML = '<p>'
    '</p>';

});
// populates drop down menu for City A when search is clicked
$("#searchACity").click(function(event) {
    populateCitySelectA()
});
// populates drop down menu for City B when search is clicked
$("#searchBCity").click(function(event) {
    populateCitySelectB()
});
// when a drop down is clicked it populates the textbox with clicked value
// and hides the drop down for city A
$("#CitySelectA").click(function(event) {
    let city = $("#CitySelectA option:selected").text();
    $("#PickCityA").val(city);
    $('#CitySelectA').hide();
});
// when a drop down is clicked it populates the textbox with clicked value
// and hides the drop down for city B
$("#CitySelectB").click(function(event) {
    let city = $("#CitySelectB option:selected").text();
    $("#PickCityB").val(city);
    $('#CitySelectB').hide();
});
// check for the radio button that is clicked
//and return a clicked value
function RadioValue() {
    var ele = document.getElementsByName('units');

    for (i = 0; i < ele.length; i++) {
        if (ele[i].checked)

            return (ele[i].value);


    }
}
// on click of the submit button get the value in the
// two textboxes add a comma and the value in the radio
//button and send to flask and display length
//and add layer
$("#searchCity").click(function(event) {
    var ele = RadioValue();
    let CityA = $("#CitySelectA").val();
    let CityB = $("#CitySelectB").val();
    var message = 'fill out both cities'

    if (CityA == null || CityB == null || CityA == "" || CityB == "") {
        alert("Please Fill All Required Field");
    } else {
        var res = CityA.concat(",", CityB, ";", ele);
        var splited = CityA.split(",");
        var splited2 = CityB.split(",");
        var lng = parseFloat(splited[0]);
        var lat = parseFloat(splited[1]);
        var lng1 = parseFloat(splited2[0]);
        var lat1 = parseFloat(splited2[1]);
        $.get("http://localhost:8080/distance/?lnglat=" + res)
            .done(function(data) {

                addLayer(lng, lat, lng1, lat1)
                lineAnswers = document.getElementById('calculated-length2');
                lineAnswers.innerHTML = '<p>' + data + '</p>';
            });
    }


});
// given the long lat of both cities add a 
//layer
function addLayer(lng, lat, lng1, lat1) {
    paint = getRandomColor();
    paint1 = getRandomColor();
    /* generate a unique layer id */
    var random = 'routeSource'
    var generate = makeid(6, random);
    //add points layer
    var random1 = 'route'
    var generate1 = makeid(6, random1);
    var random2 = 'route'
    var generate2 = makeid(6, random2);
    deleteLayer.push(generate);
    deleteLayer.push(generate1);
    deleteLayer.push(generate2);
    map.addSource(generate, {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [lng, lat],
                    [lng1, lat1]
                ]
            }
        }
    });

    map.addLayer({
        'id': generate1,
        'type': 'line',
        'source': generate,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': paint,
            'line-width': 2
        }


    });
    map.addLayer({
        'id': generate2,
        'source': generate,
        'type': 'circle',
        'paint': {
            'circle-radius': 6,
            'circle-color': paint1
        }
    });
    map.flyTo({
        center: [lng, lat],
        zoom: 4

    });
}
// read value in textbox to filter populate city A
$("#PickCityA").keyup(function(event) {
    populateCitySelectA();
});


// take the value in text box send to flask
//and display the list of cities eturned by flask
function populateCitySelectA() {
    let filter = $("#PickCityA").val();
    let html = '';
    $.get("http://localhost:8080/cities?filter=" + filter, function(data) {
        $('#CitySelectA').show();
        for (var i = 0; i < data['count']; i++) {

            html += "<option value ='" + data['results'][i].Coordinates + " '>" + data['results'][i].Name + "</option>";
        }
        $('#CitySelectA').attr("size", data['count']);
        $('#CitySelectA').html(html);

    });
}
// read value in textbox to filter populate cityB
$("#PickCityB").keyup(function(event) {
    populateCitySelectB();
});
// take the value in text box send to flask
//and display the list of cities eturned by flask
function populateCitySelectB() {
    let filter = $("#PickCityB").val();

    let html = '';
    $.get("http://localhost:8080/cities?filter=" + filter, function(data) {
        $('#CitySelectB').show();
        for (var i = 0; i < data['count']; i++) {
            html += "<option value ='" + data['results'][i].Coordinates + " '>" + data['results'][i].Name + "</option>";

        }
        $('#CitySelectB').attr("size", data['count']);
        $('#CitySelectB').html(html);

    });
}
//load city for railroads


//hide railroad dropdown
$('#stateSelectRail').hide();
//clear values in text box
$("#clearRail").click(function(event) {
    $("#pickStateRail").val("");
    $('#stateSelectRail').html("");
    getline = document.getElementById('invalidState');
    getline.innerHTML = '<p>'
    '</p>';
    getline.style.display = "none"
});
//populate states with railroad on click
$("#searchStateRail").click(function(event) {
    populateStatesSelect()
});
//on click of the drop down add the drop down value
//to the textbox and hide dropdown
$("#stateSelectRail").click(function(event) {
    let state = $("#stateSelectRail option:selected").text();
    $("#pickStateRail").val(state);
    $('#stateSelectRail').hide();
});
//search flask with the given state 
//add layer
$("#searchRail").click(function(event) {

    let state = $("#stateSelectRail").val();
    if (state == null || state == " ") {
        alert("Please select a State Field");
    } else {
        $.get("http://localhost:8080/StatesRailroad/?state=" + state)
            .done(function(data) {

                if (data['count'] == 1) {
                    getline = document.getElementById('invalidState');
                    getline.style.display = "block"
                    getline.innerHTML = '<p>' + 'database does not contain railroad data for selected state' + '</p>';

                } else {
                    addLayer1(data)
                }

            });
    }


});
//create layer for rail road given the 
//geojson
function addLayer1(json) {
    paint = getRandomColor();
    var random = 'Rail'
        /* generate a unique layer id */
    var generate = makeid(6, random);

    deleteLayer.push(generate);
    var latlng = json['geometry']['coordinates'][0];
    var enterLng = latlng[0];
    var enterLat = latlng[1];
    map.addSource(generate, {
        'type': 'geojson',
        'data': json

    });

    map.addLayer({
        'id': generate,
        'type': 'line',
        'source': generate,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': paint,
            'line-width': 1
        }
    });
    map.flyTo({
        center: [enterLng, enterLat],
        zoom: 7
    });
}
//read user input and populate states with
//dropdown with the user input
$("#pickStateRail").keyup(function(event) {
    populateStatesSelect();
});
//populate state 
function populateStatesSelect() {
    let filter = $("#pickStateRail").val();

    let html = '';
    $.get("http://localhost:8080/states?filter=" + filter, function(data) {
        $('#stateSelectRail').show();

        for (var i = 0; i < data['count']; i++) {
            html += '<option>' + data['results'][i].name + '</option>';
        }

        $('#stateSelectRail').attr("size", data['count']);
        $('#stateSelectRail').html(html);

    });
}
/* uplaod or paste geojson */
/* uplaod or paste geojson */
/* uplaod or paste geojson */


//validate brackets
/* https://stackoverflow.com/questions/52969755/how-to-check-the-sequence-of-opening-and-closing-brackets-in-string */
function check(expr) {
    const holder = []
    const openBrackets = ['(', '{', '[']
    const closedBrackets = [')', '}', ']']
    for (let letter of expr) { // loop trought all letters of expr
        if (openBrackets.includes(letter)) { // if its oppening bracket
            holder.push(letter)
        } else if (closedBrackets.includes(letter)) { // if its closing
            const openPair = openBrackets[closedBrackets.indexOf(letter)] // find his pair
            if (holder[holder.length - 1] === openPair) { // check if that pair is last element in array
                holder.splice(-1, 1) //if so, remove it
            } else { // if its not
                holder.push(letter)
                break // exit loop
            }
        }
    }
    return (holder.length === 0) // return true if length is 0, otherwise false
}
// converts to a json object
function convert(str) {
    //replaces the single qoutes with double qoutes
    str = str.replace(/'/g, '"')
    try {
        var tojson = JSON.parse(str);
    } catch (e) {
        return "false"
    }
    return tojson;

}
//onclick call addeojsonlayer
$("#loadmap").click(function(event) {
    var Coordinate = $("#TexrareaGeo").val();
    var radios = document.getElementsByName('Featuretype');
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {

            var featureValue = radios[i].value
            break;
        }
    }

    if (Coordinate == null || featureValue == null || Coordinate == "" || featureValue == "") {
        alert("Please Fill All Required Field");
    } else {
        if (check(Coordinate)) {
            var answer = convert(Coordinate)
            if (answer == "false") {
                getline = document.getElementById('invalidGeojson');
                getline.style.display = "block"
                getline.innerHTML = '<p>' + 'cannot parse geojson file' + '</p>';
            } else {
                //call back end
                $.get("http://localhost:8080/ValidGeoJson/?value=" + JSON.stringify(answer) + ";" + featureValue)
                    .done(function(data) {

                        if (data == "True") {
                            createpastedLayerPoints(answer);

                        } else {
                            getline = document.getElementById('invalidGeojson');
                            getline.style.display = "block"
                            getline.innerHTML = '<p>' + 'InvalidGeojson' + '</p>';

                        }

                    });
            }


        } else {
            getline = document.getElementById('invalidGeojson');
            getline.style.display = "block"
            getline.innerHTML = '<p>' + 'geojson is  missing some brackets' + ' < /p>';
        }


    }
});

/* add layerfor pasted geojson for points */
/* add layerfor pasted geojson for points */
/* add layerfor pasted geojson for points */
function createpastedLayerPoints(json) {
    paint = getRandomColor();
    paint1 = getRandomColor();
    paint2 = getRandomColor();

    var random = 'GeoSource'
        /* generate a unique layer id */
    var generate = makeid(6, random);
    deleteLayer.push(generate);

    var random3 = 'Geo'
        /* generate a unique layer id */
    var generate3 = makeid(6, random3);
    deleteLayer.push(generate3);

    var random1 = 'Geo'
        /* generate a unique layer id */
    var generate1 = makeid(6, random1);
    deleteLayer.push(generate1);

    var random2 = 'Geo'
        /* generate a unique layer id */
    var generate2 = makeid(6, random2);
    deleteLayer.push(generate2);


    map.addSource(generate, {
        'type': 'geojson',
        'data': json
            // poly
    });
    map.addLayer({
        'id': generate3,
        'source': generate,
        'type': 'circle',
        'paint': {
            'circle-radius': 6,
            'circle-color': paint
        },
        'filter': ['==', '$type', 'Point']
    });
    map.addLayer({
        'id': generate1,
        'type': 'fill',
        'source': generate,
        'paint': {
            'fill-color': paint1,
            'fill-opacity': 0.9
        },
        'filter': ['==', '$type', 'Polygon']
    });
    map.addLayer({
        'id': generate2,
        'type': 'line',
        'source': generate,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': paint2,
            'line-width': 5
        },
        'filter': ['==', '$type', 'LineString']
    });

    /*   map.flyTo({
          center: flytocoords,
          zoom: 5,
      }); */


}
/* travel mapjs */
$("#findTravel").click(function(event) {
    var lng = $("#lngInputs0").val();
    var lat = $("#latInputs0").val();
    var lng1 = $("#lngInputs1").val();
    var lat1 = $("#latInputs1").val();
    var result = lng + "," + lat + "," + lng1 + "," + lat1;
    if (lng == null || lng == " " || lat == null || lat == " " || lng1 == null || lng1 == " " || lat1 == null || lat1 == " ") {
        alert("Please enter a lnglat Field");
    } else {
        $.get("http://localhost:8080/Travel/?lnglat=" + result)
            .done(function(data) {
                AddTravelLayer();
            });
    }
});

function AddTravelLayer() {
    paint = getRandomColor();
    var random = 'Travel'
        /* generate a unique layer id */
    var generate = makeid(6, random);

    deleteLayer.push(generate);
    map.addSource(generate, {
        'type': 'geojson',
        'data': '/data.json'

    });

    map.addLayer({
        'id': generate,
        'type': 'line',
        'source': generate,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': paint,
            'line-width': 4
        }
    });
}

//clear textbox for pasted geojson
$("#clearpasted").click(function(event) {
    $("#TexrareaGeo").val("");
    $("#featureType").val("");
    $("input:radio").attr("checked", false);
    getline = document.getElementById('invalidGeojson');
    getline.innerHTML = '<p>'
    '</p>';
    getline.style.display = "none"

});



/* returns a list of checked boxes values */
function getSelectedCheckboxValues(boxs) {
    const checkboxes = document.querySelectorAll(`input[name="${boxs}"]:checked`);

    let values = [];
    checkboxes.forEach((checkbox) => {

        values.push(checkbox.value);
    });

    return values;
}
/* returns a list of checked boxes ids */
function getSelectedCheckboxid(boxs) {
    const checkboxes = document.querySelectorAll(`input[name="${boxs}"]:checked`);

    let values = [];
    checkboxes.forEach((checkbox) => {

        values.push(checkbox.id);
    });

    return values;
}
/* given the list of checkboxes remove the layer
remove all layers  */
const btn = document.querySelector('#buttondelete');
btn.addEventListener('click', (event) => {
    var list = [];
    list = getSelectedCheckboxValues('boxs')
    list.forEach(removelayers);


});
/* unchecks all the checked checkboxes */
window.onload = function() {
    const btns = document.querySelector('#clearcheckbox');
    btns.addEventListener('click', (event) => {
        var list = [];
        list = getSelectedCheckboxid('boxs')
        for (i = 0; i < list.length; i++) {
            document.getElementById(list[i]).checked = false;
        }

    });
};


/* removes all layers added to the delete
map that need to be deleted */

function removelayers(layer) {
    var afterdellete = [];
    var surceid = 'GeoSource';
    var sourceidRoute = 'routeSource';
    var contain = '';
    var sourcetobedeleted = '';
    var sourcetobedeleted2 = '';
    if (layer == "Geo") {
        for (i = 0; i < deleteLayer.length; i++) {
            var contain = deleteLayer[i];
            if (contain.includes(surceid)) {
                sourcetobedeleted = contain

            } else if (contain.includes(layer)) {
                afterdellete.push(contain);
                if (map.getLayer(contain)) {
                    map.removeLayer(contain);
                }

            }

        }
        map.removeSource(sourcetobedeleted);
        afterdellete.push(sourcetobedeleted);


    } else if (layer == 'route') {
        for (i = 0; i < deleteLayer.length; i++) {
            var contain = deleteLayer[i];
            if (contain.includes(sourceidRoute)) {
                sourcetobedeleted2 = contain

            } else if (contain.includes(layer)) {
                afterdellete.push(contain);
                if (map.getLayer(contain)) {
                    map.removeLayer(contain);
                }

            }

        }
        map.removeSource(sourcetobedeleted2);
        afterdellete.push(sourcetobedeleted2);


    } else {

        /*  deletes the layer that has been selcted to be 
        deleted from the map */
        for (i = 0; i < deleteLayer.length; i++) {
            var contain = deleteLayer[i];

            if (contain.includes(layer)) {
                afterdellete.push(contain);
                /*  map.removeLayer(contain);
                 */
                if (map.getLayer(contain)) {
                    map.removeLayer(contain);
                    map.removeSource(contain);
                }

            }

        }
        /* removes all the deleted layer from the array */
        for (i = 0; i < afterdellete.length; i++) {
            if (deleteLayer.includes(afterdellete[i])) {
                const index = deleteLayer.indexOf(afterdellete[i]);
                deleteLayer.splice(index, 1)
            }


        }

    }

}
//draw tool
//draw tool
//draw tool
var drawmodal = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
});
var drawTools = document.getElementById('drawAppends');
drawTools.appendChild(drawmodal.onAdd(map)).setAttribute("style", "display: inline-flex;", "border: 0;");
map.on('draw.create', updateArea);


/* creates a bounding box from the polygon 
drawn on the map gets the earthquake data 
and creates a layer */
function updateArea(e) {
    paint = getRandomColor();
    var data = drawmodal.getAll();
    var cooedinatesofdrawn = turf.meta.coordAll(data);
    var CreateLineString = turf.lineString(cooedinatesofdrawn);
    var boundingBox = turf.bbox(CreateLineString);
    var random = 'DrawL'
    var generate = makeid(6, random);

    deleteLayer.push(generate);
    //creates a bounding box around the drawn polygon
    var poly = turf.bboxPolygon(boundingBox);
    boundingBoxPolygon(poly)
    $.getJSON("http://localhost:8080/interSection/?lngLat=" + boundingBox)
        .done(function(json) {
            map.addSource(generate, {
                'type': 'geojson',
                'data': json
                    // poly
            });
            map.addLayer({
                'id': generate,
                'source': generate,
                'type': 'circle',
                'paint': {
                    'circle-radius': 6,
                    'circle-color': paint
                }
            });
            map.flyTo({
                center: cooedinatesofdrawn[0],
                zoom: 5,
            });


        })



}
// adds a layer to the boundiing box created for 
// the polygon drawn
function boundingBoxPolygon(polygonfeature) {
    paint = getRandomColor();
    var random = 'DrawL'
    var generate = makeid(6, random);
    deleteLayer.push(generate);
    map.addSource(generate, {
        'type': 'geojson',
        'data': polygonfeature
            // poly
    });
    map.addLayer({
        'id': generate,
        'type': 'fill',
        'source': generate,
        'paint': {
            'fill-color': paint,
            'fill-opacity': 0.4
        },
        'filter': ['==', '$type', 'Polygon']
    });
}


// Coordinates Tool
// Coordinates Tool
// Coordinates Tool
map.on(touchEvent, function(e) {
    var json = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinate": [e.lngLat.toArray()]
        },
        "properties": {

        }

    };
    latlngonclick
    document.getElementById('info').innerHTML =
        JSON.stringify(e.lngLat, function(key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')
    document.getElementById('latlngonclick').innerHTML =
        JSON.stringify(e.lngLat, function(key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')
    document.getElementById('latlngonclickd').innerHTML =
        JSON.stringify(e.lngLat, function(key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')

});

//BOOKMARKS
//BOOKMARKS
//BOOKMARKS

document.getElementById('icelandBookmark').addEventListener('click', function() {
    map.flyTo({
        center: [-18.7457, 65.0662],
        zoom: 5,
    });
});

document.getElementById('safricaBookmark').addEventListener('click', function() {

    map.flyTo({
        center: [23.9417, -29.5353],
        zoom: 5,
    });
});

document.getElementById('japanBookmark').addEventListener('click', function() {

    map.flyTo({
        center: [138.6098, 36.3223],
        zoom: 4,
    });
});

document.getElementById('australiaBookmark').addEventListener('click', function() {

    map.flyTo({
        center: [134.1673, -25.6855],
        zoom: 3

    });
});