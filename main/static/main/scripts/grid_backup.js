

        //globalna zmienna planszy
        let board = null;
        const lidarXInput = $("id_lidar_x");
        const lidarYInput = $("id_lidar_y");
        const obstaclesInput = $('id_obstacles')


        class Board {
            constructor(posX, posY, rows, columns, size) {
                this.posX = posX;
                this.posY = posY;
                this.cells = [];
                this.obstacles = new Map();
                this.cellSize = size;
                this.rows = rows;
                this.columns = columns;
                this.lidar = null;
                this.lidarX = 0;
                this.lidarY = 0;
            }
        }

        class BoardSaveData {
            constructor(board) {
                this.name = board.name;
                this.rows = board.rows;
                this.columns = board.columns;
                this.cellSize = board.cellSize;
                this.obstacles = '';
                this.lidarX = board.lidarX;
                this.lidarY = board.lidarY;
            }
        }

        class Cell {
            constructor(x,y) {
                this.x = x;
                this.y = y;
                this.name = String.fromCharCode(65 + x);
                this.name+=this.y;
            }
        }

        class Obstacle {
            constructor(x,y,type) {
                this.x = x;
                this.y = y;
                this.type = type;
            }
        }

        function createBoard() {
            const divWidth = document.getElementById('board').clientWidth;
            const divHeight = document.getElementById('board').clientHeight;
            const name = document.getElementById('id_name').value;

            let size = divWidth < divHeight ? divWidth : divHeight;
            const rows = document.getElementById("id_rows").value * 1;
            const columns = document.getElementById("id_columns").value * 1;


            const paper = Raphael(10, 50, divWidth, divHeight);

            const cellSize = divWidth < divHeight ? divWidth / rows - 10 : divHeight / rows - 10;

            //to odczytania ze strony
            const realCellSize = 20;

            board = new Board(10,50,rows,columns,realCellSize);
            board.name = name;
            board.lidar = paper.rect(0,0,0,0);
            let i = 0;
            for(; i < board.rows; i++) {
                let j = 0;
                for(; j < board.columns; j++) {
                    board.cells.push(new Cell(i,j));
                }
            }

            for(i = 0;i < board.cells.length;i++) {
                    const cell = board.cells[i];
                    const x = board.posX + cell.x * cellSize;
                    const y = board.posY + cell.y * cellSize;
                    const rect = paper.rect(x, y, cellSize, cellSize);
                    const text = paper.text(x + cellSize/2, y + cellSize/2, cell.name);
                    const cellGroup = paper.set();
                    rect.attr({"fill":"#fff", "stroke":"#000", "stroke-width":2});
                    text.attr("fill", "#000");
                    cellGroup.push(rect);
                    cellGroup.push(text);

                    cellGroup.attr({
                        cursor:'pointer',
                    }).mousedown(function() {
                        var coordStr = String(cell.x * realCellSize);
                        coordStr += ',';
                        coordStr += String(cell.y * realCellSize);
                        var obstacle = board.obstacles.get(coordStr);
                        if(obstacle == undefined) {
                            var obsType = document.querySelector('input[name="obstacleType"]:checked').value;
                            let obst;
                            if(obsType == "circle" || obsType == "square") {
                                if(obsType == "square"){
                                    obst = paper.rect(x,y,2*cellSize,2*cellSize);
                                } else {
                                    obst = paper.circle(x+cellSize,y+cellSize,cellSize);
                                }
                                obst.mousedown(function() {
                                    board.obstacles.delete(coordStr);
                                    this.remove();
                                });
                                obst.attr({"fill": "#808080", "fill-opacity": 0.5, "stroke-width":3 });
                                board.obstacles.set(coordStr, new Obstacle(cell.x * realCellSize,cell.y*realCellSize,obsType));
                                cellGroup.push(obst);
                                obstaclesInput.value = 
                            }
                            else {
                                board.lidar.remove();
                                obst = paper.rect(x,y,2*cellSize,2*cellSize);
                                obst.attr({"fill": "#f00", "fill-opacity": 0.5, "stroke-width":3 });
                                board.lidar = obst;
                                board.lidarX =  cell.x * realCellSize;
                                board.lidarY = cell.y * realCellSize;
                            }
                        }
                        board.lidar.toFront();
                    });
            }
        }
        function saveBoard() {
            obstacleDiv = $("obstacles");
            obstacles = [];
            board.obstacles.forEach( function (value) {
                obstacles.push(value);
            });
            obstacleDiv.value = JSON.stringify(obstacles);
        }




        createBoard();
        console.log(board);


