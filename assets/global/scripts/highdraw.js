$(function () {

    $(document).ready(function () {

        // Build the chart
        $('#container').highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: '测试项目'
            },

            tooltip: {

                pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:f}</b> of 100<br/>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [{
                type: 'pie',
                name: 'cpu',
                data: [
                {
                    name: '未分配cpu',
                    y:15
                },
                {
                    name: '已分配cpu',
                    y:25
                }],
                center: [500, 50],
                size: 200,
                showInLegend: true,
                dataLabels: {
                enabled: false
                    }
                },

                {
                type: 'pie',
                name: '内存',
                data: [
                {
                    name: '未分配内存',
                    y:25,
                    color:"#50B432"
                },
                {
                    name:'已分配内存',
                    y:15,
                    color:"#028DC7"
                }],
                center: [1000, 50],
                size: 200,
                showInLegend: true,
                dataLabels: {
                enabled: false
                    }
                }]
        });
    });

});
