/* Daniel Marzari 450
 * Project 4: Musical Instrument 
 *  
 *  Uses Sparkfun ESP8266 Thing
 *  
 *  Wiring 
 *     https://circuits4you.com/2017/12/31/nodemcu-pinout/
 *     pin D4 to Passive Busser, other to GND
 *     
 * Web Server Example from:
 *     https://circuits4you.com/2016/12/16/esp8266-web-server-ap/
 *     https://circuits4you.com/2018/02/02/esp8266-handle-not-found-pages-and-redirect/
 * 
 * HTML:
 *     W3Schools.com
 * 
 * Frequencies:
 *     https://pages.mtu.edu/~suits/notefreqs.html
 */
 
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
 
//SSID and Password for the ESP8266 (Sparkfun ESP8266 Thing) Access Point
const char* ssid = "ESP8266_AccessPoint";
const char* password = "12345678";

ESP8266WebServer server(80); //Server on port 80

int pBuzz = 2; //Output Pin D4 on the Sparkfun ESP8266
double Hz = 0; //variable to hold frequency

//===============================================================
//     This is exicuted when you open 192.168.4.1 in the browser
//===============================================================
void handleRoot() {
  char html[2000]; //char buffer for the page

  //Below is the HTML for the web page that will be displayed
  //Styles change apperance on click, svg shapes make the piano keys,
  //and the a href's redirect the page so we can play the notes
  snprintf (html, 2000,
"<html>\
 <body>\
    <style>\
      .white {fill:white;stroke:black;stroke-width:1;cursor:pointer;margin:2px;}\
      .white:active {fill:#F0F0F0;stroke:lightblue;cursor:pointer;stroke-width:1;outline: black solid 1px;}\
      .black {fill:black;stroke-width:1;cursor:pointer;margin:2px;}\
      .black:active {fill:grey;stroke:lightblue;stroke-width:1;outline: black solid 1px;}\
    </style>\
    <svg class='piano' height='230' width='1000'>\
      <a href='/261.6'><polygon points='200,10 230,10 230,100 245,100 245,220 200,220 200,10' class='white'/></a>\
      <a href='/277.2'><polygon points='230,10 260,10 260,100 230,100 230,10' class='black'/></a>\
      <a href='/293.7'><polygon points='245,100 260,100 260,10 275,10 275,100 290,100 290,220 245,220 245,100' class='white'/></a>\
      <a href='/311.1'><polygon points='275,10 305,10 305,100 275,100 275,10' class='black'/></a>\
      <a href='/329.6'><polygon points='305,10 335,10 335,220 290,220 290,100 305,100 305,10' class='white'/></a>\
      <a href='/349.2'><polygon points='335,10 365,10 365,100 380,100 380,220 335,220 335,10' class='white'/></a>\
      <a href='/370.0'><polygon points='365,10 395,10 395,100 365,100 365,10' class='black'/></a>\
      <a href='/392.0'><polygon points='380,100 395,100 395,10 410,10 410,100 425,100 425,220 380,220 380,100' class='white' /></a>\
      <a href='/415.3'><polygon points='410,10 440,10 440,100 410,100 410,10' class='black'/></a>\
      <a href='/440.0'><polygon points='425,100 440,100 440,10 455,10 455,100 470,100 470,220 425,220 425,100' class='white' /></a>\
      <a href='/466.2'><polygon points='455,10 485,10 485,100 455,100 455,10' class='black'/></a>\
      <a href='/493.9'><polygon points='470,100 485,100 485,10 515,10 515,220 470,220 470,100' class='white' /></a>\
      <a href='/523.3'><polygon points='515,10 545,10 545,100 560,100 560,220 515,220 515,10' class='white' /></a>\
    </svg>\
  </body>\
</html>");
  //send the data to our device
  server.send(200, "text/html", html);  
}

//Get Frequency from the URL and play it through the buzzer
void playHz(){
  //Recieve Data from the URL (192/168.4.1/FREQUENCY)
  String data = server.uri().substring(server.uri().indexOf("/")+1); //Get the Frequency
  //If it's a number and not giberish
  if(data.length() == 5){
    //extract the number
    Hz = data.substring(0, data.indexOf(".")).toInt();
    //Print in Serial
    Serial.print("Playing: ");
    Serial.println(Hz);
    //Play the note for half a second and stop
    tone(pBuzz, Hz, 500);
    delay(500);
    noTone(pBuzz);
  } 
  
  //Redirect back to the main page so that you can play another note
  server.sendHeader("Location", "/",true); 
  server.send(302, "text/plane","");
}

//Initialize the server and pinModes
void setup(void){
  //passiveBuzzer pin is ouput
  pinMode(pBuzz, OUTPUT);
  noTone(pBuzz);
  
  Serial.begin(9600);
  WiFi.mode(WIFI_AP);           //Only Access point
  WiFi.softAP(ssid, password);  //Start HOTspot removing password will disable security
 
  IPAddress myIP = WiFi.softAPIP(); //Get IP address
  Serial.print("HotSpt IP:");
  Serial.println(myIP);
 
  server.on("/", handleRoot);      //Which routine to handle at root location
  server.onNotFound (playHz);
   
  server.begin();//Start server
}

void loop(void){
  server.handleClient();          //Handle client requests
}
