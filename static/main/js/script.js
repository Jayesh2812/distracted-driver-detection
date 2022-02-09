const init = () => {
    google.charts.load('current', {'packages':['bar', 'corechart']});
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
        };

        var barChart = new google.charts.Bar(document.getElementById('columnchart_material'));
        var pieChart = new google.visualization.PieChart(document.getElementById('piechart'))

        barChart.draw(finalData, options);
        options = options.chart
        pieChart.draw(finalData, options);
        
        window.addEventListener('resize', () => {
          barChart.draw(finalData, options);
          pieChart.draw(finalData, options);

        })

      }
}
window.addEventListener('load', init)
