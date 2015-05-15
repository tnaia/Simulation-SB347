// Authors: TÃ¡ssio Naia and Sophie Tandonnet
// Last update: 23 Feb 2015.
// This is free software, GPL3 or later.
//
//
// Drawing curves
// ==============
// Press 1 or 2 to alternate between editing 2 or 3 curves.
// Press any key (other than 1 or 2) to save the graph currently seen.
// - 1 curve data saved to output-1bar.csv
// - 2 curve data saved to toutput-2bar.csv (order of columns: male, female and hermafrodite)
//
// Press ESC to close.
//
  

// columns: male, female, hermafrodite
int margin = 18;
int day_time_points = 3;
int ndays = 5;
int n_cols = ndays*day_time_points+1;
int n_rows = 200; // => 168
int hstep = 30; // 5
int vstep = 3; // 3
int current_col = 0;
int aux;
String output_filename_prefix = "output_test";


int scr_w = hstep*n_cols +2*margin;
int scr_h = vstep*n_rows +2*margin;

int min_x = margin;
int min_y = margin;
int max_x = min_x + hstep*n_cols;
int max_y = min_y + vstep*n_rows;

boolean single_bar = false;
int[][] bar_value = new int[n_cols][2];
int[] single_bar_value = new int[n_cols];

void set_bars_default() {
  for(int i=0; i< n_cols; i++) {
       bar_value[i][0] = n_rows/3; 
       bar_value[i][1] = n_rows/3; 
       single_bar_value[i] = n_rows/2;
  }
}

// Save bars to output file and quit.
void save_graph() {
  // We will need to read and write
  PrintWriter output;

  // We can open the file.
  if(single_bar) {
    output = createWriter(output_filename_prefix + "-1bar.csv");
  
    for(int j=0; j< n_cols; j++) { 
      int aux1, aux2, aux3;
      aux1 = single_bar_value[j];
      aux2 = n_rows -aux1;
      if (aux2 < 0) aux2 = 0;
  //    print(bar_value[j][0] +","+ bar_value[j][1] + " --> ");
  //    print(aux1 +","+ aux2 +","+ aux3 +","+ n_rows + " --> ");
  //    println(nf((float)(aux1) / n_rows,1,2) + "," + nf((float)(aux3)/n_rows,1,2) + "," + nf((float)(aux2)/n_rows,1,2));
      output.println(nf((float)(aux1) / n_rows,1,2) + "," + nf((float)(aux2)/n_rows,1,2));
    }
  } else {
    output = createWriter(output_filename_prefix + "-2bars.csv");
  
    for(int j=0; j< n_cols; j++) { 
      int aux1, aux2, aux3;
      aux1 = bar_value[j][0];
      aux2 = bar_value[j][1];
      aux3 = n_rows - aux1 -aux2;
      if (aux3 < 0) aux3 = 0;
  //    print(bar_value[j][0] +","+ bar_value[j][1] + " --> ");
  //    print(aux1 +","+ aux2 +","+ aux3 +","+ n_rows + " --> ");
  //    println(nf((float)(aux1) / n_rows,1,2) + "," + nf((float)(aux3)/n_rows,1,2) + "," + nf((float)(aux2)/n_rows,1,2));
      output.println(nf((float)(aux1) / n_rows,1,2) + "," + nf((float)(aux3)/n_rows,1,2) + "," + nf((float)(aux2)/n_rows,1,2));
    }
  }
  
  output.flush(); // Writes the remaining data to the file
  output.close(); // Finishes the file
//  exit(); // Stops the program
}

void setup() {
  size(scr_w,scr_h);  // Size should be the first statement
  set_bars_default();
  
  frameRate(500); 
  //print(min_x + "," + min_y + "," + max_x + "," + max_y);
}

void draw() {
  background(#ffd9d9);
  noStroke();
  
  int pct_mal = 0;
  int pct_her = 0;
  int pct_upper = 0;
  for(int i=0; i < n_cols; i++) {
    if(single_bar) {
      pct_upper += single_bar_value[i];
      for(int j=0; j<n_rows -single_bar_value[i]; j++) {
        fill(#cc5050);
        rect(min_x + hstep* i, min_y+ vstep*j,hstep,vstep-1);
      }
  
      for(int j=n_rows -single_bar_value[i]; j<n_rows; j++) {
        fill(#5050cc);
        rect(min_x + hstep* i, min_y+ vstep*j,hstep,vstep-1);
      }
 
    } else {
      pct_mal += bar_value[i][0];
      pct_her += bar_value[i][1];
      for(int j=0; j<bar_value[i][0]; j++) {
        fill(#aaaaaa);
        rect(min_x + hstep* i, min_y+ vstep*j,hstep,vstep-1);
      }
  
  
      for(int j=bar_value[i][0]; j<n_rows -bar_value[i][1]; j++) {
        fill(#cc5050);
        rect(min_x + hstep* i, min_y+ vstep*j,hstep,vstep-1);
      }
      //for(int j=bar_value[i][0]; j<n_rows -bar_value[i][1]; j++) {
      //  fill(#cc7070);
      //  rect(min_x + bsz* i +1, min_y+ bsz*j,bsz-2,bsz-2);
      //}
  
      for(int j=n_rows -bar_value[i][1]; j<n_rows; j++) {
        fill(#5050cc);
        rect(min_x + hstep* i, min_y+ vstep*j,hstep,vstep-1);
      }
    }
  }
  if(single_bar) {
    textSize(42);
    fill(0);
    textAlign(LEFT);
    
    text("upper: " + nf((float(100*( n_cols*n_rows - pct_upper))) / (n_cols*n_rows),1,1) + "%",margin,height-2*42-margin);
    text("lower: " + nf((float(100*pct_upper)) / (n_cols*n_rows),1,1) + "%",margin,height-42-margin); 
    if(mouseX > 0 && mouseX < max_x && mouseY > 0 && mouseY < height) {  
      aux = (mouseY -min_y)/vstep;
      if(aux < 0) aux = 0;
      if(aux > n_rows) aux = n_rows;
      
      current_col = (mouseX -min_x)/hstep;
      if(current_col < 0) current_col = 0;
      if(current_col >= n_cols) current_col = n_cols -1;
    }
    textAlign(CENTER);
    text(nf(current_col,3) + "," + nf(aux,3), width/2, height/2);
    text(nf(single_bar_value[current_col],3) +","+ nf(n_rows -single_bar_value[current_col],1),width/2,height/2+42);
      
    
    if(mousePressed) { 
      single_bar_value[current_col] = n_rows -aux;
    }
    
    
    
    
  } else {
    textSize(42);
    fill(0);
    textAlign(LEFT);
    
    text("male: " + nf((float(100*pct_mal)) / (n_cols*n_rows),1,1) + "%",margin,height-3*42-margin);
    text("female: " + nf((float(100*( n_cols*n_rows - pct_mal -pct_her))) / (n_cols*n_rows),1,1) + "%",margin,height-2*42-margin);
    text("hermafrodite: " + nf((float(100*pct_her)) / (n_cols*n_rows),1,1) + "%",margin,height-42-margin);
  
    if(mouseX > 0 && mouseX < max_x && mouseY > 0 && mouseY < height) {  
      aux = (mouseY -min_y)/vstep;
      if(aux < 0) aux = 0;
      if(aux > n_rows) aux = n_rows -1;
      
      current_col = (mouseX -min_x)/hstep;
      if(current_col < 0) current_col = 0;
      if(current_col > n_cols) current_col = n_cols -1;
    }
    textAlign(CENTER);
    text(current_col + "," + aux, width/2, height/2);
    text(bar_value[current_col][0] +","+ (n_rows -bar_value[current_col][0] -bar_value[current_col][1]) +","+ bar_value[current_col][1],width/2,height/2+42);
      
    
    if(mousePressed) { 
      // Change value of bars
      int column_to_change = 0;
      if(mouseButton == LEFT && !(keyPressed)) {
        column_to_change = 1;
        text("Hermafrodite rate (blue)",width/2,height/2+2*42);
      } else {
        text("Male rate (gray)",width/2,height/2+2*42);
      }
        
      
      if(column_to_change == 1) bar_value[current_col][column_to_change] = n_rows -aux  ;
      else bar_value[current_col][column_to_change] = aux;
      if(bar_value[current_col][0] + bar_value[current_col][1] > n_rows) {
        bar_value[current_col][1-column_to_change] = n_rows - bar_value[current_col][column_to_change];
      }
    }
  }
  for(int i=0;i<=ndays;i++) {
      // draw hourly bar (time point-hourly)
      stroke(#000000);
      line(min_x +hstep*i*day_time_points,min_y,min_x +hstep*i*day_time_points,max_y);
  }



  if(keyPressed) {
    if(key == '1') single_bar = true;
    else if(key == '2') single_bar = false;
    else save_graph();
  }
}
