function block(x,y,s,cid,elem){
  this.x=x;
  this.y=y;
  this.elem=elem;
  this.s=s;
  this.cid=cid;
  this.show = function(){
    var canvas = document.getElementById(this.cid);
    if (canvas.getContext) {
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = 'rgb(51, 204, 51)';
      ctx.fillRect(this.x, this.y, this.s, this.s);
      ctx.fillStyle = 'rgb(0, 0, 0)';
      ctx.font = "30px Comic Sans MS";
      ctx.fillText(this.elem, this.x+this.s/9, this.y+(3*this.s/4) ,7*this.s/9);
    }
  }
}
function block_n_arrow(x,y,s,cid,elem){
  this.x=x;
  this.y=y;
  this.s=s;
  this.elem=elem;
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
      
      ctx.fillStyle = 'rgb(102, 255, 102)';
      ctx.fillText(this.elem, this.x, this.y, this.s)
    }
  }
}

function clear_canvas(cid){
  var c = document.getElementById(cid);
  var ctx = c.getContext("2d");
  ctx.clearRect(0, 0, c.height, c.width);
}

function array(size,y_coord,Element,canvas){
  var arr = [];
  for(canvas_orig_index = 0; canvas_orig_index < size; canvas_orig_index++){
    newp = new block(canvas_orig_index*54,54*y_coord,50,canvas,Element);
    //newp.show();
    arr.push(newp);
  }
  return arr;
}

function linked_list(size,y_coord,Element){
  var ll = [];
  for(canvas_orig_index = 0; canvas_orig_index < size; canvas_orig_index++){
    newp = new block_n_arrow(canvas_orig_index*75,52*y_coord,50,'canvas',Element);
    //newp.show();
    ll.push(newp);
  }
  return ll;
}