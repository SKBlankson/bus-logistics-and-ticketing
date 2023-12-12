import cv2
import time
import threading

class ParkingSystem:
    def __init__(self, total_capacity, image_path):
        self.total_capacity = total_capacity
        self.filled_slots = 0
        self.image = cv2.imread(image_path)  # Read the input image

    def capture_filled_slots(self, parking_lot_image):
        # Convert the image to grayscale for easier processing
        gray_image = cv2.cvtColor(parking_lot_image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to create a binary image (assuming slots are distinct)
        _, binary_image = cv2.threshold(gray_image, 100, 2550, cv2.THRESH_BINARY_INV)

        # Find contours in the binary image
        contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out small contours (if needed) based on area
        min_contour_area = 200  # Adjust as per your requirement
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

        # Count the number of valid contours (filled slots)
        filled_slots_count = len(valid_contours)

        return filled_slots_count #24
    

    def calculate_available_spaces(self):
        return self.total_capacity - self.filled_slots

    def update_space_count(self):
        # This function is not used in this modified version since the image is static
        pass

    '''def display_occupancy_rate(self):
        available_spaces = self.calculate_available_spaces()
        occupancy_rate = (available_spaces / self.total_capacity) * 100
        print(f"Current occupancy rate: {occupancy_rate:.2f}%")'''

    def display_parking_details(self):
        print(f"Parking Capacity: {self.total_capacity}")
        print(f"Parking Available: {self.calculate_available_spaces()}")

# Usage example with an image path
image_path = "/Users/ann-vanessa/Downloads/istockphoto-856857870-612x612.jpg"  # Replace with your image path
parking_lot = ParkingSystem(total_capacity=70, image_path=image_path)

# Simulate counting filled slots using image processing
parking_lot.filled_slots = parking_lot.capture_filled_slots(parking_lot.image)

# Display parking details and occupancy rate
parking_lot.display_parking_details()
'''parking_lot.display_occupancy_rate()'''
