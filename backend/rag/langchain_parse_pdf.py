from langchain_community.document_loaders import UnstructuredPDFLoader
import os
import nltk
nltk.download("punkt")

def parse_pdf(pdf_path: str, output_path: str):
    loader = UnstructuredPDFLoader(pdf_path)
    documents = loader.load()

    # Combine all parsed content into one string
    full_text = "\n".join(doc.page_content for doc in documents)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Parsed PDF saved to {output_path}")


if __name__ == "__main__":
    parse_pdf("../data/textbook.pdf", "output/parsed_textbook.txt")
