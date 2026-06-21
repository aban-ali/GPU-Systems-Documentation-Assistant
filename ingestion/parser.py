import fitz
import re
import pymupdf4llm
from os import path
# from os import listdir
import json

RAW_OUTPUT_FILEPATH = path.join("data", "processed", "raw_data.jsonl")
PATTERN_END = re.compile(r"#+\s(\*\*)?[\d\.\s]+Notice(\*\*)?")
PATTERN_INVALID_LINE1 = re.compile(r"\(([a-zA-Z]+\s){3}[a-zA-Z]+\)")
PATTERN_INVALID_LINE2 = re.compile(r"\*\*^[a-zA-Z].*\*\*")
PATTERN_IMAGE = re.compile(r"(\*\*)?==>.*<==(\*\*)?")
PATTERN_TABLE_JUNK = re.compile(r"-?<br>")
PATTERN_ALPHA = re.compile(r"_?\\\\u03b1_?") # alpha character
PATTERN_BETA = re.compile(r"_?\\\\u03b2_?") # beta character
PATTERN_FORWARD_SLASH = re.compile(r"_?(\\\\u2215)+_?") # forward slash character

# # This is supposed to be used later
# files = listdir(path("data", "pdf_data"))

files = [
    "CUBLAS_Library.pdf",
    "CUDA_C_Best_Practices_Guide.pdf",
    "CUDA_C_Programming_Guide.pdf",
    "CUDA_Runtime_API.pdf",
    "ptx_isa_9.3.pdf"
]

def is_invalid_line(line):
    return PATTERN_INVALID_LINE1.fullmatch(line) or \
                PATTERN_INVALID_LINE2.fullmatch(line)

def is_new_chapter(line):
    return re.fullmatch(r"#+\s(\*\*)?Chapter\s.+(\*\*)?", line)

def clean_line(line):
    line = PATTERN_IMAGE.sub("==>[ IMAGE ]<==", line)
    line = PATTERN_TABLE_JUNK.sub("", line)
    line = PATTERN_ALPHA.sub("α", line)
    line = PATTERN_BETA.sub("β", line)
    line = PATTERN_FORWARD_SLASH.sub("/", line)
    return line.strip()

def smarter_parse():
    with open(RAW_OUTPUT_FILEPATH, "w") as f:
        for file in files:
            filepath = path.join("data", "pdf_data", file)
            doc = pymupdf4llm.to_markdown(filepath, header=False, footer=False).split("\n\n")
            data = {
                "doc": file[:-4], "chapter": "",  "text": ""
                }
            text = ""
            pre = True

            for line in doc:
                line = line.strip()
                if pre and not re.match(r"## (\*\*)?Chapter 1(\*\*)?", line):
                    continue
                if PATTERN_END.fullmatch(line):
                    text = ""
                    break 

                pre = False
                
                if is_invalid_line(line):
                    continue
                if is_new_chapter(line):
                    if text and data["chapter"]:
                        data["text"] = text.strip()
                        f.write(json.dumps(data) + "\n")
                    data["chapter"] = re.search(r"Chapter\s.*", line.strip()).group(0)
                    data["chapter"] = data["chapter"][:-2] if data["chapter"].endswith("**") else data["chapter"]
                    text = ""
                    continue

                line = clean_line(line)
                if line:
                    text += "\n\n" + line

def simple_parse():
    with open(RAW_OUTPUT_FILEPATH, "w") as f:
        for file in files:
            filepath = path.join("data", "pdf_data", file)
            doc = fitz.open(filepath)

            for page, content in enumerate(doc, start=1):
                text = content.get_text()
                text = " ".join(text.split())
                length = len(text.split())

                data = {
                    "doc": file[:-4], "page":page, "text": text, 
                    "length": length, "source": filepath
                    }
                
                f.write(json.dumps(data) + "\n")
            doc.close()
    

if __name__ == "__main__":
    # simple_parse()
    smarter_parse()