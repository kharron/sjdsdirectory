	 function update_catlist(cat_json){
			var keys_arr = Object.keys(cat_json);	
			$("#category-show").html('<div id="category"></div>');
			var html = '';
			keys_arr.forEach(function(i){
				html += '<div class="col-md-3 col-sm-4 col-xs-6"> <div class="category-item">';
				html += '<a href="search-result.html?category=' + cat_json[i]["name"] + '"><i class="fa fa-' + cat_json[i]['image'] + '"></i>' + cat_json[i]['name'] + '</a> </div> </div>';
			});
			$("#category-show").append(html); 
	 }
	 
	 function get_cat_list(){
		$.ajax({
			'type': 'GET',
			'url': 'http://api.sjdsdirectory.com/getcatsfull/',
			'success': function(list){
				cat_json = JSON.parse(list);
				update_catlist(cat_json);
			}
		});
	 }

	 function create_list(res){
		 res_keys = Object.keys(res);
		 var html = '';
		 res_keys.forEach(function(i){
			 html += "<li class='search-result'><a href='/company-profile.html?id=" + res[i].id + "'>" + res[i].name + "</a></li>";
		 });
		 return html;
	 }

	 function keyword_results(res, prods){
		 var html;
		 html = "<ul id='search-find'>";
		 html += create_list(res);
		 html += "<li style='height: 16px; background-color:#eee;font-size: 9pxcolor:#000; text-align: left;'>PRODUCTS</li>";
		 html += create_list(prods);
		 html += "</ul>";
		 left = $("#search-keyword").offset().left;
		 sTop = $("#search-keyword").offset().top+40;
		 var keyword_width = $("#search-keyword").width();
		 if ($("#search-keyword").val().length > 0){
			 if (!$("#search-find").length){
				 $("#main-wrapper").prepend(html);
			 } else {
				 $("#search-find").replaceWith(html);
			 }
			 $("#search-find").css("top", sTop);
			 $("#search-find").css("left", left);
			 $("#search-find").css("width", keyword_width);
		 } else {
			$("#search-find").remove();
		 }


	 }

	$(document).ready(function(){
		get_cat_list();

		$("body").on("input", "#search-keyword", function(){
			var keyword = this.value
			if (keyword){
				$.ajax({
					type: 'POST',
					url: 'http://api.sjdsdirectory.com/search/',
					data: 'keyword=' + keyword,
					success: function(data){
						var res = JSON.parse(data);
						var prods = res['prods'];
						var result = res['results'];
						keyword_results(result, prods);
					}
				});
			} else {
				if ($("#search-find").length){
					$("#search-find").remove();
				}
			}
		});

	});

