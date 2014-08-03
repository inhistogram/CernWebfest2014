function inHist() {
var w = 600;
var h = 250;
var hMini = h / 4;
//var histdata;
var hGroup = {};

socket = new WebSocket('ws://localhost:8081/websocket');
socket.onmessage = function(event) {
  console.log(event.data);
  histdata = JSON.parse(event.data);
  plotHist(histdata);
};

function plotHist(dataset) {

console.log(dataset.name);

var xScale = d3.scale.ordinal()
	.domain(d3.range(dataset.value.length))
	.rangeRoundBands([0, w], 0.05);

var yScale = d3.scale.linear()
	.domain([0, d3.max(dataset.value)])
	.range([0, h]);

var yScaleMini = d3.scale.linear()
  .domain([0, d3.max(dataset.value)])
  .range([0, hMini]);

//Create SVG element
var svg = d3.select('#histograms')
			.append('svg')
			.attr('width', w)
			.attr('height', h)
      .attr('id', dataset.name);

var svgMini = d3.select('#histograms')
  .append('svg')
  .attr('width', w)
  .attr('height', hMini)
  .attr('id', dataset.name + 'Mini');

draw(svg,dataset);

function draw(svg, dataset) {
//Create bars
svg.selectAll('rect')
   .data(dataset.value, function(d) { return d; })
   .enter()
   .append('rect')
   .attr('x', function(d, i) {
		return xScale(i);
   })
   .attr('y', function(d) {
		return h - yScale(d);
   })
   .attr('width', xScale.rangeBand())
   .attr('height', function(d) {
		return yScale(d);
   })
   .attr('fill', function(d) {
		return 'rgb(0, 0, ' + (d * 10) + ')';
   });

 svgMini.selectAll('rect')
  .data(dataset.value, function(d) { return d; })
  .enter()
  .append('rect')
  .attr('x', function(d, i) {
    return xScale(i);
  })
  .attr('y', function(d) {
    return hMini - yScaleMini(d);
  })
  .attr('width', xScale.rangeBand())
  .attr('height', function(d) {
    return yScaleMini(d);
  })
  .attr('fill', function(d) {
    return 'rgb(0, 0, ' + (d * 10) + ')';
  });

//Create labels
svg.selectAll('text')
   .data(dataset.value, function(d) { return d; })
   .enter()
   .append('text')
   .text(function(d) {
		return d;
   })
   .attr('text-anchor', 'middle')
   .attr('x', function(d, i) {
		return xScale(i) + xScale.rangeBand() / 2;
   })
   .attr('y', function(d) {
		return h - yScale(d) + 14;
   })
   .attr('font-family', 'sans-serif')
   .attr('font-size', '11px')
   .attr('fill', 'white');


svgMini.selectAll('text')
.data(dataset.value, function(d) { return d; })
.enter()
.append('text')
.text(function(d) {
  return d;
})
.attr('text-anchor', 'middle')
.attr('x', function(d, i) {
  return xScale(i) + xScale.rangeBand() / 2;
})
.attr('y', function(d) {
  return hMini - yScaleMini(d) + 14;
})
.attr('font-family', 'sans-serif')
.attr('font-size', '11px')
.attr('fill', 'white');

//Brushing
brushX = d3.scale.linear()
  .domain([dataset.edges[0], dataset.edges[dataset.edges.length - 1]])
  .range([0, w]);

var brush = d3.svg.brush()
  .x(brushX)
  .on('brush', brushed);

svgMini.append('g')
  .attr('class', 'brush')
  .attr('id', dataset.name + 'MiniBrush')
  .call(brush)
  .selectAll('rect')
  .attr('height', h);


hGroup[dataset.name] = {'xScale': xScale, 'yScale': yScale, 'brush': brush, 'brushX' : brushX };



function brushed() {

  var idBigOne = this.id.replace('MiniBrush', '');
  console.log(hGroup[idBigOne].brush.extent());
  var svg = d3.select('#' + idBigOne);
  draw(svg, dataset);

  }
 }
}
}
  //Tooltip
/*
  .on('mouseover', function(d) {
    //Get this bar's x/y values, then augment for the tooltip
    var xPosition = parseFloat(d3.select(this).attr('x')) + xScale.rangeBand() / 2;
    var yPosition = parseFloat(d3.select(this).attr('y')) + 14;

    //Update Tooltip Position & value
    d3.select('#tooltip')
    .style('left', xPosition + 'px')
    .style('top', yPosition + 'px')
    .select('#value')
    .text(d);
    d3.select('#tooltip').classed('hidden', false);
  })
  .on('mouseout', function() {
    //Remove the tooltip
    d3.select('#tooltip').classed('hidden', true);
  });

}
*/


