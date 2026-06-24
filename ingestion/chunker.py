from os import path
import json
import re

INPUT_RAW_FILEPATH = path.join("data", "processed", "raw_data.jsonl")
OUTPUT_FILEPATH = path.join("data", "processed", "chunks.jsonl")

PATTERN_PSEUDO_HEADER = re.compile(r"#+\s\*\*.*\*\*")
PATTERN_HEADER = re.compile(r"#+\s(\*\*)?\d+\.\d+\.?\s.*(\*\*)?")
PATTERN_SUBHEADER = re.compile(r"#+\s(\*\*)?\d+\.\d+\.\d+.*(\*\*)?")


def get_chunks(lines:str, subheading:str, chunk_size: int, overlap: int):
    chunks = []
    length = 0
    text = ""

    for line in lines.split("\n"):
        if PATTERN_SUBHEADER.fullmatch(line):
            if text:
                chunks.append({
                    "subheading": subheading, "text": text,
                    "length": length
                })
            subheading = line
            text = ""
            length = 0
            continue
        if length >= chunk_size:
            chunks.append({
                "subheading": subheading, "text": text,
                "length": length
            })
            text = " ".join(text.split(" ")[-overlap:])
            length = overlap
        text += line + "\n"
        length += len(line.split(" "))
    if text:
        chunks.append({
            "subheading": subheading, "text": text,
            "length": length
        })
    return chunks
 
def smart_markdown_chunk(chunk_size=500, overlap=50):
    with open(INPUT_RAW_FILEPATH, "r") as f,\
        open(OUTPUT_FILEPATH, "w") as o:
        for chapter, raw_line in enumerate(f, start=1):
            raw_data = json.loads(raw_line)
            lines = raw_data["text"].split("\n\n")
            chunk_idx = 1
            data = {
                "source": raw_data["doc"], "length": 0,
                "chapter": raw_data["chapter"], "heading": None, 
                "subheading": None
            }
            text = ""

            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue

                data["chunk_id"] = f"{raw_data["doc"]}_chapter{chapter}_c{chunk_idx}"

                if not data["heading"] and PATTERN_PSEUDO_HEADER.fullmatch(line):
                    data["heading"] = line
                    continue
                if PATTERN_HEADER.fullmatch(line):
                    if data["length"] > chunk_size+2*overlap:
                        chunks = get_chunks(text, data["subheading"], chunk_size, overlap)
                        for chunk in chunks:
                            if not chunk["text"].strip():
                                continue
                            data["chunk_id"] = f"{raw_data["doc"]}_chapter{chapter}_c{chunk_idx}"
                            data["subheading"] = chunk["subheading"]
                            data["length"] = chunk["length"]
                            data["text"] = chunk["text"]
                            data["chunk_idx"] = chunk_idx
                            o.write(json.dumps(data) + "\n")
                            chunk_idx += 1
                    else:
                        if text:
                            data["text"] = text
                            data["chunk_idx"] = chunk_idx
                            o.write(json.dumps(data) + "\n")
                            chunk_idx += 1
                    text = ""
                    data["length"] = 0
                    data["heading"] = line
                    data["subheading"] = None

                if data["length"]>3*overlap and PATTERN_SUBHEADER.fullmatch(line):
                    if data["length"] > chunk_size+2*overlap:
                        chunks = get_chunks(text, data["subheading"], chunk_size, overlap)
                        for chunk in chunks:
                            if not chunk["text"].strip():
                                continue
                            data["chunk_id"] = f"{raw_data["doc"]}_chapter{chapter}_c{chunk_idx}"
                            data["subheading"] = chunk["subheading"]
                            data["length"] = chunk["length"]
                            data["text"] = chunk["text"]
                            data["chunk_idx"] = chunk_idx
                            o.write(json.dumps(data) + "\n")
                            chunk_idx += 1
                    else:
                        if text:
                            data["text"] = text
                            data["chunk_idx"] = chunk_idx
                            o.write(json.dumps(data) + "\n")
                            chunk_idx += 1
                    text = ""
                    data["length"] = 0
                    data["subheading"] = line

                text += line + "\n"
                data["length"] += len(line.split(" "))
            if text:
                data["text"] = text
                data["chunk_idx"] = chunk_idx
                o.write(json.dumps(data) + "\n")

def simple_chunk(chunk_size=800, overlap=150):
    with open(INPUT_RAW_FILEPATH, "r") as f,\
        open(OUTPUT_FILEPATH, "w") as o:

        for line in f:
            raw_data = json.loads(line)
            start, chunk = 0, 1

            while(start < len(raw_data["text"])):
                end = start + chunk_size

                data = {
                    "chunk_id": f"{raw_data['doc']}_p{raw_data['page']}_c{chunk}",
                    "chunk_index": chunk, "page": raw_data["page"], "source": raw_data["source"],
                    "text": raw_data["text"][start:end], "doc": raw_data["doc"]
                }

                start += chunk_size - overlap
                chunk += 1

                if len(data["text"].strip()) == 0:
                    break

                o.write(json.dumps(data) + "\n")


if __name__ == "__main__":
    # simple_chunk()
    smart_markdown_chunk()