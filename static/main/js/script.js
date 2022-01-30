const init = () => {
    google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales'],
          ['2014', 1000,],
          ['2015', 1170,],
          ['2016', 660, ],
          ['2017', 1030,]
        ]);

        var options = {
          chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017',
          },
          animation: {"startup": true,
            duration: 1000,
            easing: 'out',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
        window.addEventListener('resize', () => {chart.draw(data, google.charts.Bar.convertOptions(options));})

      }
}
window.addEventListener('load', init)
