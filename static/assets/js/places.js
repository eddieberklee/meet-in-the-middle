function nearby_places(data) {
	places = data.places;
	for (var p in places) {
		place = places[p]
		$("#nearby_places_list").append("<li><div class='place' data-address='"+place.address+"'>"+place.name+"</div><div class='place' style='color:#bbb;font-size:0.7em;position:absolute;right:5px;'>"+place.address+"</div><div class='image'>"+place.image_url+"</div></li>");
	}
}
