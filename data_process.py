import cv2
import numpy as np
import math



def append_to_data_matrix(matrix, contours):
    for shape in contours:
        # Get the bounding box coordinates and dimensions
        x, y, w, h = cv2.boundingRect(shape)
        # Calculate image moments and extract the area
        moments = cv2.moments(shape)
        area = moments['m00']
        # Calculate the perimeter (assuming the shape is closed)
        perimeter = cv2.arcLength(shape, True)
        # Avoid division by zero for noise/small dots
        if perimeter > 0 and (w * h) > 0:
            width_high_ratio = abs(w-h)
            # Metric for how circular the object is (1.0 = perfect circle)
            circularity = (4 * math.pi * area) / (perimeter**2)
            # Ratio of object area to its bounding box area (Extent)
            circle_square_ratio = area / (w * h)
            # Assemble the feature vector for this object
            matrix_line = [width_high_ratio, circularity, circle_square_ratio]
            # Append the features to our training/data matrix
            matrix.append(matrix_line)

def real_time_process(con):
        if len(con)<=1:
             return [[0,0,0]]
        # Get the bounding box coordinates and dimensions
        x, y, w, h = cv2.boundingRect(con)
        # Calculate image moments and extract the area
        moments = cv2.moments(con)
        area = moments['m00']
        # Calculate the perimeter (assuming the shape is closed)
        perimeter = cv2.arcLength(con, True)
        # Avoid division by zero for noise/small dots
        if perimeter > 0 and (w * h) > 0:
            width_high_ratio = abs(w-h)
            # Metric for how circular the object is (1.0 = perfect circle)
            circularity = (4 * math.pi * area) / (perimeter**2)
            # Ratio of object area to its bounding box area (Extent)
            circle_square_ratio = area / (w * h)
            # Assemble the feature vector for this object
            matrix_line = [[width_high_ratio, circularity, circle_square_ratio]]
            return matrix_line

if __name__ =='__main__':

    data_matrix = []
    files_number = 315

    for num_file in range(1,files_number+1):
        curr_file = np.load(f'tennis_sample{num_file}.npy')
        print(f'file number: {num_file}')
        #print(curr_file)

        # 7. Spatial Analysis (Finding the Ball)
        contours, _ = cv2.findContours(curr_file, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(f'contours length is: {len(contours)}')
        append_to_data_matrix(data_matrix,contours)

    print(data_matrix)
    #np.save('tennis_ball_fithre1',data_matrix)
    #np.save('other_ball_fithre1',data_matrix)






