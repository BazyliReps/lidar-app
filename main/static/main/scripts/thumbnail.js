var div = document.getElementById("{{b.board_id}}");
var rect = div.getBoundingClientRect();
var x = rect.left;
var y = rect.top;
var width = rect.right - x;
var height = rect.bottom - y;
var pa = Raphael(div,width,height);
var columns = {{b.columns}};
var size = width < height ? width : height;
size *= 0.8;
var cellSize = size / columns;
for(j=0; j< columns; j++) {
    var path=' \"M';
    path += ("0 ");
    path += String(j*cellSize) + "L" + String(columns*cellSize) + " " + String(j*cellSize);
    pa.path(path);


}
