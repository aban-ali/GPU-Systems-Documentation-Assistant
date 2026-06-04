import fitz
from os import path, listdir
import json

RAW_OUTPUT_FILEPATH = path.join("data", "processed", "raw_data.jsonl")

# # This is supposed to be used later
# files = listdir(path("data", "pdf_data"))

files = [
    "CUBLAS_Library.pdf",
    "CUDA_C_Best_Practices_Guide.pdf",
    "CUDA_C_Programming_Guide.pdf",
    "CUDA_Runtime_API.pdf",
    "ptx_isa_9.3.pdf"
]


def parse():
    for file in files:
        filepath = path.join("data", "pdf_data", file)
        doc = fitz.open(filepath)

        for page, content in enumerate(doc):
            text = content.get_text()

            length = len(list(filter(lambda x: len(x)>0, text.split(" "))))

            data = {
                "doc": file[:-4], "page":page, "text": text, 
                "length": length, "source": filepath
                }
            
            with open(RAW_OUTPUT_FILEPATH, "a") as f:
                f.write(json.dumps(data))
                f.write("\n")
    

if __name__ == "__main__":
    parse()