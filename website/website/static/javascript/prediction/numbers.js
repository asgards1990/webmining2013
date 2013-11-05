$(document).ready(function() {
    $('#menu').on('change', function() {
	$('#prediction_item_actors > a > span').text($('#id_actors-deck > div').length);
	$('#prediction_item_keyword > a > span').text($('#id_keyword-deck > span').length);
	$('#prediction_item_genres > a > span').text($('#id_genre1-deck > span').length+$('#id_genre2-deck > span').length);
	$('#prediction_item_genres > a > span').text($('#id_genre1-deck > span').length+$('#id_genre2-deck > span').length);
    })
    
    $('#menu').mouseover(function() {
	$('#prediction_item_actors > a > span').text($('#id_actors-deck > div').length);
	$('#prediction_item_keyword > a > span').text($('#id_keyword-deck > span').length);
	$('#prediction_item_genres > a > span').text($('#id_genre1-deck > span').length+$('#id_genre2-deck > span').length);
	$('#prediction_item_genres > a > span').text($('#id_genre1-deck > span').length+$('#id_genre2-deck > span').length);
    })

});