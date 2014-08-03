
function main() {

var w = 600;
var h = 250;
var lowerMarginY = 30;
var hGroup = {};

socket = new WebSocket('ws://localhost:8081/websocket');
socket.onmessage = function (event) {
  console.log(event.data);
  histdata = JSON.parse(event.data);
  plotHist(histdata);
}




function plotHist(dataset) {

console.log(dataset.name)

var xScale = d3.scale.ordinal()
	.domain(d3.range(dataset.value.length))
	.rangeRoundBands([0, w], 0.05); 

var yScale = d3.scale.linear()
	.domain([0, d3.max(dataset.value)])
	.range([0, h]);

//Create SVG element
var svg = d3.select("body")
			.append("svg")
			.attr("width", w)
			.attr("height", h)
      .attr("id", dataset.name);

//Create bars
svg.selectAll("rect")
   .data(dataset.value, function(d) { return d; })
   .enter()
   .append("rect")
   .attr("x", function(d, i) {
		return xScale(i);
   })
   .attr("y", function(d) {
		return h - lowerMarginY - yScale(d);
   })
   .attr("width", xScale.rangeBand())
   .attr("height", function(d) {
		return yScale(d);
   })
   .attr("fill", function(d) {
		return "rgb(0, 0, " + (d * 10) + ")";
   })

	//Tooltip
	.on("mouseover", function(d) {
		//Get this bar's x/y values, then augment for the tooltip
		var xPosition = parseFloat(d3.select(this).attr("x")) + xScale.rangeBand() / 2;
		var yPosition = parseFloat(d3.select(this).attr("y")) + 14;
		
		//Update Tooltip Position & value
		d3.select("#tooltip")
			.style("left", xPosition + "px")
			.style("top", yPosition + "px")
			.select("#value")
			.text(d);
		d3.select("#tooltip").classed("hidden", false)
	})
	.on("mouseout", function() {
		//Remove the tooltip
		d3.select("#tooltip").classed("hidden", true);
	});


var xAxisScale = d3.scale.ordinal()
  .domain(d3.range(dataset.edges.length))
  .rangeRoundBands([0, w], 0.); 


//Create labels
svg.selectAll("text")
   .data(dataset.edges, function(d) { return d; })
   .enter()
   .append("text")
   .text(function(d) {
		return d;
   })
   .attr("text-anchor", "middle")
   .attr("x", function(d, i) {
		return xAxisScale(i) + xAxisScale.rangeBand()  / 2;
   })
   .attr("y", function(d) {
		return h - 14;
   })
   .attr("font-family", "sans-serif") 
   .attr("font-size", "9px")
   .attr("fill", "black");


//Brushing
brushX = d3.scale.linear()
  .domain([dataset.edges[0],dataset.edges[dataset.edges.length-1]])
  .range([0, w]);
  

var  brush = d3.svg.brush()
  .x(brushX)
  .on("brushend", brushed);
  
svg.append("g")
  .attr("class", "brush")
  .attr("id", dataset.name + "MiniBrush")
  .call(brush)
  .selectAll('rect')
  .attr('height', h);


hGroup[dataset.name] = {"xScale": xScale, "yScale": yScale, "brush": brush , "brushX" : brushX };

}

function brushed() {
  var msg = {};

  msg['histID']= this.id.replace("MiniBrush","");
  msg['xSelection'] = hGroup[this.id.replace("MiniBrush","")].brush.extent();
 
  console.log(msg["xSelection"]);
  socket.send(JSON.stringify(msg));

}

}
