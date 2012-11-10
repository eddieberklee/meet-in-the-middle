// Handler functions
var ROOT_DOMAIN = window.location.origin;
Handles = {
    bool : false,
    success : function(position){
        var lat = position.coords.latitude,
            lng = position.coords.longitude;
        View.create(lat,lng);
        navigator.geolocation.watchPosition(Handles.watch, Handles.error, {enableHighAccuracy: true, maximumAge:1000*3});
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
        View.update(lat,lng);
    }, create : function(){
        //handle for submitting creation to /create
        var name;
        if (Handles.bool){
            name = $('#name').val();
            if ( name === "" ){
                alert("Please enter a name!");
            }else{
                $.cookie("name", name);
                $.ajax({
                    type : 'POST',
                    url : '/create_session',
                    dataType : 'json',
                    data : {"name": name,"lat": View.lat, "lon":View.lng},
                    success : function(data){
                        if (data.error == 1){
                            throw Error("Server blew up");
                        }else{
                            $.cookie("uid", data.id);
                            window.location = ROOT_DOMAIN+'/'+data.session_hash;
                        }
                    },
                    error : function(){
                        alert("Invalid server request");
                    }
                });
            }
        }
    }
};

//TODO: NEED TO CHANGE MARKER.PNG LOCATION
View = {
    map : undefined,
    mark : undefined,
    bm : new google.maps.MarkerImage("static/mapimg/marker.png", new google.maps.Size(50,50), new google.maps.Point(0,0), new google.maps.Point(25,25)),
    create : function(lat, lng){
        this.map = new GMaps({
            div: '#map',
            lat: lat,
            lng: lng
        });
        this.mark = View.map.addMarker({"lat": lat, "lng" : lng, "icon" : View.bm});
        this.lat = lat;
        this.lng = lng;
    },
    update : function(lat, lng){
        this.map.setCenter(lat,lng);
        this.mark.setPosition(new google.maps.LatLng(lat,lng));
        this.lat = lat;
        this.lng = lng;
    }
};

//Launch Localization
if (navigator.geolocation) {
    Handles.bool = true;
    navigator.geolocation.getCurrentPosition(Handles.success, Handles.error, {enableHighAccuracy: true, maximumAge:1000*10});
} else {
    alert("Error: Not supported on this device");
}


//Place marker

//click find my friends
//  --> check if name is set
//  --> proceed to create
//          POST to /create
