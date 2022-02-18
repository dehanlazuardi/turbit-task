let myConfig = {
    type: 'line',
    timezone:0,
    title: {
        text: 'Data Basics',
        fontSize: 24,
    },
    legend: {
        draggable: true,
    },
    scaleX: {
        maxItems: 10,
        transform: {
            type: "date",
            all: "%Y-%m-%d<br>%H:%i",
            item: {
                visible: false
            }
        },
        zooming: true,
        label: { text: 'Date & Time' }
    },
    utc: true,
    timezone: 0,
    scaleY: {
        // Scale label with unicode character
        label: { text: 'Temperature (°F)' }
    },
    series: [
        {
            values: [
                [1433282400000,25.68],
                [1433286000000,26.41],
                [1433289600000,26.52],
                [1433293200000,26.23],
                [1433296800000,25.77]
            ],
            text: 'test-1'
        },
    ],
    preview: {
        adjustLayout: true,
        live: true
    },
    crosshairX: {
        lineColor: '#555',
        marker: {
          borderColor: '#fff',
          borderWidth: '1px',
          size: '5px'
        },
        plotLabel: {
          backgroundColor: '#fff',
          borderRadius: '2px',
          borderWidth: '2px',
          multiple: true
        }
    }
};

zingchart.render({
    id: 'myChart',
    data: myConfig
});

function updateChart(newData){
    zingchart.exec('myChart', 'setseriesvalues', {
        'values': newData
    });
}

function makeUrl(){
    startDate = document.getElementById('startdate').value;
    endDate = document.getElementById('enddate').value;
    propertyName = document.getElementById('data').value;

    return `data?start=${startDate}&end=${endDate}&key=${propertyName}`
}

function update(){
    startDate = document.getElementById('startdate').value;
    endDate = document.getElementById('enddate').value;
    propertyName = "Wind";

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            newData = JSON.parse(this.responseText)
            updateChart(newData);
        }
    };
    url = makeUrl()
    xhttp.open("GET", url, true);
    xhttp.send();
}