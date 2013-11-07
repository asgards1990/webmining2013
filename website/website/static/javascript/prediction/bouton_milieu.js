$(document).ready(function(){
    $("#prizes").mouseover(function() {
      $("#cssdeck").attr('class', 'prizesclass');
      $("#prizesborder").attr('class', 'topborder');
      $("#boxofficeborder").attr('class', 'greyborder');
      $("#reviewsborder").attr('class', 'greyborder');
      $("#bagofwordsborder").attr('class', 'greyborder');
    });

    $("#boxoffice").mouseover(function() {
      $("#cssdeck").attr('class', 'boxofficeclass');
      $("#prizesborder").attr('class', 'greyborder');
      $("#boxofficeborder").attr('class', 'topborder');
      $("#reviewsborder").attr('class', 'greyborder');
      $("#bagofwordsborder").attr('class', 'greyborder');
    });

    $("#reviews").mouseover(function() {
      $("#cssdeck").attr('class', 'reviewsclass');
      $("#prizesborder").attr('class', 'greyborder');
      $("#boxofficeborder").attr('class', 'greyborder');
      $("#reviewsborder").attr('class', 'bottomborder');
      $("#bagofwordsborder").attr('class', 'greyborder');
    });

    $("#bagofwords").mouseover(function() {
      $("#cssdeck").attr('class', 'bagofwordsclass');
      $("#prizesborder").attr('class', 'greyborder');
      $("#boxofficeborder").attr('class', 'greyborder');
      $("#reviewsborder").attr('class', 'greyborder');
      $("#bagofwordsborder").attr('class', 'bottomborder');
    }); 
});
