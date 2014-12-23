$(document).ready(function() {
	var source = $("#template").html()


	var data = {
	  foo:"bar"
	}

	var template = Mustache.render(source, data)

	$("body").html(template)
})

