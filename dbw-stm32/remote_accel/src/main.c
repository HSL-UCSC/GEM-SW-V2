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

    UART_HandleTypeDef huart2 = getUARTHandle();
    uint8_t duty_cycle;

    while (1)
    {
        HAL_UART_Receive(&huart2, (uint8_t *)&duty_cycle, 1, HAL_MAX_DELAY);
        PWM_SetDutyCycle(PWM_0, (unsigned int)(duty_cycle * 100 / 0xff));

        printf("Duty cycle: 0x%x -> %u%%\n", duty_cycle, (unsigned int)(duty_cycle * 100 / 0xff));
    }
    return 0;
}
