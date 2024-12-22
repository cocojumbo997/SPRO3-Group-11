from rclpy.node import Node
import serial
import RPi.GPIO as GPIO
import time

class ImuNode(Node):
	def __init__(self):
		super().__init__("imu_node")
		self.get_logger().info("IMU node initialized")
		
		
def main(args=None):
	rclpy.init(args=args)
	node = ImuNode()
	rclpy.spin(node)	
	rclpy.shutdown()

if __name__ == "__main__":
	main()

# L298N PINOUT
IN1 = 17  # Motor A direction 1
IN2 = 27  # Motor A direction 2
ENA = 12  # Motor A speed (PWM)

IN3 = 22  # Motor B direction 1
IN4 = 23  # Motor B direction 2
ENB = 13  # Motor B speed (PWM)


# HC-SR04 PINOUT
sensors = {
    "SENSOR_L": {"Trig": 5, "Echo": 6},   # LEFT sensor
    "SENSOR_C": {"Trig": 9, "Echo": 25},  # CENTRAL sensor
    "SENSOR_R": {"Trig": 4, "Echo": 10},  # RIGHT sensor
}

# L298N GPIO CONFIGURATION
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)  # direction pins to output
GPIO.setup([ENA, ENB], GPIO.OUT)  # speed pins to output(PWM)

# HC-SR04 GPIO CONFIGURATION
for sensor in sensors.values():
    GPIO.setup(sensor["Trig"], GPIO.OUT)
    GPIO.setup(sensor["Echo"], GPIO.IN)

# PWM CONFIGURATION
pwmA = GPIO.PWM(ENA, 1000)  # 1k Hz frequency for motor A
pwmB = GPIO.PWM(ENB, 1000)  # 1k Hz frequency for motor B

# SET POWER OF PWM | % of duty cycle
pwmA.start(100)
pwmB.start(100)

# FUNCTION for measuring distance
def measure_distance(trig, echo):
    # Send 10µs pulse to TRIG
    GPIO.output(trig, True)
    time.sleep(0.00001)  # 10 µs
    GPIO.output(trig, False)

    # Initialize times
    pulse_start, pulse_end = None, None

    # Wait for the start of return pulse
    timeout_start = time.time()
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 0.02:  # 20ms wait
            return None

    # Wait for the end of return pulse
    timeout_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
        if pulse_end - timeout_start > 0.02:  # 20ms wait
            return None

    # Calculate distance
    if pulse_start and pulse_end:
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 34300) / 2  # Get distance in cm (speed of sound)
        return distance
    else:
        return None

# FUNCTIONS to control the motors
def motorA_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def motorA_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def motorB_forward():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def motorB_backward():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop_motors():
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

# Main loop
try:
	# Start motors
    motorA_forward()
    motorB_forward()  
    
    while True:
        obstacle_detected = False

        for name, pins in sensors.items():
            distance = measure_distance(pins["Trig"], pins["Echo"])
			
			# If obstacle is detected
            if distance is not None and distance < 15:
                obstacle_detected = True
                print(f"{name}: Object detected at {distance:.2f} cm")

                if name == "SENSOR_L":  # Obstacle detected in LEFT SENSOR
                    print("Turning RIGHT...")
                    stop_motors()
                    time.sleep(1.0)
                    motorA_forward()
                    motorB_backward()


                if name == "SENSOR_C":  # Obstacle detected in CENTRAL SENSOR
                    
                    # Compare distances measured at SENSOR_L y SENSOR_R
                    left_distance = measure_distance(sensors["SENSOR_L"]["Trig"], sensors["SENSOR_L"]["Echo"])
                    right_distance = measure_distance(sensors["SENSOR_R"]["Trig"], sensors["SENSOR_R"]["Echo"])
                    
					# Check for valid measurements
                    if left_distance is not None and right_distance is not None:
                        if left_distance > right_distance:
                            print("More space on left, turning lEFT...")
                            stop_motors()
                            time.sleep(1)
                            motorB_forward()
                            motorA_backward()
                            
                        else:
                            print("More space on right, turning RIGHT...")
                            stop_motors()
                            time.sleep(1)
                            motorA_forward()
                            motorB_backward()


                elif name == "SENSOR_R":  # Obstacle detected in RIGHT SENSOR
                    print("Turning LEFT...")
                    stop_motors()
                    time.sleep(1)
                    motorB_forward()
                    motorA_backward()

        # When no obstacle detected, go forward
        if not obstacle_detected:
            print("Clear rout, going FORWARD...")
            motorA_forward()
            motorB_forward()

        time.sleep(0.2)  # pause betwwen cycles

except KeyboardInterrupt:
    print("Program stopped by admin")
    stop_motors()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()

