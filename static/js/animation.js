var bg;
var x = 0;
let cloud_1;

var a_x;
var a_y;
var b_x;
var b_y;
var pos_x = 0;
var pos_y = 0;

var fade = 255;

function setup() {
  // The background image must be the same size as the parameters
  // into the createCanvas() method. In this program, the size of
  // the image is 720x400 pixels.
  background(255, 0, 200);

  cloud_1 = loadImage("static/assets/cloud_1.png");
  cloud_2 = loadImage("static/assets/cloud_2.png");
  cloud_3 = loadImage("static/assets/cloud_3.png");
  cloud_4 = loadImage("static/assets/cloud_4.png");
  car_0 = loadImage("static/assets/vehicle_0_4.png");
  car_1 = loadImage("static/assets/vehicle_0_2.png");
  baloon = loadImage("static/assets/baloon.png");
  bg = loadImage("static/assets/story_0_15.png");
  let canvas = createCanvas(1920/1.76, 1080/1.76);
  canvas.parent('canvas')

  cloud1 = new MoveObject(cloud_1);
  cloud2 = new MoveObject(cloud_2);
  cloud3 = new MoveObject(cloud_3);
  cloud4 = new MoveObject(cloud_4);
  cloud5 = new MoveObject(cloud_1);
  cloud6 = new MoveObject(cloud_2);
  cloud7 = new MoveObject(cloud_3);
  cloud8 = new MoveObject(cloud_4);
  baloon = new MoveObject(baloon);
}

function draw() {
  background(bg);
  
  pos_x += 2.1;
  pos_y += -1;
  a_x = -100+pos_x;
  a_y = 350+pos_y;
  b_x = 1200-pos_x;
  b_y = 195-pos_y;
  image(car_0, a_x, a_y, 40, 40);
  image(car_1, b_x, b_y, 40, 40);
  print(pos_x);
  if (a_x>=800){
      pos_x = 0;
      pos_y = 0;
  }

  cloud1.move();
  cloud1.display();
  cloud2.move();
  cloud2.display();
  cloud3.move();
  cloud3.display();
  cloud4.move();
  cloud4.display();
  cloud5.move();
  cloud5.display();
  cloud6.move();
  cloud6.display();
  cloud7.move();
  cloud7.display();
  baloon.move();
  baloon.display();

  fill(255, fade)
  rect(0, 0, width, height)
  if (fade>=0){
    fade -= 1;
  }
}

function MoveObject(img_name) {

    this.x = random(width);
    this.y = random(height);
    this.w = 150;
    this.h = 80;

    this.move = function() {
        this.x += 0.5;
        this.y += 0.3;
        if (this.y >= height || this.x >= width) {
            this.x = random(-300, 800);
            this.y = random(-500, -300);
        }
    };

    this.display = function() {
        image(img_name, this.x, this.y, 300, 300);

        obj = createGraphics(300, 300);
        noStroke();
        fill(0, 12);
        ellipse(this.x+150, this.y+280, this.w, this.h);
    }
}