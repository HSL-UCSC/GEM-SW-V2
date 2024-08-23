#include <stdio.h>
#include <stdlib.h>
#include <Board.h>
#include <pwm.h>

int main()
{
    BOARD_Init();
    PWM_Init();

    PWM_AddPin(PWM_0);
    PWM_SetFrequency(1000);

    double voltage = 0.5;
    double minVoltage = 0.5;
    double maxVoltage = 3.2;
    double systemVoltage = 3.3;
    double increment = 0.05;
    int direction = 1;

    while (1)
    {
        PWM_SetDutyCycle(PWM_0, (unsigned int)(voltage * 100 / systemVoltage));
        voltage += direction * increment;

        if (voltage >= maxVoltage)
        {
            direction = -1;
        }
        else if (voltage <= minVoltage)
        {
            direction = 1;
        }
        printf("V: %f D: %d \n", voltage, (unsigned int)(voltage * 100 / systemVoltage));

        HAL_Delay(100);
    }
    return 0;
}