$(document).ready(function () {
  const statusRef = document.getElementById("status");
  const msgRef = document.getElementById("message");

  var socket = io.connect();

  //receive details from server
  socket.on("useraction", function (msg) {
    console.log("Received sensorData :: " + msg.id + " :: " + msg.action);
    statusRef.innerHTML = msg.action;
    msgRef.innerHTML = msg.id;
  });
});
