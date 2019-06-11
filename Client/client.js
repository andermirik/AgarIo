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

canvas.addEventListener('mouseover', function(e){
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
var images = [];

addImage("https://i.kym-cdn.com/entries/icons/mobile/000/013/564/doge.jpg")
addImage('https://myfin.by/images/cryptoCurrency/btc.png')
addImage('https://cottagelife.com/wp-content/uploads/2018/06/animal-bear-brown-bear-35435-1200x796.jpg')
addImage('https://printio.ru/c644f9598fcff085850f69766404ccc5.png')
addImage('https://memepedia.ru/wp-content/uploads/2018/06/unnamed-768x768.jpg')
addImage('https://cdn.tproger.ru/wp-content/uploads/2018/10/android-chrome-512x512.png')


function addImage(src){
  image = new Image()
  image.src = src
  images.push(image)
}

function start(){

}

function update(){
  let from = [canvas.width/2, canvas.height/2]
  let to = cursor_pos
  let vector = [from[0]-to[0], from[1]-to[1]]
  let dist = distance(from, to)
  vector = normalize(vector)
  socket.emit('update_start', {'vector':vector, 'distance': dist})
}

function distance(p1, p2){
  return Math.sqrt((p2[0]-p1[0])*(p2[0]-p1[0]) + (p2[1]-p1[1])*(p2[1]-p1[1]))
}

function normalize(vector){
  var speed = Math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
  if(speed != 0)
  {
    vector[0]*= 1/speed
    vector[1]*= 1/speed
  }
  else
  {
    vector[0] = 0
    vector[1] = 0
  }
  return vector
}



var state = undefined
function draw(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (var key in state)
    for(var circle in state[key]['circles']){
      draw_circle_at(
        state[key]['circles'][circle]['position'][0]+canvas.width/2,
        state[key]['circles'][circle]['position'][1]+canvas.height/2,
        state[key]['circles'][circle]['radius'],
        images[state[key]['image_code']]
      )
    }
}

var socket = io.connect('http://127.0.0.1:27002');

socket.on('connect', function() {
    console.log('connected');
});

socket.on('state_changed', function(data) {
  state = data
  console.log(state)
});


start();
setInterval(gameloop, 1000/60);




























//
