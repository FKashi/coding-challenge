#!/usr/bin/env python
import json
import os

def main():
    cleaned = 0
    controls = str.maketrans({key: '' for key in [chr(char) for char in range(0, 31)]})  # Removing 0x0000-0x0015
    escapes = str.maketrans({"\n": " ", "\t": " "})  # Translation table for escape characters
    infilename = os.path.join("tweet_input", "tweets.txt")
    outfilename = os.path.join("tweet_output", "ft1.txt")
    with open(outfilename, mode='w') as outfile:
        with open(infilename, mode='r') as infile:
            for line in infile:
                data = json.loads(line)
                text = data.get("text")
                if text is not None:
                    text_unicode = text.encode('ascii','ignore').decode('UTF-8')
                    text_control = text_unicode.translate(controls)
                    text_escape = text_control.translate(escapes)
                    if len(text) != len(text_escape):
                        cleaned += 1
                    text_ws = ' '.join(text_escape.split())
                    output = text_ws + " (timestamp: " + data.get("created_at") + ")\n"
                    outfile.write(output)
                    infile.closed
        outfile.write("\n" + str(cleaned) + " tweets contained unicode.\n")
    outfile.closed

if __name__ == "__main__":
    main()
