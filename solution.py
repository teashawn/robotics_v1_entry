#!/usr/bin/env python3
from multiprocessing import (
    Pool,
    Manager,
    Queue,
    cpu_count
)
import numpy as np
import string
from utils.function_tracer import FunctionTracer
from typing import (
    List,
    Tuple,
)
from utils.image import (
    StrideImage,
)
from utils.resolution import (
    Resolution,
)
from utils.eye_pattern import (
    EyePattern,
    EYE_PATTERN_1,
    EYE_PATTERN_2,
    EYE_PATTERN_3,
    EYE_PATTERN_4,
)

RED_EYE_REDUCTION_VALUE = 150
RED_EYE_THRESHOLD_VALUE = 200
EYE_PATTERN_RESOLUTION = Resolution(5,5)
EYE_PATTERN_SHAPE = (5,5)

def extract_pattern_matrices(patterns: List[EyePattern]) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """Converts the originally supplied eye patterns to forms suitable for efficient comparison
    and application to source images"""
    pattern_matrices: List[np.ndarray] = []
    pattern_filters: List[np.ndarray] = []

    for pattern in patterns:
        matrix = np.zeros(EYE_PATTERN_SHAPE, dtype=int)
        for line_index, line in enumerate(pattern):
            for character_index, character in enumerate(line):
                matrix[line_index, character_index] = 0 if character in string.whitespace else 1
        pattern_matrices.append(matrix)
        pattern_filters.append(matrix * RED_EYE_REDUCTION_VALUE)
    
    return pattern_matrices, pattern_filters

# The order in which patterns are tested is important! I had written all of the code
# and checked all logic, but I kept getting 2 pixels in each image that were not
# filtered. It took me as much time as writing all of the code to figure this out :)
EYE_PATTERN_MATRICES, EYE_PATTERN_FILTERS = extract_pattern_matrices([
    EYE_PATTERN_4,
    EYE_PATTERN_3,
    EYE_PATTERN_2,
    EYE_PATTERN_1,
])

def apply_red_eye_filter(image: StrideImage) -> None:
    # Sanity check
    if image.resolution.width < EYE_PATTERN_RESOLUTION.width \
        or image.resolution.height < EYE_PATTERN_RESOLUTION.height:
        return
    
    # We look at the red channel of the pixels only, per the task definition
    image_array = np.array(image.pixels_red).reshape(image.resolution.height, image.resolution.width)

    # Ensure we stay within the image boundaries when traversing
    vertical_stop = (image.resolution.height - EYE_PATTERN_RESOLUTION.height) + 1
    horizontal_stop = (image.resolution.width - EYE_PATTERN_RESOLUTION.width) + 1

    # Traverse the image with a sliding window, the size of the eye patterns
    for row in range(0, vertical_stop):
        for column in range(0, horizontal_stop):
            # Calculate the row and column indices that will define
            # our sliding window. We take an initial coordinate and
            # extend it in both directions to the size of the eye
            # patterns
            row_indices = range(row, row+EYE_PATTERN_RESOLUTION.height)
            column_indices = range(column, column+EYE_PATTERN_RESOLUTION.width)

            # Get the pixels we need for the window
            window = image_array[np.ix_(row_indices, column_indices)]
            # Create a mask of the raw values for more efficient matching
            mask = window // RED_EYE_THRESHOLD_VALUE
            
            # Check if any of the eye patterns matches the current window
            for index, pattern in enumerate(EYE_PATTERN_MATRICES):
                if np.array_equal(mask & pattern, pattern):
                        # If we have a match, we apply the filter
                        window -= EYE_PATTERN_FILTERS[index]
                        # And store the modified pixels
                        image_array[row:row+EYE_PATTERN_RESOLUTION.width, column:column+EYE_PATTERN_RESOLUTION.height] = window
                        break

    # Finally, we put the modified pixels back in the original image
    image.pixels_red = list(image_array.ravel())

def parallel_apply_red_eye_filter(image: StrideImage, q: Queue, idx: int) -> None:
    apply_red_eye_filter(image)
    q.put((idx, image))

def compute_solution(images: List[StrideImage]) -> None:
    ft = FunctionTracer("compute_solution", "seconds")

    with Pool(processes=cpu_count()) as pool:
        m = Manager()
        q =  m.Queue(maxsize=len(images))
        args = [(i, q, idx) for idx, i in enumerate(images)]
        pool.starmap(parallel_apply_red_eye_filter, args)

        for _ in range(0, len(images)):
            idx, img = q.get()
            # Since the image was mutated in another process,
            # our original copy needs to be updated before
            # the final evalutaion against the expected results
            images[idx] = img

    del ft
