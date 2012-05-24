

$(document).ready(function() {
    $('.enable-box-floating').each(function() {
	var boxes, box_width
	boxes = $(this).find('>.floated-box');
	box_width = 100/boxes.length;
	boxes.each(function() {
	    $(this).width(box_width + '%');
	    $(this).css('float', 'left');
	    $(this).css('margin', 0);
	    $(this).css('padding', 0);
	})
    });
})