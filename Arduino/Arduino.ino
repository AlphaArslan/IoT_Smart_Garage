/******************************************************************
 * Documentation
 * Coded by m.Said (Alpha Arslan)
 * contacts: +201207903371 (WhatsApp available)
 * in : 25/1/2019
 * for: Anwer Al-Zuheiry
******************************************************************/

/**************************** Define *****************************/
//constants
#define       IR_SEG_THRESHOLD    450         //the value below which we consider a NO_CAR case 

//pin coonection
#define       SEG_WIRE            3           //the wire carrying segnal to Raspberry

#define       IR1_SEGNAL          A0           //four sensors MUST stay in a row
#define       IR2_SEGNAL          A1
#define       IR3_SEGNAL          A2
#define       IR4_SEGNAL          A3

#define       green1              4             //Don't change LED connections without consultance 
#define       red1                5

#define       green2              6
#define       red2                7

#define       green3              8
#define       red3                9

#define       green4              11
#define       red4                12

/************************* Global Var. ***************************/
uint8_t ir1 = 0 ;
uint8_t ir2 = 0 ;
uint8_t ir3 = 0 ;
uint8_t ir4 = 0 ;

/************************** Functions ****************************/
bool chick_ir(char);                  //takes the number of IR and returns True if there is a car on it + controls LEDs 


/**************************** Setup() ****************************/
void setup(){
  pinMode(IR1_SEGNAL ,INPUT);
  pinMode(IR2_SEGNAL ,INPUT);
  pinMode(IR3_SEGNAL ,INPUT);
  pinMode(IR4_SEGNAL ,INPUT);

  pinMode(SEG_WIRE ,OUTPUT);
  
  pinMode(green1 ,OUTPUT);
  pinMode(red1   ,OUTPUT);
  pinMode(green2 ,OUTPUT);
  pinMode(red2   ,OUTPUT);
  pinMode(green3 ,OUTPUT);
  pinMode(red3   ,OUTPUT);
  pinMode(green4 ,OUTPUT);
  pinMode(red4   ,OUTPUT);
}
/**************************** loop() *****************************/
void loop(){
  ir1 = (chick_ir(1) ? 1 : 0 );
  ir2 = (chick_ir(2) ? 1 : 0 );
  ir3 = (chick_ir(3) ? 1 : 0 );
  ir4 = (chick_ir(4) ? 1 : 0 );

  digitalWrite(SEG_WIRE , (ir1+ir2+ir3+ir4)/4);
}

/*********************** Func. Definition *************************/
bool chick_ir(char index){
  if(analogRead(IR1_SEGNAL + index -1) > IR_SEG_THRESHOLD){
    digitalWrite(red1 + (index -1)*2  ,HIGH);
    digitalWrite(green1 + (index -1)*2  ,LOW);
    return 1 ;
  }
  
  digitalWrite(red1 + (index -1)*2  ,LOW);
  digitalWrite(green1 + (index -1)*2  ,HIGH);
  return 0;
}

