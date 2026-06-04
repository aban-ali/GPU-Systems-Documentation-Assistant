from os import path
import json

INPUT_RAW_FILEPATH = path.join("data", "processed", "raw_data.jsonl")
OUTPUT_FILEPATH = path.join("data", "processed", "chunks.jsonl")



def simple_chunk(chunk_size=800, overlap=150):
    f = open(INPUT_RAW_FILEPATH, "r")
    o = open(OUTPUT_FILEPATH, "a")

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

    f.close()
    o.close()


if __name__ == "__main__":
    simple_chunk()