var refInterval = window.setInterval('update()', 30000); // 30 seconds

var update = function() {
    $.ajax({
        type : 'GET',
        url : '../api/dashboard',
        success : function(data){
            console.log(data);
        },
    });
};

$(function() {

  // Uncomment to style it like Apple Watch
  if (!Highcharts.theme) {
      Highcharts.setOptions({
          chart: {
                	backgroundColor: 'white'
          },
          colors: ['#00A2E2', '#00A2E2', '#62CDCA', '#C4D600', '#9F015C', '#FF0700'],
          title: {
              style: {
                  color: 'silver'
              }
          },
          tooltip: {
              style: {
                  color: 'silver'
              }
          }
      });
  }
    
  Highcharts.chart('wowreturns', {

      chart: {
        type: 'solidgauge',
        marginTop: 0
      },
      
      title: {
            text: '',
            style: {
		    	fontFamily: 'Roboto, sans-serif',
				fontSize: '24px',
				fontWeight: '100',
				color: '#00A2E2',
            }
        },

      tooltip: {
        enabled: true
      },

      pane: {
        startAngle: 0,
        endAngle: 360,
        background: [{ // Track for Wow returns
          outerRadius: '80%',
          innerRadius: '48%',
          backgroundColor: Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0.3).get(),
          borderWidth: 0
        }]
      },

      yAxis: {
        min: 0,
        max: 100,
        lineWidth: 0,
        tickPositions: []
      },

      plotOptions: {
        solidgauge: {
          borderWidth: '24px',
          dataLabels: {
            enabled: false
          },
          linecap: 'round',
          stickyTracking: false
        }
      },

      series: [{
        name: 'Wowreturns',
        borderColor: Highcharts.getOptions().colors[0],
        data: [{
          color: Highcharts.getOptions().colors[0],
          radius: '100%',
          innerRadius: '100%',
          y: 50
        }]
      }]
    },

    /*
     * In the chart load callback, add icons on top of the circular shapes
    */
    function callback() {
      var chart = this,
        series = chart.series[0],
        shape = series.data[0].shapeArgs,
        x = shape.x,
        y = shape.y;

        chart.renderer.text(series.data[0].y + '<span style="vertical-align:super;font-size:50%">%</span>')
          .attr({
            'y': 15,
            'stroke': '#303030',
            'align': 'center',
            'font-size': '40px',
            'letterspacing': '5px',
            'zIndex': 10
          })
          .css({
		    fontFamily: 'Roboto, sans-serif',
            color: '#00A2E2',
          })
          .translate(x, y)
          .add(series.group);
          
        chart.renderer.circle(x, y, 60).attr({
            fill: '#FFFFFF'
        }).add(series.group);

    });


});