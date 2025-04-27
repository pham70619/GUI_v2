#define stpPinY 2
#define dirPinY 5
#define enablePin 8
#define YlimitSwitch 10

void setup() {
  pinMode(stpPinY, OUTPUT);
  pinMode(dirPinY, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(YlimitSwitch, INPUT_PULLUP);

  digitalWrite(enablePin, LOW);
  Serial.begin(115200);

  if (digitalRead(YlimitSwitch) == HIGH) {
    Serial.println("警告：限位開關已被按下！");
  } else {
    Serial.println("限位開關正常。");
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
    };
  };
  delay(1000);
}

void home(){
  digitalWrite(dirPinY, LOW); //歸0方向
  for (int i = 0; i < 1500; i++) {
    if (digitalRead(YlimitSwitch) == LOW) {
      Serial.println("運行中限位開關被觸發，停止！");
      reverse();
      return;
    }
    digitalWrite(stpPinY, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinY, LOW);
    delayMicroseconds(3000);
  }
}

void reverse(){
  digitalWrite(dirPinY, HIGH);
  for (int i = 0; i < 100; i++) {
    digitalWrite(stpPinY, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinY, LOW);
    delayMicroseconds(3000);
  }
}