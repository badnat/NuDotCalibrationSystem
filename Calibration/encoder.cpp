#include <iostream>
#include <pigpio.h>
#include <bits/stdc++.h>
#include <fstream>
using namespace std; 

class Encoder {
    private:
    int A;
    int B;
    char* name;
    double angle = 0.0;

    int wasA = 0;
    int isA = 0;
    int count = 0;
    int isB = 0;

    int d = 0;      // counts how many times listener doesn't get an edge

    public:
    Encoder(int A, int B, char* name) {
        gpioInitialise();

        this->A = A;
        this->B = B;
        this->name = name;

        ifstream fin(name);
        fin >> this->angle;

        gpioSetMode(A, PI_INPUT);
        gpioSetMode(B, PI_INPUT);
        gpioWrite(A, 0);
        gpioWrite(B, 0);

        wasA = gpioRead(A);
    }

    public:
    void listen() {
        int dir;
        while (d < 100000 || count < 3) {
            isB = gpioRead(B);
            isA = gpioRead(A);
            if(!wasA && isA) {
                d = 0;
                count++;
                if (count == 2) {
                    dir = isB;
                }
            } else {
                d++;
            }
            wasA = isA;
        }
        if (dir) {
            angle = angle - (round((count) / 5.0) * 1.8);
        } else {
            angle = angle + (round((count) / 5.0) * 1.8);
        }
        ofstream file;
        file.open(name);
        file << angle;
        file.close();
        cout << "ENCODER : " << name << " current angle = " << angle << " with " << round((count) / 5.0) << " steps" << endl;
    }
};

int myAtoi(char* str) {
    int result = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        result = result * 10 + str[i] - '0';
    }
    return result;
}

int main(int argv, char** argc) {
    int A;
    int B;
    char* name;

    A = myAtoi(argc[1]);
    B = myAtoi(argc[2]);
    name = argc[3];

    Encoder *ptr = new Encoder(A, B, name);
    Encoder e = *ptr;
    e.listen();
    gpioWrite(A, 0);
    gpioWrite(B, 0);
    return 0;
}