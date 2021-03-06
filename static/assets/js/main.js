// Handler functions
var ROOT_DOMAIN = window.location.origin;
var State = {};
State.arr = [];
State.virgin = true;
State.poll = function(){
    $.getJSON(window.location.pathname+'/data', function(data){
        //draw shit
        View.map.removeMarkers();
        $("#userlist").html("");
        $("#userlist").append('<li class="list-divider">Joined:</li>');
        //clear table
        var people = data.persons;
        var p, color;
        State.arr = [];
        for ( var i = 0; i < people.length; i++){
            p = people[i];
            color = View.rm;
            if ( parseInt(p.id) === parseInt(State.personid) ){
                color = View.bm;
            }
            View.map.addMarker({"lat" : p.lat, "lng" : p.lon, "icon" : color});
            $("#userlist").append('<li><div class="person">'+p.name+'</div><div class="clear"></div></li>');
            State.arr.push(new google.maps.LatLng(p.lat, p.lon));
            //do stuff with table
        }
        View.map.addMarker({"lat" : data.center_lat, "lng" : data.center_lon});
        State.cx = data.center_lat;
        State.cy = data.center_lon;
        //View.map.setCenter(data.center_lat, data.center_lon);
        if (State.virgin){
            State.virgin = false;
            View.map.fitZoom(State.arr);
        }
    });
};
State.zoom = function(){
        View.map.fitZoom(State.arr);
};
State.center = function(){
        View.map.setCenter(State.cx, State.cy);
};
State.update = function(lat,lng){
    State.lat = lat;
    State.lng = lng;
            $.ajax({
                type : 'POST',
                url : window.location.pathname+'/update',
                dataType : 'json',
                data : { "id" : State.personid, "lat" : State.lat, "lon" : State.lng},
                success : function(data){
                    return;
                },
                error : function(){
                    alert("Error with server");
                }
            });
};
State.cont = function(){
            $.ajax({
                type : 'POST',
                url : window.location.pathname+'/update',
                dataType : 'json',
                data : { "id" : State.personid, "lat" : State.lat, "lon" : State.lng},
                success : function(data){
                    if (data.error === 1 ){
                        throw Error("shit");
                    }else{
                        setInterval(State.poll, 5000);
                    }
                },
                error : function(){
                    alert("Error with server");
                }
            });
            navigator.geolocation.watchPosition(State.update, Handles.error, {enableHighAccuracy    : true, maximumAge:1000*3});
};

Handles = {
    success : function(position){
        var lat = position.coords.latitude,
            lng = position.coords.longitude;
        View.create(lat,lng);
        State.personid = $.cookie(window.location.pathname.substr(1,5)+"id");
        State.name = $.cookie(window.location.pathname.substr(1,5)+'name');
        State.lat = lat;
        State.lng = lng;
        if (State.personid === null ){
            State.name = prompt("Enter your name:");
            $.ajax({
                type : 'POST',
                url : '/create_person',
                dataType : 'json',
                data : { "session_hash" : window.location.pathname.substr(1,5), "name" : State.name, "lat" : lat, "lon" : lng},
                success : function(data){
                    $.cookie(window.location.pathname.substr(1,5)+'name', State.name);
                    $.cookie(window.location.pathname.substr(1,5)+'id', data.id);
                    State.personid = data.id;
                    $('#myname').text(State.name);
                    State.cont();
                },
                error : function(){
                    alert("Error with server");
                }
            });
        }else{
            $('#myname').text(State.name);
            State.cont();
        }
        //navigator.geolocation.watchPosition(Handles.watch, Handles.error, {enableHighAccuracy: true, maximumAge:1000*3});
    },
    error : function(position){
        alert("Error: Geolocationing not enabled.");
    },
    watch : function(position){
        console.log("watching");
        var lat = position.coords.latitude,
            lng = position.coords.longitude;
        //View.map must be instantiated
        if ( View.map === undefined )
            throw Error("View.map is undefined");
        View.updateCenter(lat,lng);
    },createPerson : function(){
    }
};

View = {
    map : null,
    bm : new google.maps.MarkerImage("static/mapimg/marker.png", new google.maps.Size(50,50), new google.maps.Point(0,0), new google.maps.Point(25,25)),
    rm : new google.maps.MarkerImage("static/mapimg/rmarker.png", new google.maps.Size(50,50), new google.maps.Point(0,0), new google.maps.Point(25,25)),
    create : function(lat, lng){
        console.log(lat,lng);
        this.map = new GMaps({
            div: '#map',
            lat: lat,
            lng: lng
        });
        this.lat = lat;
        this.lng = lng;
    },
    updateCenter : function(lat, lng){
        this.map.setCenter(lat,lng);
        this.lat = lat;
        this.lng = lng;
    }
};

//Launch Localization
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(Handles.success, Handles.error, {enableHighAccuracy: true, maximumAge:1000*10});
} else {
    alert("Error: Not supported on this device");
}

