def move_to_point(center_between):
    global prev_error_x, prev_error_y

    # Текущая позиция аппарата (предполагается, что она известна)
    current_x, current_y = 320, 240  # например, центр изображения

    # Вычисление ошибки
    error_x = center_between[0] - current_x
    error_y = center_between[1] - current_y

    # Вычисление производной ошибки
    d_error_x = error_x - prev_error_x
    d_error_y = error_y - prev_error_y

    # ПД-регулятор
    U_x = Kp * error_x + Kd * d_error_x
    U_y = Kp * error_y + Kd * d_error_y

    # Обновление предыдущей ошибки
    prev_error_x = error_x
    prev_error_y = error_y

    # Управление моторами
    # Используем U_x для регулировки скорости моторов
    motor_left = base_speed + U_x
    motor_right = base_speed - U_x

    # Ограничение значений моторов в пределах 0-100%
    motor_left = max(0, min(100, motor_left))
    motor_right = max(0, min(100, motor_right))

    print(f"Moving to point: {center_between}")
    print(f"Left Motor Speed: {motor_left}%, Right Motor Speed: {motor_right}%")

    # Устанавливаем скорость для обоих моторов одновременно
    left_motor_pwm.ChangeDutyCycle(motor_left)
    right_motor_pwm.ChangeDutyCycle(motor_right)
