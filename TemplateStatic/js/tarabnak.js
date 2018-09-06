$(document).ready(function(){
	$('.sidenav').sidenav();

	$(document).ready(function(){
		$('.collapsible').collapsible({
			accordion: false
		});
	});

	$(".mainSlider").owlCarousel({
		items: 1,
		nav: true,
		dots: true,
		autoplay: true,
		autoplayTimeout: 15000,
		animateIn: 'fadeIn',
		animateOut: 'fadeOut',
		navContainer: $('.navSlider > .owl-navs'),
		dotsContainer: $('.navSlider > .owl-dots'),
		navText: ["<i class='material-icons'>arrow_forward</i>", "<i class='material-icons'>arrow_back</i>"],
		rtl: true,
		loop: true
	});
});