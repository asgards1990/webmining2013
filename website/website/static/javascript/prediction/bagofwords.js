$(document).ready(function() {
	var fill = d3.scale.category20();
	
	d3.layout.cloud().size([300,300])
	        .words([
	            "Hello", "world", "normallyvrgtrbtnthn", "your", "want", "more", "words",
	            "than", "this"].map(function (d) {
	                    return {text: d, size: 10 + Math.random() * 40};
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
	            .attr("width", 400)
	            .attr("height", 220)
	            .append("g")
	            .attr("transform", "translate(200,110)")
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