function draw_points(data, id) {
    var div = document.getElementById(id);
    var rect = div.getBoundingClientRect();
    var x = rect.left;
    var y = rect.top;
    var width = rect.right - x;
    var height = rect.bottom - y;
    var size = width < height ? width : height;

    var midX = width/2;
    var midY = y + height/2;

     var pa = Raphael(div);
     pa.setViewBox(0, 0, size, size, true);
     pa.canvas.setAttribute('preserveAspectRatio', 'none');

    var circle = pa.circle(midX, midY, 5)
    let pathline = 'M'+midX.toString()+" "+midY.toString()+"L"+(midX + 30).toString() + " " + midY.toString();
    var arrowhead = pa.path(pathline).attr({
    stroke: '#000000',
    'stroke-width': 2,
    'arrow-end':
        'classic-wide-long'
    });
    circle.attr("fill", "#f00")

    elems = data.length

    deltaDeg = 2 * Math.PI / elems;
    alfa = 0.0;

    k = 1;



    for(i = 0; i < elems; i++) {
        //console.log(data[i][1])
        l = data[i][1];
        c = pa.circle(midX + k*l*Math.cos(alfa), midY + k*l*Math.sin(alfa), 1)
        alfa -= deltaDeg;
    }



    //pa.setViewBox(0, 0, size, size, true);
    //pa.canvas.setAttribute('preserveAspectRatio', 'none');


}
