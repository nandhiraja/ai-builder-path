import fitz 


class DocumentChunker:

    def __init__(self, chunk_size=500, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def extract_text_from_pdf(self, pdf_path):
      
        document = fitz.open(pdf_path)
        text = ""
        for page in document:
            text += page.get_text()

        document.close()
        return text

    def clean_text(self, text):

        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        while "  " in text:
            text = text.replace("  ", " ")

        return text.strip()

    def split_into_chunks(self, text):
   
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):

            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)

            start += self.chunk_size - self.overlap

        return chunks

    def process_pdf(self, pdf_path):

        text = self.extract_text_from_pdf(pdf_path)
        text = self.clean_text(text)
        chunks = self.split_into_chunks(text)

        return chunks