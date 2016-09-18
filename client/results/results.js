function EasyPeasyParallax() {
	scrollPos = $(this).scrollTop();
	$('.p1').css({
		'background-position' : '50% ' + (-scrollPos/4)+"px"
	});
  $('.p2').css({
		'background-position' : '50% ' + (-scrollPos/8)+"px"
	});
  $('.p3').css({
		'background-position' : '70% ' + (-scrollPos/16)+"px"
	});
	$('.parallax-text').css({
		'margin-top': (scrollPos/2)+"px",
		'opacity': 1-(scrollPos/230)
	});
}
$(document).ready(function(){
	$(window).scroll(function() {
		EasyPeasyParallax();
	});
});




Template.results.events({
   "click .toggle-checked": function ()  {
      HTTP.call("POST", "localhost:5000/results", jsonData);
    }
});
