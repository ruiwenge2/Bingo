const socket = io();
const gameboard = document.getElementById("gameboard")
var board;

socket.emit("joined", name, room);

socket.on("gameboard", data => {
  board = data;
  drawBoard();
  addEventListeners();
});

function drawBoard(){
  var html = "";
  rownum = 0;
  colnum = 0;
  for(let row of board){
    html += "<tr>"
    for(let num of row){
      html += `<td id="row${rownum}col${colnum}">${num}</td>`;
      colnum++;
    }
    colnum = 0;
    rownum++;
    html += "</tr>";
  }
  gameboard.innerHTML = html;
  document.getElementById("gameboard-message").innerHTML = "The board has been generated for you."
}

function addEventListeners(){
  var tds = document.getElementsByTagName("TD");
  for(let i = 0; i < tds.length; i++){
    tds[i].addEventListener("click", () => {
      manageGameboardClick(tds[i]);
    });
  }
}

function manageGameboardClick(element){
  alert(element.id)
}