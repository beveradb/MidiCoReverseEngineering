#!/usr/bin/env python3
import sys
import os


def read_midico_file(file_path):
    marker_start = b"\x4C\x31"  # L1 marker
    marker_end = b"\x4C\x32"  # L2 marker

    # Create output file name
    output_file = os.path.splitext(file_path)[0] + "-extract.txt"

    try:
        with open(file_path, "rb") as file:
            data = file.read()
            start_index = data.find(marker_start)
            end_index = data.find(marker_end)
            if start_index == -1 or end_index == -1:
                print("Markers not found in the file.")
                return
            # Skip the start marker itself
            start_index += len(marker_start)
            content_between_markers = data[start_index:end_index]

        # Write output to file
        with open(output_file, "w") as out_file:
            out_file.write("Hex, Decimal, Binary, and ASCII Representation:\n")
            for i, byte in enumerate(content_between_markers):
                hex_representation = f"{byte:02x}"
                decimal_representation = f"{byte:3d}"
                binary_representation = f"{byte:08b}"
                ascii_representation = chr(byte) if 32 <= byte < 127 else "."
                line = f"{hex_representation} {decimal_representation} {binary_representation} {ascii_representation}\n"
                out_file.write(line)

        print(f"Output written to: {output_file}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_midico_file>")
    else:
        read_midico_file(sys.argv[1])
