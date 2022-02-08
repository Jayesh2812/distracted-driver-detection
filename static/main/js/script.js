const init = () => {
    google.charts.load('current', {'packages':['bar']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var finalData = google.visualization.arrayToDataTable([
          ['Class Labels', 'Count'],
          ...data
        ]);

        var options = {
          chart: {
            title: 'Different Driving Positions Frequency Comparison',
            subtitle: 'Driver\'s behaviour analysis using deep learning',
          },
          animation: {"startup": true,
            duration: 1000,
            easing: 'out',
          }
        };

        var chart = new google.charts.Bar(document.getElementById('columnchart_material'));

        chart.draw(finalData, google.charts.Bar.convertOptions(options));
        window.addEventListener('resize', () => {chart.draw(finalData, google.charts.Bar.convertOptions(options));})

      }
}
window.addEventListener('load', init)
