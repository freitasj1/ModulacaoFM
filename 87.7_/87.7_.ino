int local = 0;

float freq = 87.7;
//pinagem dos botoes
int botoes[5] = {2, 3, 4, 5, 6}, botao_emergencia = 7;
//pinagem da configuracao da frequencia
int setfreq_pin[4] = {12, 11, 10, 9};
//relacao da frequencia e a pinagem
float setfreq_data[14][5] = {
  //frequencia de emergencia
  {87.7, 0, 0, 0, 0},
  //frequencias "baixas"
  {87.9, 1, 0, 0, 0},
  {88.1, 0, 1, 0, 0},
  {88.3, 1, 1, 0, 0},
  {88.5, 0, 0, 1, 0},
  {88.7, 1, 0, 1, 0},
  {88.9, 0, 1, 1, 0},
  //frequencias "altas"
  {106.7, 0, 0, 0, 1},
  {106.9, 1, 0, 0, 1},
  {107.1, 0, 1, 0, 1},
  {107.3, 1, 1, 0, 1},
  {107.5, 0, 0, 1, 1},
  {107.7, 1, 0, 1, 1},
  {107.9, 0, 1, 1, 1}
};

float freq_emerge = 87.7;

//prototipagem
void setfreq(float);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  //botoes pra simular area
  for (int i = 0; i < 5; i++) {
    pinMode(botoes[i], INPUT_PULLUP);
  }
  pinMode(botao_emergencia, INPUT_PULLUP); //botao de emergencia

  //pinMode(8, OUTPUT); //led de emergencia
  //pinMode(9, OUTPUT); //led de mudanca de estadoh

  for (int i = 0; i < 4; i++) {
    pinMode(setfreq_pin[i], OUTPUT);
  }
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);

}

void loop() {
  if (digitalRead(botoes[0]) == 0) {
    local = 1;
    digitalWrite(A1, 1);
  } else if (digitalRead(botoes[1]) == 0) {
    local = 2;
    digitalWrite(A1, 1);
  } else if (digitalRead(botoes[2]) == 0) {
    local = 3;
    digitalWrite(A1, 1);
  } else if (digitalRead(botoes[3]) == 0) {
    local = 4;
    digitalWrite(A1, 1);
  } else if (digitalRead(botoes[4]) == 0) {
    local = 5;
    digitalWrite(A1, 1);
  } else if (digitalRead(botao_emergencia) == 0) {
    setfreq(freq_emerge);
    digitalWrite(A1, 1);
  }


  if (local != 0) {
    Serial.print("area-");
    Serial.print(local);
    Serial.println(";");
    digitalWrite(A2, 0);
  }
  else {
    digitalWrite(A2, 1);
    if (digitalRead(botao_emergencia) == 0) {
      freq = freq_emerge;
    }
  }
  while (Serial.available() > 0) {
    // Lê a string recebida
    String receivedMessage = Serial.readStringUntil('\n');
    freq = receivedMessage.toFloat();
  }

  delay(1000);
  digitalWrite(A1, 0);
  
  setfreq(freq);
}

//configura a frequencia do modulo
void setfreq(float freq) {

  //Serial.println("confg frequencia");
  //para cada frequencia comfiguravél
  for (int i = 0; i < 14; i++) {
    //verifica se a ferequencia passada esta entre as configuraveis
    if (freq == setfreq_data[i][0]) {
      //se sim, configura o estado dos pinos para essa frequencia
      for (int j = 0; j < 4; j++) {
        digitalWrite(setfreq_pin[j], (bool) setfreq_data[i][j + 1]);
      }
      break;//e sai do loop
    }
  }
}
