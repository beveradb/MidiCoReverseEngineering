#!/usr/bin/env python3
import sys
import os


def decode_timestamp(bytes_data):
    binary_str = "".join(f"{b:08b}" for b in bytes_data)
    print(f"Decoding timestamp bits: {binary_str}")
    value = int.from_bytes(bytes_data, byteorder="big")
    whole_seconds = (value >> 11) - 16  # Subtract 16 to account for the offset
    fraction = (value & 0x7FF) / 2048  # Use 11 bits for fraction
    result = whole_seconds + fraction
    print(f"Whole seconds: {whole_seconds} ({binary_str[1:6]})")
    print(f"Fraction: {fraction:.6f} ({binary_str[6:]})")
    print(f"Decoded timestamp: {result:.6f} seconds")
    return result


def read_midico_file(file_path):
    print(f"Processing file: {file_path}")
    marker_start = b"\x4C\x31"  # L1 marker
    marker_end = b"\x4C\x32"  # L2 marker

    output_file = os.path.basename(os.path.splitext(file_path)[0]) + "-extract.txt"
    print(f"Output will be written to: {output_file}")

    try:
        with open(file_path, "rb") as file:
            data = file.read()
            print(f"File size: {len(data)} bytes")
            start_index = data.find(marker_start)
            end_index = data.find(marker_end)
            if start_index == -1 or end_index == -1:
                print("Markers not found in the file.")
                return
            print(f"Start marker found at index: {start_index}")
            print(f"End marker found at index: {end_index}")
            start_index += len(marker_start)
            content_between_markers = data[start_index:end_index]
            print(f"Content between markers: {len(content_between_markers)} bytes")
            print(f"Content: {''.join(f'{b:08b}' for b in content_between_markers)}")

        timestamps = []
        i = 0
        while i < len(content_between_markers):
            print(f"\nProcessing byte at index {i}")
            if i + 11 > len(content_between_markers):
                print("Not enough bytes left to process a complete entry")
                break

            # Skip the first 4 bytes (header)
            header = content_between_markers[i : i + 4]
            print(f"Header: {''.join(f'{b:08b}' for b in header)}")
            i += 4

            # Extract timestamp bytes
            timestamp_bytes = content_between_markers[i : i + 2]
            i += 2
            print(f"Timestamp bytes: {''.join(f'{b:08b}' for b in timestamp_bytes)}")

            timestamp = decode_timestamp(timestamp_bytes)

            # Skip the remaining 5 bytes
            remaining = content_between_markers[i : i + 5]
            print(f"Remaining bytes: {''.join(f'{b:08b}' for b in remaining)}")
            i += 5

            timestamps.append(timestamp)

        print(f"\nTotal timestamps extracted: {len(timestamps)}")

        with open(output_file, "w") as out_file:
            out_file.write("Start Timestamp (seconds)\n")
            for timestamp in timestamps:
                out_file.write(f"{timestamp:.6f}\n")
                print(f"Written: {timestamp:.6f}")

        print(f"Output written to: {output_file}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_midico_file>")
    else:
        read_midico_file(sys.argv[1])
