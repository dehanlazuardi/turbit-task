const data = {
        datasets: [{
            label: 'Scatter Dataset',
            data: [{
                x: "2016-01-01 00:10:00",
                y: 0
            }, {
                x: "2016-01-01 00:20:00",
                y: 10
            }, {
                x: "2016-01-01 00:30:00",
                y: 5
            }, {
                x: "2016-01-01 00:40:00",
                y: 5.5
            }],
            backgroundColor: 'rgb(255, 99, 132)'
        }],
    };

const config = {
        type: 'scatter',
        data: data,
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'MM YYYY'
                        }
                    }
                }
            }
        }
    };

const myChart = new Chart(document.getElementById('myChart'), 
                        {
                            type: 'line',
                            data: {
                                datasets: [{
                                    data: [{
                                        x: '2016-01-01T01:00:00Z',
                                        y: 50
                                    }, {
                                        x: '2016-01-01T01:00:00Z',
                                        y: 60
                                    }, {
                                        x: '2016-01-01T01:00:00Z',
                                        y: 20
                                    }],
                                    backgroundColor: 'rgb(255, 99, 132)'
                                }],
                            },
                            options: {
                                scales: {
                                    xAxes: [{
                                        type: 'time',
                                        time: {
                                            parser: 'YYYY-MM-DDTHH:mm:ss',
                                            unit: 'date',
                                            displayFormats: {
                                                'date': 'YYYY-MM-DD'
                                            }
                                        }
                                    }]
                                },
                                bezierCurve: true
                            }
                        });

function updateChart(new_data){
    myChart.config.data.datasets[0].data = new_data;
    myChart.update();
}

function update(){
    startDate = document.getElementById('startdate').value;
    endDate = document.getElementById('enddate').value;
    propertyName = "Wind";

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            updateChart(JSON.parse(this.responseText));
        }
    };
    xhttp.open("GET", "/data", true);
    xhttp.send();
}