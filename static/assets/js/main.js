// Handler functions
var ROOT_DOMAIN = "http://localhost:5000/";
var State = {};
State.cont = function(){
};

Handles = {
    success : function(position){
        var lat = position.coords.latitude,
            lng = position.coords.longitude;
        View.create(lat,lng);
        State.personid = $.cookie('uid');
        State.name = $.cookie('name');
        if (State.personid === null ){
            State.name = prompt();
            $.ajax({
                type : 'POST',
                url : '/create_person',
                dataType : 'json',
                data : { "session_hash" : window.location.pathname.substr(1,5), "name" : State.name, "lat" : lat, "lon" : lon},
                success : function(data){
                    State.personid = data.id;
                    State.cont();
                },
                error : function(){
                    alert("Error with server");
                }
            });
        }else{
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

