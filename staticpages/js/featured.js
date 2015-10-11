	$(document).ready(function(){
		$.ajax({
			'type': 'GET',
			'url': 'http://api.sjdsdirectory.com/fish_prices',
			'success': function(feat){
				featured_json = JSON.parse(feat);
				console.log(featured_json);
				update_fish(featured_json);
			}
		});
		$.ajax({
			'type': 'GET',
			'url': 'http://api.sjdsdirectory.com/get_num_featured/1/',
			'success': function(feat){
				featured_json = JSON.parse(feat);
				update_single_featured(featured_json[0][1]);
			}
		});
		$.ajax({
			'type': 'GET',
			'url': 'http://api.sjdsdirectory.com/get_num_featured/12/',
			'success': function(feat){
				featured_json = JSON.parse(feat);
				add_featured_businesses(featured_json);
			}
		});
		$.ajax({
			'type': 'GET',
			'url': 'http://api.sjdsdirectory.com/get_num_featured/2/',
			'success': function(feat){
				featured_json = JSON.parse(feat);
				update_footer_2(featured_json);
			}
		});
	});
	function update_footer_2(featured_json){
			var html = '';
			keys_arr = Object.keys(featured_json);
			keys_arr.forEach(function(i){
				html += '<div class="latest-post clearfix"> <div class="post-image"><a href="/company-profile.html?id=' + featured_json[i][1]['id'] + '"><img src="http://api.sjdsdirectory.com/media/business_images/' + featured_json[i][1]['id'] + '/' + featured_json[i][1]['photos'][0] + '" alt=""></a>';
				html += '<p><span></span>Feat</p> </div> <h4><a href="/company-profile.html?id=' + featured_json[i][1]['id'] + '">' + featured_json[i][1]['name'] + '</a></h4>';
				html += '<p>' + featured_json[i][1]['description'].slice(0,50) +'...</p> </div>';
			});
		$(".latest-post").replaceWith(html);
	}

	function update_single_featured(featured_json){
		$("#Featured_Business").replaceWith('<div id="Featured_Business"></div>');
		var image;
		if (featured_json['photos']){
			image = '<img style="width: 250px;" class="logo-image" src="http://api.sjdsdirectory.com/media/business_images/' + featured_json['id'] + '/' + featured_json['photos'][0] + '" />';
		} else {
			image = '';
		}
		$("#Featured_Business").append('<h2>' + featured_json['name'] + '</h2>' + image + '<br />' + featured_json['description']);
	}

	function update_fish(featured_json){
		$("#fishies").replaceWith('<div id="fishies"></div>');
		keys_arr = Object.keys(featured_json)
		$("#fishies").append("<h2>Local Fish</h2>");
		keys_arr.forEach(function(i){
			$("#fishies").append('<div><b>' + featured_json[i]['name_english']  + ' (' + featured_json[i]['name_spanish'] + ') ' +  '</b> - ' + featured_json[i]['price'] + ' C/lb</div>');
		});
		$("#fishies").append('<h4 class="fishies-contact">Ask for Esterlina</h4>');
	}



	function add_featured_businesses(featured_json){
		var html = '';
		keys_arr = Object.keys(featured_json);
		keys_arr.forEach(function(i){
        html += '<div class="col-md-3 col-sm-4 col-xs-6">';
				html += '<div class="single-product" style="min-height: 256px;"> <figure> <img src="http://api.sjdsdirectory.com/media/business_images/' + featured_json[i][1]['id'] + '/' + featured_json[i][1]['photos'][0] + '" alt=""> <div class="rating"> <ul class="list-inline">';
				html += '<li><a href="#"><i class="fa fa-star"></i></a></li> <li><a href="#"><i class="fa fa-star"></i></a></li> <li><a href="#"><i class="fa fa-star"></i></a></li>';
				html += '<li><a href="#"><i class="fa fa-star-half-o"></i></a></li> <li><a href="#"><i class="fa fa-star-o"></i></a></li> </ul>';
				html += '<p>Featured</p> </div> <!-- end .rating -->';
				html += '<figcaption>  <div class="read-more"> <a href="/company-profile.html?id=' + featured_json[i][1]['id'] + '"><i class="fa fa-angle-right"></i> Read More</a> </div> </figcaption>';
				html += '</figure> <h4><a href="/company-profile.html?id=' + featured_json[i][1]["id"] + '">' + featured_json[i][1]['name'] + '</a></h4>';
				//html += '<h5><a href="#">Category</a>, <a href="#">Another Category</a></h5>';
				html += '</div> <!-- end .single-product -->';
				html += '</div>';
		});
		$("#featured_listings").replaceWith(html);
	}

