#define stpPinZ 4
#define dirPinZ 7
#define turnTableStp 2
#define turnTableDir 5
#define enablePin 8
#define ZlimitSwitch 9

//控制爪子套件
#include <Servo.h>

// 建立馬達物件
Servo myServo;


void setup() {
  pinMode(stpPinZ, OUTPUT);
  pinMode(dirPinZ, OUTPUT);
  pinMode(turnTableStp, OUTPUT);
  pinMode(turnTableDir, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(ZlimitSwitch, INPUT_PULLUP);

//  宣告爪子控制腳位
  myServo.attach(10);
  
  // enable Stepper motor
  digitalWrite(enablePin, LOW);
  Serial.begin(115200);

  if (digitalRead(ZlimitSwitch) == HIGH) {
    Serial.println("警告：限位開關已被按下！");
  } else {
    Serial.println("限位開關正常。");
  }
}





void home(){
  Serial.println("home void available");
  digitalWrite(dirPinZ, HIGH); //歸0方向
  for (int i = 0; i < 1500; i++) {
    if (digitalRead(ZlimitSwitch) == HIGH) {
      Serial.println("運行中限位開關被觸發，停止！");
      reverse();
      return;
    }
    digitalWrite(stpPinZ, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinZ, LOW);
    delayMicroseconds(3000);
  }
}

void reverse(){
  Serial.println("reserse available");
  digitalWrite(dirPinZ, LOW);
  for (int i = 0; i < 50; i++) {
    digitalWrite(stpPinZ, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinZ, LOW);
    delayMicroseconds(3000);
  }
}

void turn(){
  Serial.println("turning....");
//  轉動方向定義
  digitalWrite(turnTableDir, LOW);
  for (int i = 0; i < 50; i++) {
    digitalWrite(turnTableStp, HIGH);
    delayMicroseconds(3000);
    digitalWrite(turnTableStp, LOW);
    delayMicroseconds(3000);
  }
  Serial.println("TURN OVER");
}

void clip_close(){
  myServo.write(90);
  Serial.println("已夾緊");
}

void clip_open(){
  myServo.write(0);
  Serial.println("已打開");
}

void down(){
  Serial.println("downing...");
  digitalWrite(dirPinZ, LOW);
  for (int i = 0; i < 250; i++) {
    digitalWrite(stpPinZ, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinZ, LOW);
    delayMicroseconds(3000);
  }
}

void up(){
  Serial.println("downing...");
  digitalWrite(dirPinZ, HIGH);
  for (int i = 0; i < 250; i++) {
    digitalWrite(stpPinZ, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinZ, LOW);
    delayMicroseconds(3000);
  }
}


void loop() {
  if(Serial.available() > 0){
    String command = Serial.readString();//SERIAL函數 將SERIAL讀到字串變成變數
    command.trim();//刪減成能理解的指令
    Serial.println("收到指令：" + command);

    if (command.equals("HOME")) {
      Serial.println("馬達歸位啟動...");
      home();
    }else if(command.equals("TURN")){
      Serial.println("turn");
      turn();
    }else if(command.equals("CLIP_CLOSE")){
      Serial.println("clip_close");
      clip_close();
    }else if(command.equals("CLIP_OPEN")){
      Serial.println("clip_open");
      clip_open();
    }else if(command.equals("DOWN")){
      Serial.println("down");
      down();
    }else if(command.equals("UP")){
      Serial.println("up");
      up();
    }
  }
    delay(50);
  };
