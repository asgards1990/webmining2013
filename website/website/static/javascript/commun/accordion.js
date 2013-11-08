$(function() {

    var menu_li = $('.menu > li'),
           menu_a  = $('.menu > li > a');
    
    menu_li.each(function(){
//    alert('hello');
    if(!$(this).hasClass('item1') && !$(this).hasClass('item2') && !$(this).hasClass('item3')){
    $(this).children('ul').hide();
    	}
    	})

    menu_a.click(function(e) {
        e.preventDefault();
        if(!$(this).hasClass('active')) {
//            menu_a.removeClass('active');
//            menu_ul.filter(':visible').slideUp('normal');
            $(this).addClass('active').next().stop(true,true).slideDown('normal');
        } else {
            $(this).removeClass('active');
            $(this).next().stop(true,true).slideUp('normal');
        }
    });

});
