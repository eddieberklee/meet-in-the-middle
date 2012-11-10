function nearby_places(data) {
	places = data.places;
	for (var p in places) {
		place = places[p]
		$("#nearby_places_list").append("<li><div class='place' data-address='"+place.address+"'>"+place.name+"</div></li>");
	}
}
