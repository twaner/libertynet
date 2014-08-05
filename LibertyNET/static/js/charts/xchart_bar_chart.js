/**
 * Created by taiowawaner on 8/4/14.
 */
//     <figure style="width: 800px; height: 400px;" id="myChart"></figure>
    function createChart(estimateList) {
        var qq = 0;
        var ww = 0;
        var fields = [1, 2, 3];
        // My work
        // Data Source
        var estimates = jQuery.parseJSON(
    //        {{ estimate_list | safe }}
            estimateList);

    var getData = function () {
    // counter
    var cnt = 0;
    var data = {
        "xScale": "ordinal",
        "yScale": "linear"
    };

    data.main = [];
    $(fields).each(function () {
        // graph data array
        var graphData = [];
        var q = 0;
        var t = '';
        cnt++;
        // loop through array of estimates
        $.each(estimates, function () {
            if (cnt % 3 == 0) {
                q = parseInt(this["fields"]["listed_price"]);
                t = 'cnt % 3 == 0 PRICE';
            }
            else if (cnt % 3 == 1) {
                q = parseInt(this["fields"]["listed_profit"]);
                t = 'cnt % 3 == 1 PROFIT';
            }
            else if (cnt % 3 == 2) {
                q = parseInt(this["fields"]["custom_sales_commission"]);
                t = 'cnt % 3 == 2 custom_sales_commission';
            }
            graphData.push({
                "x": this["fields"]["job_name"],
                "y": q
            });
//                  alert("cnt & q " + cnt + ' ' + q + ' t is : ' + t + ' this ' + this["fields"]["job_name"]
//                         + ' graphData length ' + graphData.length);
        });
        data.main.push({
            "className": ".estimates",
            "data": graphData
        })
    });
    return data;
};

var myChart = new xChart('bar', getData(), '#myChart', {axisPaddingTop: 5, paddingLeft: 35});
}