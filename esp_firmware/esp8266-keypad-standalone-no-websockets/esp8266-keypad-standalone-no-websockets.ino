// this sketch works as a plain keypad lock
// no websockets or api fetching

#include <String.h>
#include <Vector.h>



//variables for lock status and pins
bool is_locked = false;
int forwards = 4;
int backwards = 5;
int motor_run_time = 3000;

//keypad variables
//store all lockcodes for unit
String storage_array[10];
Vector<String> lock_codes(storage_array);

//master lock code
char* master_code = "2222";
//keypad wire pins
int LockBtn = 16;
int UnlockBtn = 3;
int btnA = 15;
int btnB = 13;
int btnC = 12;
int btnD = 14;
int btnE = 2;

//when key is pressed add this to array
int max_passcode_length = 4;
String keypad_entries = "";
// keep track of the time of the last entry
int  last_time;
int clear_key_entry_wait = 10000;

//manually locks deadbolt when pressed if deadbolt is unlocked
//will reset user inputted keypad entries if deadbolt is already locked
void lock_deadbolt(){
    if(is_locked == false){
      Serial.println("locking");
      digitalWrite(forwards, HIGH);
      delay(motor_run_time);
      digitalWrite(forwards, LOW);
      is_locked = true;
    }
    return;
}

//unlocks deadbolt 
void unlock_deadbolt(){
  if(is_locked == true){
    Serial.println("unlocking");
    digitalWrite(backwards, HIGH);
    delay(motor_run_time);
    digitalWrite(backwards, LOW);
    is_locked = false;
    keypad_entries = "";
  }
  return;
}

//handle passcode entries
void handle_keypad_entries(int btn){
    Serial.println(keypad_entries);
    //if user inputted keypad entries have exceeded maximum length, reset.
    if(keypad_entries.length() >= max_passcode_length){
        keypad_entries = "";
    }

    if(btn == btnA){
        keypad_entries.concat('1');
    }
    if(btn == btnB){
        keypad_entries.concat('2');
    }
    else if(btn == btnC){
        keypad_entries.concat('3');
    }
    else if(btn == btnD){
        keypad_entries.concat('4');
    }
     else if(btn == btnE){
        keypad_entries.concat('5');
    }

    if(keypad_entries.length() > 0){
        check_lock_code();
      } 
     delay(500);
    return;
}


//check to see if correct keypad code has been entered
void check_lock_code(){
Serial.println("checking lock codes");

  bool equals = false;
  
  if(keypad_entries == master_code){
      unlock_deadbolt();
      return;
    }
    
  for(int x; x <= std::size(lock_codes); x++){
    Serial.println("looping through keypad_entries");
    if(lock_codes[x] == keypad_entries){
      unlock_deadbolt();
      break;
    }
  }
    return;
}


void setup() {
    Serial.begin(115200);

  //set pins for deadbolt motor
  pinMode(forwards, OUTPUT);
  pinMode(backwards, OUTPUT);

  //set pins for keypad
  //pinMode(LockBtn, INPUT_PULLUP); 
  pinMode(LockBtn, INPUT);
  pinMode(UnlockBtn, INPUT);
  pinMode(btnA, INPUT); 
  pinMode(btnB, INPUT); 
  pinMode(btnC, INPUT); 
  pinMode(btnD, INPUT); 
  pinMode(btnE, INPUT);

  }

void loop() {

    //After clear_key_entry_wait has been met, reset keypad entries
   if(last_time == clear_key_entry_wait && keypad_entries.length() > 0){
    keypad_entries = "";
   }
  // increase last_time variable every loop, after this has increased so many times, keypad_entries will be reset
   last_time += 1;

   // manually lock deadbolt when pressed
   if(digitalRead(LockBtn) == HIGH){
    lock_deadbolt();
   }

   if(digitalRead(UnlockBtn) == HIGH){
    unlock_deadbolt();
   }

  //handle btn states if pressed
   if(digitalRead(btnA) == HIGH){
    handle_keypad_entries(btnC);
   }

   if(digitalRead(btnB) == HIGH){
    handle_keypad_entries(btnB);
   }
  
   if(digitalRead(btnC) == HIGH){
    handle_keypad_entries(btnC);
   }

   
   if(digitalRead(btnD) == HIGH){
    handle_keypad_entries(btnD);
   }
   
   if(digitalRead(btnE) == HIGH){
    handle_keypad_entries(btnE);
   }
   
  delay(100);
}
