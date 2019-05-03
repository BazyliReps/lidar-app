function draw_board(columns, id, obstacles, lidar_x, lidar_y) {
    var div = document.getElementById(id);
    var rect = div.getBoundingClientRect();
    var x = rect.left;
    var y = rect.top;
    var width = rect.right - x;
    var height = rect.bottom - y;
    var columns = columns;
    var size = width < height ? width : height;
    xOffset = x + (width - size)/2;

    var pa = Raphael(div);
    pa.setViewBox(0, 0, size, size, true);
    pa.canvas.setAttribute('preserveAspectRatio', 'none');

    var cellSize = size / columns;
        for(j=0; j< columns; j++) {
            var path=' \"M';
            path += ("0 ");
            path += String(j*cellSize) + "L" + String(columns*cellSize) + " " + String(j*cellSize);
            line = pa.path(path);

            var path=' \"M';
            path += (String(j * cellSize));
            path += " 0" + "L" + String(j*cellSize) + " " + String(columns*cellSize);
            line = pa.path(path);
        }
    obstacles = obstacles;
    obstacles.forEach( function (obs) {
        type = obs['type'];
        x = obs['x'];
        y = obs['y'];
        var c;
        if(type == "circle") {
            c = pa.circle(x,y,cellSize);
        } else {
            c = pa.rect(x,y,2*cellSize, 2*cellSize);
        }
        c.attr({"fill": "#808080", "fill-opacity": 0.5, "stroke-width":3 });
    });
    lid = pa.rect(lidar_x, lidar_y, 2*cellSize, 2*cellSize);
    lid.attr({"fill": "#f00", "fill-opacity": 0.5, "stroke-width":3 });
}
