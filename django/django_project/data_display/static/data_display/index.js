function makeChartConfig(chartName, chartType, useDate=true) {
    myConfig = {
        type: chartType,
        title: {
            text: chartName,
            fontSize: 24,
        },

        noData: {
            text: "Currently there is no data in the chart",
            fontSize: 18,
            textAlpha: .9,
            alpha: .6,
            bold: true
          },
    };

    if ((useDate) == true) {
        myConfig["timezone"] = 0
        myConfig["utc"] = true
        myConfig["scaleX"] = {
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
        }
        myConfig["crosshairX"] = {
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
        myConfig["preview"] = {
            adjustLayout: true,
            live: true
        }
    }

    return myConfig
}

zingchart.render({
    id: 'myChart1',
    data: makeChartConfig("Turbine-1", "line", true)
});

zingchart.render({
    id: 'myChart2',
    data: makeChartConfig("Turbine-2", "line", true)
});

zingchart.render({
    id: 'myChart3',
    data: makeChartConfig("Power vs Wind", "scatter", false)
});

function updateChart(chartNum, newData, labelX="", labelY="") {
    // update data value
    chartId = `myChart${chartNum}`
    optionElementId = `data-${chartNum}`
    optionElement = document.getElementById(optionElementId)
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

    // update Y axis
    if (labelY) {
        zingchart.exec(chartId, 'modify', {
            data: {
                scaleY: {
                    label: { text: labelY }
                }
            }
        });
    }
    
    // update X axis
    if (labelX) {
        zingchart.exec(chartId, 'modify', {
            data: {
                scaleX: {
                    label: { text: labelX }
                }
            }
        });
    }
    
    // reset zoom
    zingchart.exec(chartId, 'viewall');
}

function makeUrl(chartNum) {
    startDateId = `start-date-${chartNum}`
    endDateId = `end-date-${chartNum}`
    propertyNameId = `data-${chartNum}`
    turbine = `${chartNum}`

    startDate = document.getElementById(startDateId).value;
    endDate = document.getElementById(endDateId).value;
    propertyName = document.getElementById(propertyNameId).value;
    
    if (propertyName == "Wind-Power"){
        key1 = "Wind"
        key2 = "Leistung"
        turbine = "1"
    } else {
        key1 = "Dat/Zeit"
        key2 = propertyName
    }

    return `/data?start=${startDate}&end=${endDate}&key=${key1}&key=${key2}&turbine=${turbine}`
}

function update(chartNum) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            newData = JSON.parse(this.responseText);
                        
            labelX = `${newData['name'][0]}`
            if (newData['unit'][0]) {
                labelX += ` (${newData['unit'][0]})`
            }

            labelY = `${newData['name'][1]}`
            if (newData['unit'][1]) {
                labelY += ` (${newData['unit'][1]})`
            }

            updateChart(chartNum, newData['data'], labelX, labelY);
        }
    };
    url = makeUrl(chartNum);
    xhttp.open("GET", url, true);
    xhttp.send();
}