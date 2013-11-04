$("#rateit").bind('rated', function (event, value) {
    $('#value5').text('You\'ve rated it: ' + value);
});


$("#rateit").bind('rated', function (event, value) {
    $('#value5').text('You\'ve rated it: ' + value);
    valueStar=value;
});


//build toc
var toc = [];
$('#examples > li').each(function (i, e) {


    if (i > 0)
        toc.push(', ');
    toc.push('<a href="#')
    toc.push(e.id)
    toc.push('">')
    var title = $(e).find('h3:first').text();
    title = title.substring(title.indexOf(')') + 2);
    toc.push(title);
    toc.push('</a>');
});

$('#toc').html(toc.join(''));

