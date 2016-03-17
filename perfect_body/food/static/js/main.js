(function() {
		$('dd').filter(':nth-child(n+2)').addClass('hide');
		$('dl').on('click', 'dt', function() {
			$(this)
				.next()
					.slideDown(300)
					.siblings('dd')
						.slideUp(300);	
				google.maps.event.trigger(map, 'resize');

		})
	})();

function initAutocomplete() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 42.6955987, lng: 23.1835176},
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var input = document.getElementById('pac-input');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
        map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
        });

        var markers = [];
        searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }
          markers.forEach(function(marker) {
            marker.setMap(null);
          });
          markers = [];
          var bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            var icon = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };
            markers.push(new google.maps.Marker({
              map: map,
              icon: icon,
              title: place.name,
              position: place.geometry.location
            }));

            if (place.geometry.viewport) {
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }
          });
          map.fitBounds(bounds);
        });
      }

$(document).ready(function() {
  
  $("dt.profile").click();

  $("form[name='change_password']").submit(function(e){
    e.preventDefault();
    var form = $(this);
    $.ajax({
      url:'/saveProfile',
      data:form.serialize(),
      type: "POST",
      success:function(data){        
        console.log(data);
      }
    });
  })

  initAutocomplete();
});