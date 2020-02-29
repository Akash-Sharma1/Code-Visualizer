function array(x,y,s,cid){
    this.x=x;
    this.y=y;
    this.s=s;
    this.cid=cid;
    this.size=0;
    this.add_block = function(){
      this.size+=1;
      var canvas = document.getElementById(this.cid);
      if (canvas.getContext) {
        var ctx = canvas.getContext('2d');
        //ctx.fillStyle = 'rgb(204, 204, 204)';
        ctx.fillRect(this.x, this.y, this.s, this.s);
        this.x = this.x + this.s +25;
      }
    }
    this.makearray = function(size){
      for(i=0;i<size;i++){
        this.add_block();
      }
    }
  }
  function arrow(x,y,leap,cid,len){
    this.x=x;
    this.y=y;
    this.len=len;
    this.leap=leap;
    this.cid=cid;
    this.add_arrow = function(){  
      var canvas = document.getElementById(this.cid);
      if (canvas.getContext) {
        var ctx = canvas.getContext('2d');
        console.log(this.x)
        ctx.beginPath();
        ctx.moveTo(this.x + this.len, this.y+5);
        ctx.lineTo(this.x + this.len + 15, this.y);
        ctx.lineTo(this.x + this.len, this.y-5);
        ctx.fill();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x + this.len, this.y);
        ctx.stroke();
      }
      this.x = this.x + this.len + 15 + this.leap;
    }
  }
  function linkedlist(x,y,s,cid){
    this.x=x;
    this.y=y;
    this.s=s;
    this.cid=cid;
    this.arrow = new arrow(this.x + this.s , this.y + this.s/2 , this.s , 'canvas',10);
    this.add_block = function(){
      var canvas = document.getElementById(this.cid);
      if (canvas.getContext) {
        var ctx = canvas.getContext('2d');
        //ctx.fillStyle = 'rgb(204, 204, 204)';
        ctx.fillRect(this.x, this.y, this.s, this.s);
        this.arrow.add_arrow();
        this.x = this.x + this.s + 25;
      }
    }
  }
  
