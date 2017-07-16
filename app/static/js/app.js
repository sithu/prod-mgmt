var source = $("#orders-template").html(); 
var template = Handlebars.compile(source); 
var MAX_ROW = 20;
var current_orders = [];
var charts = [];
var refInterval = window.setInterval('update()', 30000); // 30 seconds

var update = function() {
    $.ajax({
        type : 'GET',
        url : '../api/dashboard',
        success : function(data){
            console.log(data);
            if (arraysEqual(data, current_orders)) {
                // update progress
                console.log("update progress");
                console.log(charts.length);

                for(var j = 0; j < data.length; j++) {
                    order = data[j];
                    if ( JSON.stringify(current_orders[j]) === JSON.stringify(order) ) {
                        console.log("No changes found. Skipping...");
                        continue;
                    }
                    $('#title_' + order.id).html(order.machine_product);
                    $('#q_' + order.id).html(order.quantity);
                    $('#c_' + order.id).html(order.completed);
                    $('#b_' + order.id).html(order.total_bad);
                    chart = charts[j];
                    console.log(chart);
                    console.log("current value");
                    current = chart.series[0].data[0];
                    console.log(current.y);
                    current.y = order.percent;
                    console.log("new value =" + order.percent);
                    chart.series[0].setData([current]);
                    chart.percent_label.attr({
                        text: order.percent + '<span style="vertical-align:super;font-size:50%">%</span>'
                    })
                }
            } else {
                console.log("init all charts");
                console.log(charts.length);

                current_orders = [];
                charts = [];
                var row_num = 0;
                $('#chart_group').html('');

                for( var i = 0;  i < data.length; i++) {
                    order = data[i];
                    current_orders.push(order);
                    if ( i % 3 == 0) {
                        row_num++;
                        row_html = '<div id="row_' + row_num + '" class="flex-row row"></div>';
                        $('#chart_group').append(row_html);
                    }
                    row = '#row_' + row_num;
                    $(row).append(template(order));
                    console.log("draw_donut");
                    chart = draw_donut(order.id + '', order.percent);
                    console.log(chart);
                    charts.push(chart);
                }
            }
        },
    });
};

var draw_donut = function(id, percent) {

    var chart = new Highcharts.chart(id, {

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
          y: percent
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

        this.percent_label = chart.renderer.text(series.data[0].y + '<span style="vertical-align:super;font-size:50%">%</span>')
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
    
    return chart;
};


function arraysEqual(a, b) {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length != b.length) return false;

  // If you don't care about the order of the elements inside
  // the array, you should sort both arrays here.

  for (var i = 0; i < a.length; ++i) {
    if (a[i].id !== b[i].id) return false;
  }
  return true;
}