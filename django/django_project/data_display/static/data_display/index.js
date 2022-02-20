function makeChartConfig(chartName) {
    myConfig = {
        type: 'line',
        timezone: 0,
        utc: true,
        title: {
            text: chartName,
            fontSize: 24,
        },
        legend: {
            draggable: false,
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
        scaleY: {
            // Scale label with unicode character
            label: { text: 'Temperature (°F)' }
        },
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
        },
        noData: {
            text: "Currently there is no data in the chart",
            fontSize: 18,
            textAlpha: .9,
            alpha: .6,
            bold: true
          },
    };
    return myConfig
}

zingchart.render({
    id: 'myChartLeft',
    data: makeChartConfig("Turbine-1")
});

zingchart.render({
    id: 'myChartRight',
    data: makeChartConfig("Turbine-2")
});

function updateChart(newData, unit = '', chartNum) {
    // update data value
    optionElement = document.getElementById('data-left')
    chartId = "myChartLeft"
    if (chartNum ==  2) {
        optionElement = document.getElementById('data-right')
        chartId = "myChartRight"
    }
    dataName = optionElement.options[optionElement.selectedIndex].text;
    seriesNewData = [
        {
            values: newData,
            text: dataName
        }
    ];
    zingchart.exec(chartId, 'setseriesdata', {
        'data': seriesNewData
    });

    // update axis Y
    labelY = `${dataName}`
    if (unit) {
        labelY += ` (${unit})`
    }
    zingchart.exec(chartId, 'modify', {
        data: {
            scaleY: {
                label: { text: labelY }
            }
        }
    });
    zingchart.exec(chartId, 'viewall');
}

function makeUrl(chartNum) {
    startDateId = "start-date-left"
    endDateId = "end-date-left"
    propertyNameId = "data-left"
    turbine = "1"
    if (chartNum == 2) {
        startDateId = "start-date-right"
        endDateId = "end-date-right"
        propertyNameId = "data-right"
        turbine = "2"
    }

    startDate = document.getElementById(startDateId).value;
    endDate = document.getElementById(endDateId).value;
    propertyName = document.getElementById(propertyNameId).value;

    return `/data?start=${startDate}&end=${endDate}&key=${propertyName}&turbine=${turbine}`
}

function update(chartNum) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            newData = JSON.parse(this.responseText)
            updateChart(newData['data'], newData['unit'], chartNum);
        }
    };
    url = makeUrl(chartNum)
    xhttp.open("GET", url, true);
    xhttp.send();
}