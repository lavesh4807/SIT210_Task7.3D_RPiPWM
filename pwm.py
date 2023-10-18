import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BCM)

TRIGGER_PIN = 15
ECHO_PIN = 13
BUZZER_PIN =4

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer_pwm = GPIO.PWM(BUZZER_PIN, 1000)  # Frequency = 1000 Hz
buzzer_pwm.start(0)  # Start with a 0% duty cycle

def measure_distance():
    # Trigger the HC-SR04 ultrasonic sensor
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    while GPIO.input(ECHO_PIN) == False:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == True:
        finish_time = time.time()

    # Calculate the distance based on the time difference and the speed of sound
    total_time = finish_time - start_time
    distance = (total_time * 34300) / 2  # Speed of sound is approximately 34300 cm/s
    return distance

try:
    while True:
        # Get the distance measurement from the ultrasonic sensor
        distance = measure_distance()
        print(distance)  # Print the distance to the terminal for debugging
        
        # Limit the maximum distance reading to 30 cm
        if distance > 30:
            distance = 30
            
        if distance < 0:
            distance = 0

        # Convert the distance to a ratio between 0 and 100
        distance_ratio = (distance / 30) * 100
        
        # Adjust the PWM duty cycle for the buzzer based on the distance ratio
        buzzer_pwm.ChangeDutyCycle(distance_ratio)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up the GPIO settings when the program is interrupted by the user
    GPIO.cleanup()
