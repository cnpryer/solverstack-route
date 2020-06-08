// Builds the HTML Table out of data.
function buildHtmlTable(selector, data) {
  var columns = addAllColumnHeaders(data, selector);

  for (var i = 0; i < data.length; i++) {
    var row$ = $('<tr/>');
    for (var colIndex = 0; colIndex < columns.length; colIndex++) {
      var cellValue = data[i][columns[colIndex]];
      if (cellValue == null) cellValue = "";
      row$.append($('<td/>').html(cellValue));
    }
    $(selector).append(row$);
  }
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records.
function addAllColumnHeaders(data, selector) {
  var columnSet = [];
  var headerTr$ = $('<tr/>');

  for (var i = 0; i < data.length; i++) {
    var rowHash = data[i];
    for (var key in rowHash) {
      if ($.inArray(key, columnSet) == -1) {
        columnSet.push(key);
        headerTr$.append($('<th/>').html(key));
      }
    }
  }
  $(selector).append(headerTr$);

  return columnSet;
}

function buildPlotlyMap(selector, solution) {

    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }

    var id = unpack(solution, 'id'),
        pallets = unpack(solution, 'pallets'),
        lat = unpack(solution, 'latitude'),
        lon = unpack(solution, 'longitude'),
        cluster = unpack(solution, 'cluster')
        vehicle = unpack(solution, 'vehicle')
        size = [],
        hoverText = [],
        //scale = 2.* Math.max(null, pallets) / (100**2);
        scale = 2;

    for ( var i = 0 ; i < pallets.length; i++) {
        var currentSize = pallets[i] / scale;
        var currentText = "pallets: " + pallets[i]  + "<br>cluster: " + cluster[i] + "<br>vehicle: " + vehicle[i];
        size.push(currentSize);
        hoverText.push(currentText);
    }

    var data = [{
        type: 'scattergeo',
        locationmode: 'USA-states',
        lat: lat,
        lon: lon,
        hoverinfo: 'text',
        text: hoverText,
        marker: {
            size: size,
            color: vehicle,
            line: {
                color: 'black',
                width: 0.5
            },
        }
    }];

    var layout = {
        title: 'without dbscan preprocessing (segmentation)',
        showlegend: false,
        autosize: true,
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 30,
            pad: 4
        },
        geo: {
            scope: 'usa',
            projection: {
                type: 'albers usa'
            },
            showland: true,
            landcolor: 'rgb(217, 217, 217)',
            subunitwidth: 1,
            countrywidth: 1,
            subunitcolor: 'rgb(255,255,255)',
            countrycolor: 'rgb(255,255,255)'
        },
    };

    Plotly.plot(selector, data, layout, {showLink: false});
}
