import('https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.8/socket.io.min.js')

var canvas = document.getElementById('canvas'),
    ctx = canvas.getContext('2d');

(function() {
    window.addEventListener('resize', resizeCanvas, false);

    function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
    }
    resizeCanvas();
})();

canvas.addEventListener('mousemove', function(e){
  cursor_pos[0] = e.pageX - e.target.offsetLeft;
  cursor_pos[1] = e.pageY - e.target.offsetTop;
});

function draw_circle_at(x, y, r, img){
  ctx.save();

  ctx.beginPath();
  ctx.arc(x,y,r,0,2*Math.PI);
  ctx.closePath();
  ctx.clip();

  ctx.drawImage(img ,x-r, y-r, 2*r, 2*r);
  ctx.globalCompositeOperation = 'source-in';

  ctx.restore();
}

function gameloop() {
  update()
  draw()

}

var cursor_pos=[0,0];

var image = new Image();
image.src="https://i.kym-cdn.com/entries/icons/mobile/000/013/564/doge.jpg";

var image2 = new Image();
image2.src='http://d279m997dpfwgl.cloudfront.net/wp/2018/05/0514_blue-1000x667.jpg';

function start(){

}

function update(){
  socket.emit('update_start', cursor_pos)

}


var state = undefined
function draw(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (var key in state)
      draw_circle_at(
        state[key]['position'][0],
        state[key]['position'][1],
        75,
        image
      )
}

var socket = io.connect('http://127.0.0.1:27002');
var X=-150, Y=-150

socket.on('connect', function() {
    console.log('connected');
});

socket.on('state_changed', function(data) {
  state = data
  console.log(state)
});


start();
setInterval(gameloop, 16);




























//
