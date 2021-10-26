const socket = io();
const gameboard = document.getElementById("gameboard");
const players = document.getElementById("players");
const chat = document.getElementById("chat");
var board;

socket.emit("joined", name, room);

socket.on("gameboard", data => {
  board = data;
  drawBoard();
  addEventListeners();
});

socket.on("new player", data => {
  players.innerHTML += `<p id="player_${data.sid}">${decodeHTML(data.name)}</p>`;
});

function drawBoard(){
  var html = "";
  rownum = 0;
  colnum = 0;
  for(let row of board){
    html += "<tr>"
    for(let num of row){
      html += `<td id="row${rownum}col${colnum}" data-row="${rownum}" data-col=${colnum}>${Object.keys(num)[0]}</td>`;
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
  alert(element.dataset.row + " " +  element.dataset.col);
}

function decodeHTML(text){
  var div = document.createElement("div");
  div.innerText = text;
  return div.innerHTML;
}

function generateNumber(){
  socket.emit("generate", room);
}