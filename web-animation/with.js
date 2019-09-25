var labels = [data,floor_one,floor_two,floor_three];
var floor_number=1 ;
var emphasis_factor = 2;
var t=0;
var fr = 30;
var original_x=300;

var userdata;
var mag_dict;
var phase_dict ;
var freq_dict ;
var lower_x;
var current_x;

function setup(){
    createCanvas(750,500); 
    frameRate(fr);
}

function draw()
{   
    
    // collect data from user input 
    floor_number = document.getElementById("whichfloor").value;      
    userdata = JSON.parse(labels[floor_number]);
    mag_dict = userdata[0];
    phase_dict = userdata[1];
    freq_dict = userdata[2];  
    var slider = document.getElementById("myRange");
    input_frequency = slider.value;    
    background(245,245,220);
    

    // the stored data is discrete, so we need to find the nearest neighbour to the user's input
    var actual_frequency = freq_dict['ffloor'].reduce(function(prev, curr) {
        return (Math.abs(curr - input_frequency) < Math.abs(prev - input_frequency) ? curr : prev);
      });
    
    var indx= (freq_dict['ffloor'].indexOf(actual_frequency)); 
      // this array will store the height,amplitude, and phase for each floor
    var coords = [[490,40,0],
    [340,mag_dict['ffloor'][indx],phase_dict['ffloor'][indx]],
    [210,mag_dict['mfloor'][indx],phase_dict['mfloor'][indx]],
    [60,mag_dict['tfloor'][indx],phase_dict['tfloor'][indx]]];
    
    //draw the actual animation 

    lower_x=original_x + (coords[0][1]* Math.sin(t*2*Math.PI*input_frequency));
    ground_x=lower_x;
    fill(200, 200, 200);    
    strokeWeight(1.5);
    rect(lower_x,coords[0][0],60,5);

    for (i=1;i<4;i++)
    { 
        current_x=ground_x + (coords[i][1]*emphasis_factor*10000*Math.sin((t*2*Math.PI*input_frequency)+coords[i][2]));
    
        rect(current_x,coords[i][0],60,5);
        line(lower_x,coords[i-1][0],current_x,coords[i][0]+6);
        
        line(lower_x+60,coords[i-1][0],current_x+60,coords[i][0]+6);
        lower_x = current_x;

    }

    //draw the animation for the building
    if(floor_number!=0)
    {
        var damper_x = ground_x + 30+ (coords[floor_number][1]*emphasis_factor* 10000*Math.sin((t*2*Math.PI*input_frequency)+coords[floor_number][2]));
        var damper_y= coords[floor_number][0]
        var length_of_rod = 50;
        var damper_amplitude = mag_dict['damper'][indx];
        var damper_phase = phase_dict['damper'][indx];

        var damper_angle = damper_amplitude*25*Math.sin((t*2*Math.PI*input_frequency)+damper_phase);
        var pendulum_x = (length_of_rod *Math.sin(damper_angle)) + damper_x;
        var pendulum_y = damper_y+(length_of_rod* Math.cos(damper_angle));

        line(damper_x,damper_y,pendulum_x,pendulum_y);
        ellipse (pendulum_x,pendulum_y,20,20);

    }
    

    t+= 1/(fr * 10 );

}