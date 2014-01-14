var colourPurple = "#cb3594";
var colourGreen = "#96ff00";
var colourYellow = "#ffed17";
var colourRed = "#ff0000";
var colourOrange = "#ffa500";
var colourPink = "#ec17fe";
var colourBlue = "#17feec";
var colourBlack = "#000000";
var colourDkBlue = "#2220c1";
var colourDkGreen = "#379235";
var colourBrown = "#7A551A"
var colourDkPurple = "#590990"
var colourBlack = "#000000";

var eraser = "#ffffffff";

var clickSize = new Array();
var curSize = "normal";
var radius = 5;

var clickTool = new Array();
var curTool = "crayon";

var canvas = document.getElementById ("tableauCanvas");


var curColour = colourPurple;
var clickColour = new Array();
var clickX = new Array ();
var clickY = new Array();
var clickDrag = new Array ();
var paint;

var ws = new WebSocket("ws://" + SERVER_IP + ":8888/savecanvas/test");

$(document).ready(function (){
context = document.getElementById ('tableauCanvas').getContext("2d");

$('#canvas')
	.mousedown
	(function (e){
		var mouseX = e.pageX - this.offsetLeft;
		var mouseY = e.pageY - this.offsetTop;
        
        clickX.push(-1);
		clickY.push(-1);
        clickSize.push(-1);
        clickColour.push(-1);
        
		paint = true;
		addClick (e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
		redraw();
	})
	.mousemove(function (e){
		if (paint) {
			addClick (e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
			redraw();
		}
	})
	.mouseup(function (e){
		paint = false;
	})
	.mouseleave(function (e){
		paint = false;
	});

	function addClick(x,y,dragging)
	{
		clickX.push(x);
		clickY.push(y);
		clickDrag.push(dragging);
		if(curTool == "eraser"){
			clickColour.push("white");
		}else{
			clickColour.push(curColour);
		}
		clickSize.push(radius);
	}

	function redraw(){
	  
      context.clearRect(0,0,canvas.width, canvas.height);
      if (background)
      	context.drawImage(background,0,0);
	  /*context.strokeStyle = "#df4b26";*/
	  context.lineJoin = "round";
      
	  /*context.lineWidth = 5;*/
			
  	for(var i=0; i < clickX.length; i++) {	
        if(clickSize[i] == -1) continue;
    	context.beginPath();
    	context.lineWidth = clickSize[i] ;
	    context.strokeStyle = clickColour[i];
	    
        if(clickDrag[i] && i && clickSize[i-1] > 0){
	      context.moveTo(clickX[i-1], clickY[i-1]);
	    }else{
	      context.moveTo(clickX[i]-1, clickY[i]);
	    }
	    context.lineTo(clickX[i], clickY[i]);
	    context.closePath();
	    context.stroke();
	}
  		/*
        if(curTool == "crayon"){
  			context.golobalAlpha = 0.4;
  			context.drawImage(crayonTextureImage, 0, 0, canvasWidth, canvasHeight);
  		}

  		context.globalAlpha = 1;*/ 
	}

$('#colourPurple').click(function(){
	curColour = colourPurple;
});

$('#colourGreen').click(function(){
	curColour = colourGreen;
});

$('#colourYellow').click(function(){
	curColour = colourYellow;
});

$('#colourRed').click(function(){
	curColour = colourRed;
});

$('#colourOrange').click(function(){
	curColour = colourOrange;
});

$('#colourPink').click(function(){
	curColour = colourPink;
});

$('#colourBlue').click(function(){
	curColour = colourBlue;
});

$('#colourBlack').click(function(){
	curColour = colourBlack;
});

$('#colourDkBlue').click(function(){
	curColour = colourDkBlue;
});

$('#colourDkGreen').click(function(){
	curColour = colourDkGreen;
});

$('#colourDkPurple').click(function(){
	curColour = colourDkPurple;
});

$("#eraser").click(function(){
	curColour = eraser;
});

$('#clearCanvas').click(function(){
	context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
	clickSize = new Array();
	clickTool = new Array();
	clickColour = new Array();
	clickX = new Array ();
	clickY = new Array();
	clickDrag = new Array ();
});

$('#undoCanvas').click(function(){
	if(clickSize.length == 0) return;
    while(clickSize[clickSize.length-1] >= 0){
        clickSize.pop();
        clickX.pop();
        clickY.pop();
        clickColour.pop();
        }
    clickSize.pop();
    clickX.pop();
    clickY.pop();
    clickColour.pop();
    redraw();
});

$('#sizePencil').click(function(){
	radius = 1;
});

$('#sizeSmall').click(function(){
	radius = 5;
});

$('#sizeMedium').click(function(){
	radius = 10;
});

$('#sizeLarge').click(function(){
	radius = 15;
});

$('#saveCanvas').click(function(){
	var img = canvas.toDataURL();
	ws.send(img); 
	window.alert("Your Image has been Saved Sucessfully !");
});

function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if (pair[0] == variable) {
      return pair[1];
    }
  } 
  return null;
}

if (getQueryVariable("background")) {
	var background = new Image();
	background.src = "/static/images/"+getQueryVariable("background");

	// Make sure the image is loaded first otherwise nothing will draw.
	background.onload = function(){
	    context.drawImage(background,0,0);
	}
}

})
