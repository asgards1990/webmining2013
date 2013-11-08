$(function() {
    $( "#slider" ).slider();
      });

  $(function() {
    $( "#slider-range-min" ).slider({
      range: "min",
      value: 100,
      min: 1,
      max: 300,
      slide: function( event, ui ) {
        $( "#amountb" ).val( "$" + ui.value +" M");
      }
    });
    $( "#amountb" ).val( "$" + $( "#slider-range-min" ).slider( "value" )+" M" );
  });


$(function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 300,
      values: [ 0, 300 ],
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
