/*
 * Author @Daniel Marzari 9/7/2019 CIS 331
 * 
 * Morse Code Transmitter
 * 
 *  - takes in text input from the serial monitor
 *  - converts the text into morse code
 *  - transmits the morse code through an LED
 * 
 */

//Use the onboard LED
#define ledPin LED_BUILTIN

//One unit of time is .200 seconds
int transmissionSpeed = 200;

//Each (character's index + 2) is the binary morse code of that character with a 1 in front
//Morse Code from https://ece.uwaterloo.ca/~dwharder/Morse_code/
String morseCode = "TEMNAIOGKDWRUS~ QZYCXBJP L FVH09 8   7 (   /=61    + &2   3 45       :    ,     ) !;        -  '        .  \"    _? @                                                                                                                                $";

//String to hold input from the Serial Monitor
String inputString;

//String to hold the data to print to the Serial Monitor
String serialOutput;

//Initialization before loop()
void setup() {
  
  //Initialize LED
  pinMode(ledPin, OUTPUT);

  //Initialize Serial Monitor
  Serial.begin(9600);
  Serial.println("Enter text to be translated into International Morse Code.");
  
} // setup()

void loop() {
  
  //Start with LED off
  digitalWrite(ledPin, LOW);
  
  //If Serial Monitor is available
  if (Serial.available()){
    
    //Get the Serial Input
    inputString = Serial.readString();
    //Format the string to all upper case
    inputString.toUpperCase();
    
    //since Ch is 2 characters, it has been replaced by ~ in the translation string
    inputString.replace("CH", "~");

    //Itterate over the inputString by character
    for (int i = 0; i < inputString.length() - 1; i ++){

      //If there is a space (the delimiter between words) follow morse code procedure for new words
      if(inputString.charAt(i) == ' '){
        
        //Space between words is 7 units of darkness (will sum to 7 at next letter)
        blink(false, transmissionSpeed * 4);
        
      }else{

        //Get the binary Morse Code for each character were 1 is a . and 0 is a - 
        serialOutput = String(morseCode.indexOf(inputString.charAt(i)) + 2, BIN).substring(1);

        //turn the binary representation into morse code (. and -) 
        serialOutput.replace("0", "-");
        serialOutput.replace("1", ".");
        //print the morse code to the Serial Monitor
        Serial.println(serialOutput);
        
        //Space between words is 3 units of darkness
        blink(false, transmissionSpeed * 3);
        //Send the Morse Code via the LED
        transmit(String(morseCode.indexOf(inputString.charAt(i)) + 2, BIN).substring(1));
        
      }
    }
  }
}

//This function handles the timeing of morse code 1s and 0s (.s and -s)
void transmit(String code){
  
  //Itterate over each . and - (1 is dot, 1 unit of light, and 0 is dash, 3 units of light)
  for (int i = 0; i < code.length(); i ++){
    
    //Send ON, delay depending on dot or dash
    blink(true, transmissionSpeed * (code.charAt(i) == '1' ? 1 : 3));
    //Space between letters is one unit
    blink(false, transmissionSpeed);
    
  }
}

//This function turns the LED on or off for a specified length of time
void blink(boolean ON_OFF, int lenTime){
  
  //turn the LED on or off (based on ON_OFF boolean)
  digitalWrite(ledPin, ON_OFF ? HIGH : LOW);
  //Wait the specfied time (lenTime)
  delay(lenTime);
  
}
