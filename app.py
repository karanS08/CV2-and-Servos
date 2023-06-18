import cv2
import mediapipe as mp
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# Initialize the MoveNet head pose model
mp_pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

last_command_time = time.time()

def callibrate(x,y):
    ser.write(b'180 \n 180\n')
    time.sleep(1)
    ser.write(b'0 \n 0\n')
    time.sleep(1)
    ser.write(f"{x} \n {y}\n".encode())
    print("Calibrated")
    

def capture_movement(x,y):
    global last_command_time, last_pan_position, last_tilt_position
    

    # Get mouse coordinate
    mouse_x = x
    mouse_y = y

    # Calculate servo positions
    pan_position = int((mouse_x / form_width) * 270)
    tilt_position = int((mouse_y / form_height) * 270)

    # Convert pan_position and tilt_position to 0-180
    pan_position = int(pan_position * 0.5)
    tilt_position = int(tilt_position * 0.5)

    # Check if the movement is within the threshold
    if (
        abs(pan_position - last_pan_position) >= PAN_THRESHOLD or
        abs(tilt_position - last_tilt_position) >= TILT_THRESHOLD
    ):
        # Create an array of values
        servo_values = [pan_position, tilt_position]

        # Convert the array to a string representation
        servo_values_str = " ".join(str(val) for val in servo_values)

        # Send servo commands via serial
        current_time = time.time()
        elapsed_time = current_time - last_command_time

        if elapsed_time >= 0.1:
            ser.write(f"{servo_values_str}\n".encode())
            print(f"Servo Values: {servo_values_str}")

            # Update the last command time
            last_command_time = current_time

    # Update last positions
    last_pan_position = pan_position
    last_tilt_position = tilt_position




# Create a video capture object
cap = cv2.VideoCapture(0)

form_width = 800
form_height = 600
last_pan_position = 0
last_tilt_position = 0
PAN_THRESHOLD = 1
TILT_THRESHOLD = 1

program_start_time = time.time()

while True:
    # Capture a frame from the video
    ret, frame = cap.read()
    form_width = frame.shape[1]
    form_height = frame.shape[0]

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:


        # Perform pose estimation on the frame
        results = mp_pose.process(rgb_frame)

        # Extract the head pose landmarks
        head_pose = results.pose_landmarks.landmark

    except:
        # try again
        continue


    # Draw the head pose landmarks on the frame
    # draw a circle around the head
    x,y = (int(head_pose[0].x * frame.shape[1]), int(head_pose[0].y * frame.shape[0]))
    # invert x 
    in_x = frame.shape[1] - x



    # callibrate before moving
    if time.time() - program_start_time < 2:
        callibrate(in_x,y)
        continue

    capture_movement(in_x,y)
    cv2.circle(frame, (x,y), 10, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Frame', frame)


    # Check if the user wants to quit
    key = cv2.waitKey(1)
    if key == 27:
        break


# Release the video capture object
cap.release()

# Close all windows
cv2.destroyAllWindows()
