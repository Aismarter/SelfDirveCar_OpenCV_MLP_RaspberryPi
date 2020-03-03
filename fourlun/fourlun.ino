//定义引脚
int Left_motor_go = 8;        //左电机前进 AIN1
int Left_motor_back = 7;      //左电机后退 AIN2

int Right_motor_go = 2;       //右电机前进 BIN1
int Right_motor_back = 4;     //右电机后退 BIN2

int Left_motor_pwm = 6;       //左电机控速 PWMA
int Right_motor_pwm = 5;      //右电机控速 PWMB

int command = 0;
int time = 0;
void setup()
{
  //初始化电机驱动IO口为输出方式
  pinMode(Left_motor_go, OUTPUT);
  pinMode(Left_motor_back, OUTPUT);
  pinMode(Right_motor_go, OUTPUT);
  pinMode(Right_motor_back, OUTPUT);
  Serial.begin(9600);
}
void loop() {
  if (Serial.available() > 0)
  {
    command = Serial.read();
  }
  else
  {
    reset();
  }

   drive(command);
}


void reset()
{
  digitalWrite(Left_motor_go, LOW);
  digitalWrite(Left_motor_back, LOW);
  digitalWrite(Right_motor_go, LOW);
  digitalWrite(Right_motor_back, LOW);
}

// alternatively try 40/60, 250/500
void forward(int time)
{
  //左电机前进
  digitalWrite(Left_motor_go, HIGH);   //左电机前进使能
  digitalWrite(Left_motor_back, LOW);  //左电机后退禁止
  analogWrite(Left_motor_pwm, 120);    //PWM比例0-255调速，左右轮差异略增减

  //右电机前进
  digitalWrite(Right_motor_go, HIGH);  //右电机前进使能
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 120);   //PWM比例0-255调速，左右轮差异略增减
  delay(time);
}

// alternatively try: 50/50
void reverse(int time)
{
  //左电机后退
  digitalWrite(Left_motor_go, LOW);     //左电机前进禁止
  digitalWrite(Left_motor_back, HIGH);  //左电机后退使能
  analogWrite(Left_motor_pwm, 120);

  //右电机后退
  digitalWrite(Right_motor_go, LOW);    //右电机前进禁止
  digitalWrite(Right_motor_back, HIGH); //右电机后退使能
  analogWrite(Right_motor_pwm, 120);

  delay(time);
}

void left(int time)
{
  //左电机停止
  digitalWrite(Left_motor_go, LOW);     //左电机前进禁止
  digitalWrite(Left_motor_back, LOW);   //左电机后退禁止
  analogWrite(Left_motor_pwm, 0);       //左边电机速度设为0(0-255)

  //右电机前进
  digitalWrite(Right_motor_go, HIGH);  //右电机前进使能
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 120);   //右边电机速度设200(0-255)

  delay(time);
}

void right(int time)
{
 //左电机前进
  digitalWrite(Left_motor_go, HIGH);    //左电机前进使能
  digitalWrite(Left_motor_back, LOW);   //左电机后退禁止
  analogWrite(Left_motor_pwm, 120);     //左边电机速度设200(0-255)

  //右电机停止
  digitalWrite(Right_motor_go, LOW);    //右电机前进禁止
  digitalWrite(Right_motor_back, LOW);  //右电机后退禁止
  analogWrite(Right_motor_pwm, 0);      //右边电机速度设0(0-255)
  
  delay(time);
}

void forward_right(int time)
{
  //左电机
  digitalWrite(Left_motor_go, HIGH);     //左电机前进禁止
  digitalWrite(Left_motor_back, LOW);   //左电机后退禁止
  analogWrite(Left_motor_pwm, 120);       //左边电机速度设为0(0-255)

  //右电机
  digitalWrite(Right_motor_go, HIGH);  //右电机前进使能
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 60);   //右边电机速度设200(0-255)

  delay(time);
}


void forward_left(int time)
{
   //左电机停止
  digitalWrite(Left_motor_go, HIGH);     //左电机前进禁止
  digitalWrite(Left_motor_back, LOW);   //左电机后退禁止
  analogWrite(Left_motor_pwm, 60);       //左边电机速度设为0(0-255)

  //右电机前进
  digitalWrite(Right_motor_go, HIGH);  //右电机前进使能
  digitalWrite(Right_motor_back, LOW); //右电机后退禁止
  analogWrite(Right_motor_pwm, 120);   //右边电机速度设200(0-255)

  delay(time);
}

void reverse_right(int time)
{
   //左电机停止
  digitalWrite(Left_motor_go, LOW);     //左电机前进禁止
  digitalWrite(Left_motor_back, HIGH);   //左电机后退禁止
  analogWrite(Left_motor_pwm, 60);       //左边电机速度设为0(0-255)

  //右电机前进
  digitalWrite(Right_motor_go, LOW);  //右电机前进使能
  digitalWrite(Right_motor_back, HIGH); //右电机后退禁止
  analogWrite(Right_motor_pwm, 120);   //右边电机速度设200(0-255)

  delay(time);
}

void reverse_left(int time)
{
   //左电机停止
  digitalWrite(Left_motor_go, LOW);     //左电机前进禁止
  digitalWrite(Left_motor_back, HIGH);   //左电机后退禁止
  analogWrite(Left_motor_pwm, 60);       //左边电机速度设为0(0-255)

  //右电机前进
  digitalWrite(Right_motor_go, LOW);  //右电机前进使能
  digitalWrite(Right_motor_back, HIGH); //右电机后退禁止
  analogWrite(Right_motor_pwm, 120);   //右边电机速度设200(0-255)

  delay(time);
}
void drive(int command)
{
  switch(command)
  {
    
    case 48: reset(); break;
    case 49: forward(50); break;   //左转一小下
    case 50: reverse(50); break;    //右前一下下
    case 51: right(50); break;     //直接往前冲
    case 52: left(50); break;      //直接往后冲
    case 53: forward_right(100);break;     //右转转圈圈
    case 54: forward_left(100);break;    //左转转圈圈
    case 55: reverse_right(100); break;   //右前转圈圈
    case 56: reverse_left(100); break;    //左前转圈圈
    default: break;
  }
}
