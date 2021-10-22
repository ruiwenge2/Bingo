const socket = io();
const gameboard = document.getElementById("gameboard")
var board;

socket.emit("joined", name, room);

socket.on("gameboard", data => {
  board = data;
  drawBoard();
});

function drawBoard(){
  var html = "";
  for(let row of board){
    html += "<tr>"
    for(let num of row){
      html += `<td>${num}</td>`;
    }
    html += "</tr>";
  }
  gameboard.innerHTML = html;
}