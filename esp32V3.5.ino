//define

//include
#include <math.h>

//global variables
const int pinADC = 25;
float analogVolts = 0;

int prevTime = 0;
int tim = 0;

const int ilePomDoBuff = 100; //ile pomiarow jest wysylanych
const int maxBufforu = 25000;
unsigned int bufforADC[maxBufforu];
int ileDanychWBADC = 0; //ile pom jest obecnie (ktory element jest najnowszy)

TaskHandle_t Task1;
const int freq = 10000; //czestotliwosc pomiarow
int czasDelay = 1000000/freq;

int iter=0;
int sto=0;
int ostatniaWyswietlonaSeria = 0;
bool czyWyswietlone = true;

//functions
void readADC(int pinNum)
{
  //ok. 9kHz kiedy wypisuje czestotliwosc + wartosci
  // read the millivolts value for pin pinNum:
  bufforADC[ileDanychWBADC] = analogReadMilliVolts(pinNum);//
  //bufforADC[ileDanychWBADC] -= 1690;

  //bufforADC[ileDanychWBADC] = iter++;
  
  //Serial.printf("ileDanychWBADC%d\n", ileDanychWBADC);
  
  ileDanychWBADC++;

  if ((ileDanychWBADC+1)%ilePomDoBuff==0)
  {
    tim = (micros() - prevTime) /ilePomDoBuff;
    //Serial.printf("mamy100: %d ", ++sto);
    czyWyswietlone=false;
    prevTime=micros();
  }
  
  if (ileDanychWBADC==maxBufforu) 
  {
    //tim = (micros() - prevTime) /ileDanychWBADC;
    //tim/=ileDanychWBADC;
    //prevTime=micros();

    ileDanychWBADC=0; //zeby nie wyszlo poza buffor
  }
}

void wyswietlBuffor(int od)
{
  //Serial.printf("wyswietlBuffor od%d\n", od);
/*    
  tim = micros() - prevTime;
  tim/=ilePomDoBuff;
*/
  Serial.printf("%d\t", tim);//tim w jednostce us
 
  //Serial.printf("%d\t", czasDelay);//czas w jednostce us

  for(int i=od; i<ilePomDoBuff+od; i++)
     Serial.printf("%d\t", bufforADC[i]);
  Serial.printf("\n");
/*  
  prevTime=micros();
*/
  czyWyswietlone=true;
}

//main
void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(1000000);
  
  //set the resolution to 12 bits (0-4096), dokladnosc = 0,732421875 mV
  analogReadResolution(12);

  //utworzenie nowego watku (uzycie 2go rdzenia)
  xTaskCreatePinnedToCore(Task1code,"Task1",10000,NULL,0,&Task1,0);

  delay(1000);
  prevTime = micros();
}

void loop() {
  //prevTime=micros();
  
  //funkcja do pomiaru napiecia
  if(ileDanychWBADC+1==(ostatniaWyswietlonaSeria-1)*ilePomDoBuff)
  {
    //Serial.println("nie nadaza wyswietlac");
    Serial.println("\nxd\n");
    czyWyswietlone=false;
    delayMicroseconds(1000);
  }
  else readADC(pinADC);
  //delayMicroseconds(czasDelay); //ustala czestotliwosc pomiarow
  //vTaskDelay(czasDelay/1000);
  delayMicroseconds(400);//~+100ms na pomiary (75 = min)
  
  //tim = micros() - prevTime;
  //Serial.printf("tim%d\t", tim);
}

void Task1code( void * pvParameters )   // pracuje na rdzeniu 0
{
 // polecenia wykonywane jak w funkcji setup()
 
  for(;;) 
    {
      // polecenia wykonywane jak w funkcji loop()
      //wysyłanie kiedy buffor jest pelen
      if(czyWyswietlone==false) 
      {
        wyswietlBuffor(ostatniaWyswietlonaSeria*ilePomDoBuff);
        ostatniaWyswietlonaSeria++;

        if(ostatniaWyswietlonaSeria==maxBufforu/ilePomDoBuff)
          ostatniaWyswietlonaSeria=0;
      }
      //delayMicroseconds(czasDelay);
      //vTaskDelay(czasDelay/1000);
      else delayMicroseconds(1);
    }
}
