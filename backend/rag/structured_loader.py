import re
import os
import json
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from toc import toc  # must exist

def split_text(text, chunk_size=2000, overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)


def extract_chunks_from_parsed_text(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        full_text = f.read().lower()

    chunks = []

    for i, entry in enumerate(tqdm(toc, desc="🔍 Extracting chunks")):
        pattern = re.escape(entry["subchapter_code"]) + r"\s+" + re.escape(entry["subchapter_title"].lower())

        # Start match
        match = re.search(pattern, full_text)
        if not match:
            print(f"⚠️ Could not find: {entry['subchapter_code']} {entry['subchapter_title']}")
            continue
        start_idx = match.start()

        # End match
        if i == len(toc) - 1:
            end_idx = len(full_text)
        else:
            next_entry = toc[i + 1]
            next_pattern = re.escape(next_entry["subchapter_code"]) + r"\s+" + re.escape(next_entry["subchapter_title"].lower())
            next_match = re.search(next_pattern, full_text)
            if not next_match:
                print(f"⚠️ Could not find end of: {entry['subchapter_code']} → next section missing: {next_entry['subchapter_code']}")
                end_idx = len(full_text)
            else:
                end_idx = next_match.start()

        # Slice and chunk
        sub_text = full_text[start_idx:end_idx]
        sub_chunks = split_text(sub_text)

        for chunk in sub_chunks:
            chunks.append({
                "text": chunk,
                "chapter_title": entry["chapter_title"],
                "subchapter_title": entry["subchapter_title"],
                "subchapter_code": entry["subchapter_code"]
            })

    return chunks


if __name__ == "__main__":
    chunks = extract_chunks_from_parsed_text("output/parsed_textbook.txt")

    os.makedirs("output", exist_ok=True)
    with open("output/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Saved {len(chunks)} chunks to 'output/chunks.json'")
