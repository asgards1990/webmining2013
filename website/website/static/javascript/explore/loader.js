/**
 * Created by Julien on 08/11/13.
 * http://fgnass.github.io/spin.js/
 */

var opts = {
  lines: 13, // The number of lines to draw
  length: 11, // The length of each line
  width: 9, // The line thickness
  radius: 29, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 0, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#000', // #rgb or #rrggbb or array of colors
  speed: 1.3, // Rounds per second
  trail: 70, // Afterglow percentage
  shadow: true, // Whether to render a shadow
  hwaccel: true, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: 'auto', // Top position relative to parent in px
  left: 'auto' // Left position relative to parent in px
};
var target = document.getElementById('actors');
var spinner = new Spinner(opts).spin(target);
