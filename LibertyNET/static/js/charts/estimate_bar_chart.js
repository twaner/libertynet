/**
 * Created by taiowawaner on 8/10/14.
 */
function makeChart(estimates) {
     var estimates = jQuery.parseJSON(estimates);
      var estimates_array = [['Job Name', 'Price', 'Profit', 'Commission']]
      for (var i = 0; i < estimates.length; i++) {
//          if(parseFloat(estimates[i]["fields"]["listed_price"]) > 0 &&
//             parseFloat(estimates[i]["fields"]["listed_profit"] > 0) &&
//              parseFloat(estimates[i]["fields"]["custom_sales_commission"]) > 0)
//          {
              estimates_array.push([estimates[i]["fields"]["job_name"],
                  parseFloat(estimates[i]["fields"]["listed_price"]),
                  parseFloat(estimates[i]["fields"]["listed_profit"]),
                  parseFloat(estimates[i]["fields"]["custom_sales_commission"])]);
            }

//      $.each(estimates, function(){
//          estimates_array.push([estimates["fields"]["job_name"],parseFloat(estimates["fields"]["listed_price"]),
//             parseFloat(estimates["fields"]["listed_profit"]),parseFloat(estimates["fields"]["custom_sales_commission"])])
//      });

      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(estimates_array);

        var options = {
          title: 'Estimates Overview',
          hAxis: {title: 'Estimates', titleTextStyle: {color: 'blue'}}
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
}