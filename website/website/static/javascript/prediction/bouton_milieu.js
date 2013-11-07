$(document).ready(function(){
    $("#prizes").mouseover(function() {
      $("#cssdeck").attr('class', 'prizesclass');
    });

    $("#boxoffice").mouseover(function() {
      $("#cssdeck").attr('class', 'boxofficeclass');
    });

    $("#reviews").mouseover(function() {
      $("#cssdeck").attr('class', 'reviewsclass');
    });

    $("#bagofwords").mouseover(function() {
      $("#cssdeck").attr('class', 'bagofwordsclass');
    }); 
});
