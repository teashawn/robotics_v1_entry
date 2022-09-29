#!/usr/bin/env python3

import argparse
import utils.file_parser as fp

from solution import compute_solution

def main():  # pylint: disable=missing-function-docstring
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", default="input.bin", type=str)
    parser.add_argument("-o", "--output", help="Output file", default="output.bin", type=str)
    args = parser.parse_args()

    image_type: fp.ImageType = fp.ImageType.StrideImageType
    input_file_name = args.input
    output_file_name = args.output
    
    #NOTE: data loading could take at least several seconds with big test files
    input_images, output_images = fp.generate_io_data(input_file_name, output_file_name, image_type)
    
    compute_solution(input_images)
    
    if input_images == output_images:
        print("Solution status - [SUCCESS]\n")
    else:
        print("Solution status - [FAIL]\n")
 
if __name__ == "__main__":
    main()