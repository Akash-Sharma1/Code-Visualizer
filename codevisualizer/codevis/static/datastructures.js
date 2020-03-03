function block(x,y,s,cid){
  this.x=x;
  this.y=y;
  this.s=s;
  this.cid=cid;
  this.show = function(){
    var canvas = document.getElementById(this.cid);
    if (canvas.getContext) {
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = 'rgb(204, 204, 204)';
      ctx.fillRect(this.x, this.y, this.s, this.s);
    }
  }
}
function block_n_arrow(x,y,s,cid){
  this.x=x;
  this.y=y;
  this.s=s;
  this.cid=cid;
  this.len=10
  // arrow length+ tip = 10+15 =25
  this.show = function(){
    var canvas = document.getElementById(this.cid);
    if (canvas.getContext) {
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = 'rgb(204, 204, 204)';
      ctx.fillRect(this.x, this.y, this.s, this.s);
      ctx.beginPath();
      var mid = this.y+(this.s/2);
      var blckend = this.x + this.s;
      ctx.moveTo(blckend + this.len, mid+5);
      ctx.lineTo(blckend + this.len + 15, mid);
      ctx.lineTo(blckend + this.len, mid-5);
      ctx.fill();
      ctx.moveTo(blckend , mid);
      ctx.lineTo(blckend + this.len, mid);
      ctx.stroke();
    }
  }
}

function clear_canvas(cid){
  var c = document.getElementById(cid);
  var ctx = c.getContext("2d");
  ctx.clearRect(0, 0, c.height, c.width);
}

function array(size,y_coord){
  var arr = [];
  for(i=0;i<size;i++){
    newp = new block(i*52,52*y_coord,50,'canvas');
   // console.log(newp)
   // newp.show();
    arr.push(newp);
  }
  return arr;
}
function linked_list(size,y_coord){
  var ll = [];
  for(i=0;i<size;i++){
    newp = new block_n_arrow(i*75,52*y_coord,50,'canvas');
    //newp.show();
    ll.push(newp);
  }
  return ll;
}