$(document).ready(function() {
	var fill = d3.scale.category20();
    var jWord = ["abc","def","ghi"] ;
    var jCount = [80, 50, 30];
    var s = d3.scale.linear().range([0, 100]).domain([10,50]);
    console.log(d3.zip(jWord, jCount));

    d3.layout.cloud().size([420, 353])
        /* .words([
         "Hello", "world", "normallyvrgtrbtnthn", "your", "want", "more", "words",
         "than", "this"].map(function (d) {
         return {text: d, size: 10 + Math.random() * 40};
         }))*/
        .words(d3.zip(jWord, jCount).map(function (d) {
            return {text: d[0], size: d[1]};
        }))
        .padding(5)
                .rotate(function () {
                    return ~~(Math.random() * 2) * 90;
                })
                .font("Impact")
                .fontSize(function (d) {
                    return d.size;
                })
                .on("end", draw)
                .start();
	
	function draw(words) {
	    d3.select("#bagofwords").append("svg")
	            .attr("width", 420)
	            .attr("height", 353)
	            .append("g")
	            .attr("transform", "translate(210,177)")
	            .selectAll("text")
	            .data(words)
	            .enter().append("text")
	            .style("font-size", function (d) {
	                return d.size + "px";
	            })
	            .style("font-family", "Impact")
	            .style("fill", function (d, i) {
	                return fill(i);
	            })
	            .attr("text-anchor", "middle")
	            .attr("transform", function (d) {
	                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	            })
	            .text(function (d) {
	                return d.text;
	            });
	}
});