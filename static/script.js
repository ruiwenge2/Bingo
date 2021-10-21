function embedded() {
  try {
    return window.self !== window.top;
  } catch(e) {
    return true;
  }
}

if(embedded()){
  document.body.innerHTML = `<p>Please open this in a <a href="https://bingo.ruiwenge2.repl.co" target="_blank">new tab</a> for best results.`;
}

function rename(){
  document.getElementById("rename").style.display = "block";
  document.getElementById("newname").focus();
}