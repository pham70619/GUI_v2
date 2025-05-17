#define stpPinY 3
#define stpPinX 2
#define stpPinZ 4

#define dirPinY 6
#define dirPinX 5
#define dirPinZ 7

#define enablePin 8

#define YlimitSwitch 10
#define XlimitSwitch 9
#define ZlimitSwitch 11

void setup() {
  pinMode(stpPinY, OUTPUT);
  pinMode(dirPinY, OUTPUT);
  pinMode(stpPinX, OUTPUT);
  pinMode(dirPinX, OUTPUT);
  pinMode(stpPinZ, OUTPUT);
  pinMode(dirPinZ, OUTPUT);
  pinMode(YlimitSwitch, INPUT_PULLUP);
  pinMode(XlimitSwitch, INPUT_PULLUP);
  pinMode(ZlimitSwitch, INPUT_PULLUP);
  pinMode(enablePin, OUTPUT);

  digitalWrite(enablePin, LOW);
  Serial.begin(115200);

  if (digitalRead(YlimitSwitch) == HIGH) {
    Serial.println("警告：Y軸限位開關已被按下！");
  } else {
    Serial.println("限位開關正常。");
  }
  if (digitalRead(XlimitSwitch) == HIGH) {
    Serial.println("警告：X軸限位開關已被按下！");
  } else {
    Serial.println("限位開關正常。");
  }
  if (digitalRead(ZlimitSwitch) == HIGH) {
    Serial.println("警告：Z軸限位開關已被按下！");
  } else {
    Serial.println("限位開關正常。");
  }
}

void loop() {
  if(Serial.available() > 0){
    String command = Serial.readString();
    command.trim();
    Serial.println("收到指令：" + command);

    if (command.equals("HOME")) {
      Serial.println("馬達歸位啟動...");
      Zhome();
      Yhome();
      Xhome();
    }
    else if (command.equals("START")) {
      Serial.println("啟動開始流程");
      Xstart();
      Ystart();
      Zstart();
      Serial.println("turn");
    }
    else if (command.equals("OK")) {
      Serial.println("OK分類");

 
    }
  }
  delay(1000);
}

void Yhome() {
  digitalWrite(dirPinY, LOW);
  for (int i = 0; i < 1500; i++) {
    if (digitalRead(YlimitSwitch) == HIGH) {
      Serial.println("運行中限位開關被觸發，停止！");
      Yreverse();
      return;
    }
    digitalWrite(stpPinY, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinY, LOW);
    delayMicroseconds(3000);
  }
}

void Xhome() {
  digitalWrite(dirPinX, LOW);
  for (int i = 0; i < 1500; i++) {
    if (digitalRead(XlimitSwitch) == HIGH) {
      Serial.println("運行中限位開關被觸發，停止！");
      Xreverse();
      return;
    }
    digitalWrite(stpPinX, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinX, LOW);
    delayMicroseconds(3000);
  }
}

void Zhome() {
  digitalWrite(dirPinZ, LOW);
  for (int i = 0; i < 1500; i++) {
    if (digitalRead(ZlimitSwitch) == HIGH) {
      Serial.println("運行中限位開關被觸發，停止！");
      Zreverse();
      return;
    }
    digitalWrite(stpPinZ, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinZ, LOW);
    delayMicroseconds(3000);
  }
}

void Yreverse() {
  digitalWrite(dirPinY, HIGH);
  for (int i = 0; i < 100; i++) {
    digitalWrite(stpPinY, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinY, LOW);
    delayMicroseconds(3000);
  }
}

void Xreverse() {
  digitalWrite(dirPinX, HIGH);
  for (int i = 0; i < 100; i++) {
    digitalWrite(stpPinX, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinX, LOW);
    delayMicroseconds(3000);
  }
}

void Zreverse() {
  digitalWrite(dirPinZ, HIGH);
  for (int i = 0; i < 100; i++) {
    digitalWrite(stpPinZ, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinZ, LOW);
    delayMicroseconds(3000);
  }
}
void Xstart() {
  digitalWrite(dirPinX, HIGH);
  for (int i = 0; i < 520; i++) {
    digitalWrite(stpPinX, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinX, LOW);
    delayMicroseconds(3000);
  }
}
void Ystart() {
  digitalWrite(dirPinX, HIGH);
  for (int i = 0; i < 900; i++) {
    digitalWrite(stpPinY, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinY, LOW);
    delayMicroseconds(3000);
  }
}
void Zstart() {
  digitalWrite(dirPinZ, HIGH);
  for (int i = 0; i < 200; i++) {
    digitalWrite(stpPinZ, HIGH);
    delayMicroseconds(3000);
    digitalWrite(stpPinZ, LOW);
    delayMicroseconds(3000);
  }
}