import subprocess

# Define the camera devices
CAMERA_1 = "/dev/video0"
CAMERA_2 = "/dev/video1"

# Function to preview the camera feed using libcamera-vid
def preview_camera(camera_id):
    print(f"Starting preview for {camera_id}")
    # Launch libcamera-vid for preview with specified window geometry
    try:
        subprocess.run(["libcamera-vid", "--camera", camera_id, "--preview", "0,0,640,480"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except KeyboardInterrupt:
        print(f"Stopping preview for {camera_id}")

if __name__ == "__main__":
    print("Select camera module:")
    print("1. Camera 1")
    print("2. Camera 2")
    choice = input("Please select a camera (1 or 2): ")

    if choice == "1":
        preview_camera(CAMERA_1)
    elif choice == "2":
        preview_camera(CAMERA_2)
    else:
        print("Invalid choice, please rerun the program")
