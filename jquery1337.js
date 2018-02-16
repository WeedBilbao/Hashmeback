$(function () {
	var loadPOST = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'post',
			success: function (data) {
				$(".paja").html(data.data);
				$(".x_loc_data").text(data.x);
				$(".y_loc_data").text(data.y);
				$(".flechaUP").attr({"data-url" : data.nextUP});
				$(".flechaDOWN").attr({"data-url" : data.nextDOWN});
				$(".flechaLEFT").attr({"data-url" : data.nextLEFT});
				$(".flechaRIGHT").attr({"data-url" : data.nextRIGHT});
			}
		});
	};
$(document).on("click", ".flecha", loadPOST);
$(document).ready(loadPOST);
});