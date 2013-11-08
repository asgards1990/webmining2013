$(document).ready(function() {
    $('#menu').mouseover(function() {
	$('#actors > a > span').text($('#actors > ul > li > p > .checked').length);
    $('#directors > a > span').text($('#directors > ul > li > p > .checked').length);
	$('#genres > a > span').text($('#genres > ul > li > p > .checked').length);
    })
});
