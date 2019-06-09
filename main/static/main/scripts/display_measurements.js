function draw_points(data, id) {
    var div = document.getElementById(id);
    var rect = div.getBoundingClientRect();

    var x = 0//rect.left;
    var y = 0//rect.top;
    var width = 1000//rect.right - x;
    var height = 1000//rect.bottom - y;
    var size = width < height ? width : height;

    k = 0.18;
    cellSize = 210 * k
    columns = size / cellSize

    var midX = Math.floor(columns/2) * cellSize;
    var midY = Math.floor(columns/2) * cellSize;

    pa.clear()
    var circle = pa.circle(midX, midY, 5)
    let pathline = 'M'+midX.toString()+" "+midY.toString()+"L"+(midX - 30).toString() + " " + midY.toString();
    var arrowhead = pa.path(pathline).attr({
    stroke: '#000000',
    'stroke-width': 2,
    'arrow-end':
        'classic-wide-long'
    });
    circle.attr("fill", "#f00")

    elems = data.length
    var border = pa.rect(x, y, width, height)
    border.attr("stroke-width", "7")

    for(j=0; j< columns; j++) {
            var path=' \"M';
            path += ("0 ");
            path += String(j*cellSize) + "L" + String(columns*cellSize) + " " + String(j*cellSize);
            line = pa.path(path);

            var path=' \"M';
            path += (String(j * cellSize));
            path += " 0" + "L" + String(j*cellSize) + " " + String(columns*cellSize);
            line = pa.path(path);
            line.attr("stroke-width", "0.5")
        }

    deltaDeg = 2 * Math.PI / elems;
    alfa = -Math.PI;

    for(i = 0; i < elems; i++) {
        //console.log(data[i][1])
        str = data[i][2];
        color = scale(str, 0, 1000, 0, 255);
        color = color > 255 ? 255 : color;
        l = data[i][1];
        c = pa.circle(midX + k*l*Math.cos(alfa), midY + k*l*Math.sin(alfa), 1)
        colorString = "rgb(0," + color +",0)"
        c.attr({
            stroke: colorString
        })
        alfa += deltaDeg;
    }

    imgSvg = pa.toSVG()
    divSvg = document.getElementById('svg')
    divSvg.innerHtml = imgSvg
}

const scale = (num, in_min, in_max, out_min, out_max) => {
  return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

async function downloadSVG() {

    const svg = document.getElementById('svg').innerHtml

    filename = "skan.svg"
    type = "image/svg+xml"
    data = svg

    var file = new Blob([data], {type: type});
    blob = URL.createObjectURL(file);
    console.log(blob)
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }

    await sleep(5000)

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/create_pdf",
      data: blob
    }).done(function() {
      $( this ).addClass( "done" );
    });

}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

