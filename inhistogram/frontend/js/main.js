function checkboxTick(element){
    msg={"var":element.parentElement.innerText, "bin_edges":"", "selection": "" };
    socket.send(JSON.stringify(msg))
}

function main() {

var w = 600;
var h = 250;
var lowerMarginY = 30;
var hGroup = {};
var varNames;
d3.json("/variables/name", function(error, json) {
  if (error) return console.warn(error);
  console.log(json);
  varNames = json;
  console.log(varNames);
});
varNames={"varNames": ["D0_MM", "D0_PT", "D0_TAU", "D0_MINIPCHI2", "D0_DIRA_OWNPV", "nPV", "D0_MINIP", "piminus_PT", "piminus_ProbNNpi", "piminus_ProbNNk", "Kplus_PT", "Kplus_ProbNNpi", "Kplus_ProbNNk"]}    
drawTable(varNames);
socket = new WebSocket('ws://localhost:8081/websocket');
socket.onmessage = function (event) {
  console.log(event.data);
  histdata = JSON.parse(event.data);
  plotHist(histdata);
}
function drawTable(arrayNames){
    var array = d3.range(arrayNames.varNames.length)
    var table = d3.select('#table');
    table.selectAll("div").attr("class","checkbox").data(array, function(d) { return d; })
   .enter()
   .append("label").style("display", "block")
    .text(function(d) { 
       return arrayNames.varNames[d]; })
   .append("input")
   .attr("type","checkbox").attr("onclick","checkboxTick(this)")
}
    


function plotHist(dataset) {

console.log(dataset.name)

var xScale = d3.scale.ordinal()
	.domain(d3.range(dataset.value.length))
	.rangeRoundBands([0, w], 0.05); 

var yScale = d3.scale.linear()
	.domain([0, d3.max(dataset.value)])
	.range([0, h]);

var xAxisScale = d3.scale.ordinal()
  .domain(d3.range(dataset.edges.length))
  .rangeRoundBands([0, w], 0.); 

var svg = d3.select("#"+dataset.name);
console.log(dataset.name)

//Axis
var stepSize = (dataset.edges[1] - dataset.edges[0]).toPrecision(4);

var trueXAxisScale = d3.scale.ordinal()
  .domain(d3.range(0, dataset.edges[dataset.edges.length - 1].toPrecision(4), stepSize))
  .rangeRoundBands([0, w-2], 0.); 

var bandSize = xAxisScale.rangeBand()/2;

var xAxis = d3.svg.axis()
  .scale(trueXAxisScale)
  .orient("bottom")
  .ticks(5);

//Brushing
brushX = d3.scale.linear()
  .domain([dataset.edges[0],dataset.edges[dataset.edges.length-1]])
  .range([0, w]);
  

var  brush = d3.svg.brush()
  .x(brushX)
  .on("brushend", brushed);
  

// Check if avaliable
if (svg[0][0] == null) {
  svg = d3.select("#histograms")
      .append("svg")
      .attr("width", w + 20)
      .attr("height", h + 50) //+50 for the axis
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
    });

  svg.append("g")
    .attr("class", "x_axis")
    .attr("transform", "translate(-" + bandSize + "," + (h-25) + ")")
    .call(xAxis)
    .selectAll("text")
    .attr("transform", function(d) {
      return "translate(5,5) rotate(20)";
    });

  svg.append("g")
    .attr("class", "brush")
    .attr("id", dataset.name + "MiniBrush")
    .call(brush)
    .selectAll('rect')
    .attr('height', h);
} else {
  svg.selectAll("rect")
    .data(dataset.value, function(d) { return d; })
    .exit()
    .remove()

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
    });

  svg.append("g")
    .attr("class", "brush")
    .attr("id", dataset.name + "MiniBrush")
    .call(brush)
    .selectAll('rect')
    .attr('height', h);
}



















hGroup[dataset.name] = {"xScale": xScale, "yScale": yScale, "brush": brush , "brushX" : brushX };

}

function brushed() {
  var msg = {};
  msg['var']= this.id.replace("MiniBrush","");
  msg['bin_edges']= "";
  msg['selection'] = hGroup[this.id.replace("MiniBrush","")].brush.extent();
 
  console.log(msg["xSelection"]);
  socket.send(JSON.stringify(msg));

}

}
