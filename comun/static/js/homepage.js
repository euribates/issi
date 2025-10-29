console.log("Empezamos");
const canvas = document.getElementById('myChart');
ctx = canvas.getContext("2d");

const config = {
  'type': 'doughnut',
  'data': {
    'labels': ['Completos', 'Parciales', 'Solo identificados'],
    'datasets': [{
      'data': [12, 20, 16],
      'backgroundColor': ['#1bc138', '#fad90e', '#e56b6f'],
      'hoverBackgroundColor': ['LightGreen', 'yellow', 'red'],
      'borderWidth': 1.5,
      }],
    }, 
  'options': {
    'label': 'Sistemas de información',
    'onClick': function(evt) {
      console.log('onClick');
      },
    'animation': {
      'delay': 100,
      'onComplete': function(evt) {
          var chart = evt.chart;
          var ctx = chart.ctx;
          ctx.font = "50px Arial";
          var text = "48";
          var text_width = ctx.measureText(text).width;
          var x = (chart.width / 2) - (text_width / 2);
          var y = chart.chartArea.top + (chart.height / 2) - 25;
          ctx.fillText(text, x, y);
         },
       },
     },
  }

new Chart(ctx, config);

console.log('hasta aquí llega');
console.log('Y aquí tambien');
