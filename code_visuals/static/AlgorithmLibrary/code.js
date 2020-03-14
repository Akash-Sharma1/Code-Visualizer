function Algo(am, w, h)
{
	this.init(am, w, h);
}

Algo.prototype = new Algorithm();
Algo.prototype.constructor = Algo;
Algo.superclass = Algorithm.prototype;

Algo.prototype.init = function(am, w, h)
{
	Algo.superclass.init.call(this, am, w, h);
	
	this.addControls();
	this.nextIndex = 0;

	// TODO:  Add any code necessary to set up your own algorithm.  Initialize data
    // structures, etc.
    
    this.nooflists = 0;
    this.noofdicts = 0;
    this.noofvariables = 0;

    this.lists = [];
    this.lists_vid = []; 
    this.dicts = [];
    this.dicts_vid = [];
    this.variables = [];
    this.variables_vid = [];
    
    var max_vars = 100;
    for(i = 0 ;i < max_vars ;i++){
        lists.append([]);
        dicts.append({});
    }

    this.Ins_num = 0;    
    this.Instructions = [];
    this.Algo.get_instructions();
}

Algo.prototype.get_instructions = funciton()
{

    {% for i in output %}
        temp ={}
        temp['Line'] = {{i["Line"]}}
        temp['action'] = {{i['actions']}}
        Instructions.push(temp);
    {% end for %}
    console.log(Instructions);
}

Algo.prototype.addControls =  function()
{
	this.controls = [];
	
	// Add any necessary controls for your algorithm.
	
		this.NextButton = addControlToAlgorithmBar("Button", "Next Step");
	    this.NextButton.onclick = this.next_instruction.bind(this);
        this.controls.push(this.NextButton);
        
    //where myCallback is a method on this function that implemnts the callback
}

Algo.prototype.reset = function()
{
	// Reset all of your data structures to *exactly* the state they have immediately after the init function is called.
    
    var nooflists = 0;
    var noofdicts = 0;
    var noofvariables = 0;
    
    var lists = [];
    var lists_vid = []; 
    var dicts = [];
    var dicts_vid = [];
    var variables = [];
    var variables_vid = [];
    
    var max_vars = 100;
    for(i = 0 ;i < max_vars ;i++){
        lists.append([]);
        dicts.append({});
    }
	this.nextIndex = 0;
    this.Ins_num = 0;
}

//////////////////////////////////////////////
// Callbacks:
//////////////////////////////////////////////
//
//   All of your callbacks should *not* do any work directly, but instead should go through the
//   implement action command.  That way, undos are handled by ths system "behind the scenes"
//
//   A typical example:
//
//Algo.prototype.insertCallback = function(event)
//{
//	// Get value to insert from textfield (created in addControls above)
//	var insertedValue = this.insertField.value;
//
//  // If you want numbers to all have leading zeroes, you can add them like this:
//	insertedValue = this.normalizeNumber(insertedValue, 4);
//
//  // Only do insertion if the text field is not empty ...
//	if (insertedValue != "")
//	{
//		// Clear text field after operation
//		this.insertField.value = "";
//      // Do the actual work.  The function implementAction is defined in the algorithm superclass
//		this.implementAction(this.insertElement.bind(this), insertedValue);
//	}
//}

Algo.prototype.next_instruction = function(event){

    if (this.Instructions.length < this.Ins_num){
        
        //highlight(Ins_num);
        var i = this.Ins-num;
        var curr_line = this.Instructions[i]['Line'];
        for(j=0;j<this.Instructions[i].length;j++){
            
            var action = this.Instructions[i]['actions'][j];
            var  One_step = {};
            
            if( action['about']=="Initialize" ){
                // Variable value
                One_step['val_type'] = type(action["val"])
                One_step['val'] = action["val"]
            } 
            else if( action['about']=="Change" ){
                // variable index/key prev_value new_value
                One_step['val_type'] = type(action["new_val"])
                One_step['var_name'] = action["var"]
                One_step['new_val'] = action["new_val"]
                One_step['prev_val'] = action["prev_val"]

                if ( action['var_type'] = "List" ){

                    One_step['index'] = action["index"]
                }
                else if ( action['var_type'] = "Dict" ){
                    
                    One_step['key'] = action["key"]
                }
            }
            else if( action['about']=="Add" ){
                // variable index/key value
                One_step['var_name'] = action["var"]
                One_step['val_type'] = type(action["val"])
                One_step['val'] = action["val"]

                if ( action['var_type'] = "List" ){

                    One_step['index'] = action["index"]

                }
                else if ( action['var_type'] = "Dict" ){
                    
                    One_step['key'] = action["key"]
                }
            }
            else if( action['about']=="Remove" ){
                // variable index/key 
                One_step['var_name'] = action["var"]
                
                if ( action['var_type'] = "List" ){

                    One_step['index'] = action["index"]

                }
                else if ( action['var_type'] = "Dict" ){
                    
                    One_step['key'] = action["key"]
                }
            }
        }
        this.Ins_num++;
    }

}

//  Note that implementAction takes as parameters a function and an argument, and then calls that
//  function using that argument (while also storing the function/argument pair for future undos)

//////////////////////////////////////////////
// Doing actual work
//////////////////////////////////////////////
//   The functions that are called by implementAction (like insertElement in the comments above) need to:
//
//      1. Create an array of strings that represent commands to give to the animation manager
//      2. Return this array of commands
//
//    We strongly recommend that you use the this.cmd function, which is a handy utility function that
//    appends commands onto the instance variable this.commands
//
//    A simple example:
//
//Algo.simpleAction(input)
//{
//	this.commands = [];  // Empty out our commands variable, so it isn't corrupted by previous actions
//
//	// Get a new memory ID for the circle that we are going to create
//	var circleID = nextIndex++;
//	var circleX = 50;
//	var circleY = 50;
//	
//	// Create a circle
//	this.cmd("CreateCircle", circleID, "Label",  circleX, circleY);
//	circleX = 100; 
//	// Move the circle
//	this.cmd("Move", circleID, circleX, circleY);
//	// First Animation step done
//	this.cmd("Step");
//	circleX = 50; 
//	circleY = 100; 
//	// Move the circle again
//	this.cmd("Move", circleID, circleX, circleY);
//	// Next Animation step done
//	this.cmd("Step");
//	// Return the commands that were generated by the "cmd" calls:
//	return this.commands;
//}



// Called by our superclass when we get an animation started event -- need to wait for the
// event to finish before we start doing anything
Algo.prototype.disableUI = function(event)
{
	for (var i = 0; i < this.controls.length; i++)
	{
		this.controls[i].disabled = true;
	}
}

// Called by our superclass when we get an animation completed event -- we can
/// now interact again.
Algo.prototype.enableUI = function(event)
{
	for (var i = 0; i < this.controls.length; i++)
	{
		this.controls[i].disabled = false;
	}
}


var currentAlg;

function init()
{
	var animManag = initCanvas();
	currentAlg = new Algo(animManag, canvas.width, canvas.height);
	
}