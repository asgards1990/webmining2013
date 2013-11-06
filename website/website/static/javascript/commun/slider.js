$(function() {
    $( "#slider" ).slider();
      });

$(function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 300,
      values: [ 30, 250 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.values[ 0 ] + "M - $" + ui.values[ 1 ]+"M" );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
      "M - $" + $( "#slider-range" ).slider( "values", 1 )+"M" );
      });

$(function() {
    $( "#slider-rangeyear" ).slider({
      range: true,
      min: 1980,
      max: 2013,
      values: [ 1980, 2013 ],
      slide: function( event, ui ) {
        $( "#amountyear" ).val(ui.values[ 0 ] + " - " + ui.values[ 1 ]);
      }
    });
    $( "#amountyear" ).val($( "#slider-rangeyear" ).slider( "values", 0 ) +
      " - " + $( "#slider-rangeyear" ).slider( "values", 1 ));
      });