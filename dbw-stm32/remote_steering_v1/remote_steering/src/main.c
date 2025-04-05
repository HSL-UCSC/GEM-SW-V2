#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <Board.h>
#include "timers.h"
#include "stm32f4xx_hal.h"
#include "stm32f411xe.h"
#include "stm32f4xx_hal_tim.h"

#define INITIAL_PERIOD 1500
#define MIN_PERIOD 1000
#define MAX_PERIOD 2300
#define CYCLE_PERIOD 20 * 1000
#define INCREMENT 10

int period = INITIAL_PERIOD;
int direction = 1;

int lastOutput = 0;
int currentPeriod = INITIAL_PERIOD;

TIM_HandleTypeDef htim3;

#define OUT GPIO_PIN_8

int main()
{

    BOARD_Init();

    // this block initializes the GPIO output pin (PB8, PWM_5 on shield)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = OUT;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    // this block inits the timer generated interrupt
    TIM_ClockConfigTypeDef sClockSourceConfig = {0};
    TIM_MasterConfigTypeDef sMasterConfig = {0};
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 83; // divide by 1 prescaler (84-1) = 1 Mhz tick
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = (CYCLE_PERIOD - currentPeriod); // number of clock cycles between interrupts (20 ms)
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
    if (HAL_TIM_Base_Init(&htim3) != HAL_OK)
    {
        return ERROR;
    }
    sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
    if (HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig) != HAL_OK)
    {
        return ERROR;
    }
    sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
    sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
    if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
    {
        return ERROR;
    }
    HAL_TIM_Base_Start_IT(&htim3); // start interrupt

    uint8_t input;
    UART_HandleTypeDef huart2 = getUARTHandle();

    while (1)
    {
        HAL_UART_Receive(&huart2, (uint8_t *)&input, 1, HAL_MAX_DELAY);
        period = (int)(input * (MAX_PERIOD - MIN_PERIOD) / 0xff + MIN_PERIOD);
        printf("Duty cycle: 0x%02x -> %04d\n", input, period);
    }
    return 0;
}

// TIM3 ISR
void TIM3_IRQHandler(void)
{
    if (__HAL_TIM_GET_IT_SOURCE(&htim3, TIM_IT_UPDATE) != RESET)
    {
        if (!lastOutput)
        {
            currentPeriod = period;
            HAL_GPIO_WritePin(GPIOB, OUT, GPIO_PIN_SET);
            htim3.Instance->ARR = currentPeriod; // 10 us pulse
            lastOutput = 1;
        }
        else
        {
            HAL_GPIO_WritePin(GPIOB, OUT, GPIO_PIN_RESET);
            htim3.Instance->ARR = (CYCLE_PERIOD - currentPeriod); // 60 ms timer
            lastOutput = 0;
        }
        __HAL_TIM_CLEAR_IT(&htim3, TIM_IT_UPDATE); // clear interrupt flag
    }
}
