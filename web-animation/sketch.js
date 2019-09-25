var userdata = JSON.parse(data);
var mag_dict = userdata[0];
var phase_dict = userdata[1];
var freq_dict = userdata[2];
var lower_x;
var current_x;
var fr = 30;
var input_frequency=document.getElementById("demo"); 
var original_x=300;
var actual_frequency = freq_dict['ffloor'].reduce(function(prev, curr) {
    return (Math.abs(curr - input_frequency) < Math.abs(prev - input_frequency) ? curr : prev);
  });
  

var indx= (freq_dict['ffloor'].indexOf(actual_frequency));

function setup(){
    createCanvas(750,500); 
    frameRate(fr);
}

var coords = [[450,40,0],
[350,mag_dict['ffloor'][indx],phase_dict['ffloor'][indx]],
[250,mag_dict['sfloor'][indx],phase_dict['sfloor'][indx]],
[150,mag_dict['tfloor'][indx],phase_dict['tfloor'][indx]]];






var t=0;

function draw()
{
  var slider = document.getElementById("myRange");
  input_frequency = slider.value;
    
    


    var actual_frequency = freq_dict['ffloor'].reduce(function(prev, curr) {
        return (Math.abs(curr - input_frequency) < Math.abs(prev - input_frequency) ? curr : prev);
      });
    console.log(actual_frequency);
    
    var indx= (freq_dict['ffloor'].indexOf(actual_frequency)); 

    var coords = [[490,40,0],
    [340,mag_dict['ffloor'][indx],phase_dict['ffloor'][indx]],
    [210,mag_dict['sfloor'][indx],phase_dict['sfloor'][indx]],
    [60,mag_dict['tfloor'][indx],phase_dict['tfloor'][indx]]];

   
    background(245,245,220);
    
    lower_x=original_x + (coords[0][1]* Math.sin(t*2*Math.PI*input_frequency));
    ground_x=lower_x;
    fill(200, 200, 200);    
    strokeWeight(1.5);
    rect(lower_x,coords[0][0],60,5);

    for (i=1;i<4;i++)
    { 
        current_x=ground_x + (coords[i][1]*10000*Math.sin(t*2*Math.PI*input_frequency+coords[i][2]));
        rect(current_x,coords[i][0],60,5);
        line(lower_x,coords[i-1][0],current_x,coords[i][0]+6);
        
        line(lower_x+60,coords[i-1][0],current_x+60,coords[i][0]+6);
        lower_x = current_x;

    }

    t+= 1/(fr * 10 );

}