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