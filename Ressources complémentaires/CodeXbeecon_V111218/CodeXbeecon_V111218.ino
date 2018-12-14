
unsigned char PANID=1;
int incomingByte;


void setup()
{
    Serial1.begin(9600);
}

void loop()
{
    delay(1000);
    Serial1.print("+++");
    delay(1000);

    //Read the incoming byte
    incomingByte = Serial1.read();
    // Serial.println("ici");
    if(incomingByte == '\r') {
         switch(PANID) {
            case(1):// Placement des balises dans le PANID C133
                // Serial.println("PANID1");
                delay(1000);
                Serial1.write("ATIDC133\r");
                delay(1000);
                Serial1.write("ATWR\r");
                delay(1000);
                Serial1.write("ATCN\r");
                PANID=2;
                break;
            case(2):// Placement des balises dans le PANID C233
                //Serial.println("PANID2");
                delay(1000);
                Serial1.write("ATIDC233\r");
                delay(1000);
                Serial1.write("ATWR\r");
                delay(1000);
                Serial1.write("ATCN\r");
                PANID=3;
                break;
            case(3):// Placement des balises dans le PANID C333
                //Serial.println("PANID3");
                delay(1000);
                Serial1.write("ATIDC333\r");
                delay(1000);
                Serial1.write("ATWR\r");
                delay(1000);
                Serial1.write("ATCN\r");
                PANID=1;
                break;
            default:
                break;
        }
    }

}
