$(document).ready(function() {
	$("#input-container").height(window.innerHeight);

	$("form").first().submit(function(e) {

	e.preventDefault();

	var url = $("#url-text").val();
	if (!isValidUrl(url)) {
		return doError();
	}

	// $("#error-msg").hide();
	TweenLite.to("#error-msg", .1, {autoAlpha: 0});
	$("#url-text").css("outline", "none");

	doSubmitAnimation();

	$("#result").css("display", "block");
	$.getJSON(
	  "/get_ingredients/",
	  {url:$("[name=url]").first().val()},
	  function(resp) {
	  	showResults(resp);
	    $.each(resp, function(index, val) {
	      $("#result").html($("#result").html() + "<br />" + val)
	    });
	});
	return false;

	});
});

function doSubmitAnimation() {
	var box_offset = $("#black-box").offset();
	var submit_offset = $("#url-submit").offset();
	var t1 = new TimelineLite();

	var text_offset = $("#url-text").offset();

	t1.to("#url-submit", .3, {
		top: 500,
		left: submit_offset.left + 40,
		width: 0,
		height:0,
		color:"transparent",
		ease:Back.easeIn,
		opacity:0
	})
	.to("#url-text", .3, {
		top: 500,
		left: submit_offset.left + 40,
		width: 0,
		height:0,
		color:"",
		ease:Back.easeIn,
		opacity:0
	});

	TweenLite.to("#title", .5, {opacity:0, y:"-=50px", ease:Back.easeIn});

	$("#progress-bar").css("display","block");

	var t2 = new TimelineMax();
	t2.to("#progress-bar", .5, {opacity:1, y:"-=50px", ease:Back.easeIn});
	t2.to("#progress-bar", 1, {rotationZ:-360, repeat:-1, ease:Linear.easeNone})
}

function isValidUrl(str) {
	if (str.length !== 0 && (str.slice(0, 7) === "http://" ||
		str.slice(0, 8) === "https://")) {
		return true;
	}
	return false;
}

function doError() {
	$("#url-text").css("outline", "1px solid red");
	TweenLite.fromTo("#error-msg", .5, {top:"-80px"}, {top:0, ease:Bounce.easeOut});
}

function showResults() {
	TweenLite.to("#progress-bar", .3, {y:"+=100px", ease:Back.easeIn, autoAlpha:0, display:"none"});
	TweenLite.to("#result", .5, {opacity:1, y:"-=50px"});
}





