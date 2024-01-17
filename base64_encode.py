import base64

def encode_file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file_filetype:
            encoded_file = base64.b64encode(file_filetype.read())
            return encoded_file.decode("utf-8")
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error encoding file: {e}")
        return None

file_path = "C:/Users/LokeshAnna/Desktop/posttest.txt"
encoded_file = encode_file_to_base64(file_path)

if encoded_file is not None:
    print(f"Encoded file code is:\n{encoded_file}")
else:
    print("Conversion failed.")
