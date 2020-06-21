import json
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        filename, _ = os.path.splitext(input_file)
        with open(input_file) as f: 
            data = json.loads(f.read())
            text = " ".join([x["transcript"] for x in data["results"]["transcripts"]])

            with open(f"{filename}.txt", "w") as f2:
                f2.write(text)
        sys.exit(0)
    else:
        print(f"python {__file__} f1.txt")
        sys.exit(1) 
        