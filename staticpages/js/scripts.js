;(function($) {

  "use strict";

  var $body = $('body');
  // var $head = $('head');
  // var $mainWrapper = $('#main-wrapper');

  // Mediaqueries
  // ---------------------------------------------------------
  // var XS = window.matchMedia('(max-width:767px)');
  // var SM = window.matchMedia('(min-width:768px) and (max-width:991px)');
  // var MD = window.matchMedia('(min-width:992px) and (max-width:1199px)');
  // var LG = window.matchMedia('(min-width:1200px)');
  // var XXS = window.matchMedia('(max-width:480px)');
  // var SM_XS = window.matchMedia('(max-width:991px)');
  // var LG_MD = window.matchMedia('(min-width:992px)');


  // jquery ui call functionfor calendar
  //------------------------------------------------
  $( "#datepicker" ).datepicker();

  // Touch
  // ---------------------------------------------------------
  var dragging = false;

  $body.on('touchmove', function() {
    dragging = true;
  });

  $body.on('touchstart', function() {
    dragging = false;
  });


  // Advanced search toggle
  var $SearchToggle = $('.header-search-bar .search-toggle');
  $SearchToggle.hide();

  $('.header-search-bar .toggle-btn').on('click', function(e){
    e.preventDefault();
    $SearchToggle.slideToggle(300);
  });


  // navbar toggle
  //------------------------------------------------
  $('.header-nav-bar button').on('click',function(event){
		event.preventDefault();
		$(this).toggleClass('active');
    $('.header-nav-bar').toggleClass('active');
		$('.header-nav-bar').show("slide", { direction : "left" }, 1000);
  });

  var $headerNavBar = $('#header .header-nav-bar, .header-nav-bar button');

  $headerNavBar.each(function () {
    var $this = $(this);

    $this.on('clickoutside touchendoutside', function (event) {
      event.preventDefault();
      if ($this.hasClass('active')) { $this.removeClass('active'); }
    });
  });



  // Category toggle
  //-------------------------------------------------

  $('.category-toggle button').on('click',function(){
    $('.category-toggle').toggleClass('active');
  });

  var $CategoryTtoggle = $('.category-toggle');

  $CategoryTtoggle.each(function () {
    var $this = $(this);

    $this.on('clickoutside touchendoutside', function () {
      if ($this.hasClass('active')) { $this.removeClass('active'); }
    });
  });




  //home slide tab-content hide
  //---------------------------------------
  $('.home-tab li > a').on('click', function(){

    $CategoryTtoggle.removeClass('active');
  });

  // home map tab-content hide
  //---------------------------------------------
  $('.accordion-tab li > div a').on('click', function(){

    $CategoryTtoggle.removeClass('active');
  });


  // our-partners slider customize
  //-----------------------------------------
  $("#partners-slider").owlCarousel({
    autoPlay: 3000,
    items : 6,
    itemsDesktop : [1199,4],
    itemsDesktopSmall : [979,3],
    itemsTablet: [600,2]
  });


  // home slider section
  //-------------------------------------------
  var homeSlide = $("#home-slider");

  homeSlide.owlCarousel({

    navigation : false, // Show next and prev buttons
    slideSpeed : 600,
    paginationSpeed : 600,
    singleItem:true

  });


  // Custom Navigation Events
    $(".next").click(function(){
      homeSlide.trigger('owl.next');
    });
    $(".prev").click(function(){
      homeSlide.trigger('owl.prev');
    });




  // UOU Selects
  // ---------------------------------------------------------
  $.fn.uouCustomSelect = function () {
    var $select = $(this);

    $select.wrap('<div class="uou-custom-select"></div>');

    var $container = $select.parent('.uou-custom-select');

    $container.append('<ul class="select-clone"></ul>');

    var $list = $container.children('.select-clone'),
      placeholder = $select.data('placeholder') ? $select.data('placeholder') : $select.find('option:eq(0)').text();

    // $('<input class="value-holder" type="text" disabled="disabled" placeholder="' + placeholder + '"><i class="fa fa-chevron-down"></i>').insertBefore($list);
    $('<input class="value-holder" type="hidden" disabled="disabled" placeholder="' + placeholder + '"><span class="placeholder">' + placeholder + '</span><i class="fa fa-chevron-down"></i>').insertBefore($list);

    var $valueHolder = $container.children('.value-holder');
    var $valuePlaceholder = $container.children('.placeholder');

    // Create clone list
    $select.find('option').each(function () {
      var $this = $(this);

      $list.append('<li data-value="' + $this.val() + '">' + $this.text() + '</li>');
    });

    // Toggle list
    $container.on('click', function () {
      // console.log('click ' + $container);
      $container.toggleClass('active');
      $list.slideToggle(250);
    });

    // Option Select
    $list.children('li').on('click', function () {
      var $this = $(this);

      $valueHolder.val($this.text());
      $valuePlaceholder.html($this.text());
      $select.find('option[value="' + $this.data('value') + '"]').prop('selected', true);
    });

    // Hide
    $container.on('clickoutside touchendoutside', function () {
      if (!dragging) {
        $container.removeClass('active');
        $list.slideUp(250);
      }
    });

    // Links
    if ($select.hasClass('links')) {
      $select.on('change', function () {
        window.location.href = select.val();
      });
    }

    $select.on('change', function () {
      cosole.log(chnaged);
      cosole.log($(this).val());
    });
  };

  $('select').each(function () {
    $(this).uouCustomSelect();
  });




// distance slider initialize

  // distance slider

  $( "#slider-range-min" ).slider({
    range: "min",
    value: 42,
    min: 1,
    max: 100,
    slide: function( event, ui ) {
      $( "#amount" ).val( ui.value +   "km" );
    }
  });
  $( "#amount" ).val( $( "#slider-range-min" ).slider( "value" ) +   "km");


  $( "#slider-range-search" ).slider({
    range: "min",
    value: 42,
    min: 1,
    max: 100,
    slide: function( event, ui ) {
      $( "#amount-search" ).val( ui.value +   "km" );
    }
  });
  $( "#amount-search" ).val( $( "#slider-range-search" ).slider( "value" ) +   "km");




  $( "#slider-range-search-day" ).slider({
    range: "min",
    value: 20,
    min: 1,
    max: 300,
    slide: function( event, ui ) {
      $( "#amount-search-day" ).val(  "<"  + ui.value );
    }
  });
  $( "#amount-search-day" ).val( "<" +  $( "#slider-range-search-day" ).slider( "value" ) );





  // Accordion
  // ---------------------------------------------------------
  $('.accordion').each(function () {

    $(this).find('ul > li > a').on('click', function (event) {
      event.preventDefault();

      var $this = $(this),
        $li = $this.parent('li'),
        $div = $this.siblings('div'),
        $siblings = $li.siblings('li').children('div');

      if (!$li.hasClass('active')) {
        $siblings.slideUp(250, function () {
          $(this).parent('li').removeClass('active');
        });

        $div.slideDown(250, function () {
          $li.addClass('active');
        });
      } else {
        $div.slideUp(250, function () {
          $li.removeClass('active');
        });
      }
    });

  });



  // header login register scripts
  //-------------------------------------------

  var $headerLoginRegister = $('#header .header-login, #header .header-register');

  $headerLoginRegister.each(function () {
    var $this = $(this);

    $this.children('a').on('click', function (event) {
      event.preventDefault();
      $this.toggleClass('active');
    });

    $this.on('clickoutside touchendoutside', function () {
      if ($this.hasClass('active')) { $this.removeClass('active'); }
    });
  });



  var $headerNavbar = $('#header .header-nav-bar .primary-nav > li');

  $headerNavbar.each(function () {
    var $this = $(this);

    $this.children('a').on('click', function (event) {
      $this.toggleClass('active');
    });

    $this.on('clickoutside touchendoutside', function () {
      if ($this.hasClass('active')) { $this.removeClass('active'); }
    });
  });




  // Header Language Toggle
  // ---------------------------------------------------------
  var $headerLanguageToggle = $('#header .header-language');

  $headerLanguageToggle.children('a').on('click', function (event) {
    event.preventDefault();
    $(this).parent('.header-language').toggleClass('active');
  });

  $headerLanguageToggle.on('clickoutside touchendoutside', function () {
    if ($headerLanguageToggle.hasClass('active')) { $headerLanguageToggle.removeClass('active'); }
  });

  // Header Social Toggle
  // ---------------------------------------------------------
  var $headerSocialToggle = $('#header .header-social');

  $headerSocialToggle.children('a').on('click', function (event) {
    event.preventDefault();
    $(this).parent('.header-social').toggleClass('active');
  });

  $headerSocialToggle.on('clickoutside touchendoutside', function () {
    if ($headerSocialToggle.hasClass('active')) { $headerSocialToggle.removeClass('active'); }
  });




  // sub-categories remove and active class
  //-----------------------------------------------------
  var $CategoryLink = $('#categories .accordion ul li div a');

  $CategoryLink.on('click', function(){
    $(this)
      .addClass('active')
      .siblings().removeClass('active')
      .parent().parent().siblings('li').children('div a').click(function(){
        $CategoryLink.removeClass('active');
      });
  });



  // style switcr for list-grid view
  //--------------------------------------------------
  $('.change-view button').on('click',function(e) {

    if ($(this).hasClass('grid-view')) {
      $(this).addClass('active');
      $('.list-view').removeClass('active');
      $('.page-content .view-switch').removeClass('product-details-list').addClass('product-details');

    } else if($(this).hasClass('list-view')) {
      $(this).addClass('active');
      $('.grid-view').removeClass('active');
      $('.page-content .view-switch').removeClass('product-details').addClass('product-details-list');
      }
  });




  // company-heading slider content
  //--------------------------------------------------------
  $('.button-content button').on('click',function(e) {
    console.log('clickes');

    if ($(this).hasClass('general-view-btn')) {
      $(this).addClass('active')
      .siblings().removeClass('active')
      .parent().parent().next().css("left","0%");


    } else if($(this).hasClass('map-view-btn')) {
      $(this).addClass('active')
      .siblings().removeClass('active')
      .parent().parent().next().css("left","-100%");

    } else if($(this).hasClass('male-view-btn')) {
      $(this).addClass('active')
     .siblings().removeClass('active')
     .parent().parent().next().css("left","-200%");
    }

  });


  $("a").click(function(e){
    if($(this).attr("href") === '#'){
      e.preventDefault();
    }
  });


}(jQuery));



$("document").ready(function($){
  var nav = $('.header-search-bar');

  $(window).scroll(function () {
    if ($(this).scrollTop() > 60) {
        nav.addClass("sticky");

    } else {
        nav.removeClass("sticky");
    }

  });
	// For now remove the ability to carousel
	$("a.btn.prev").remove();
	$("a.btn.next").remove();
});


