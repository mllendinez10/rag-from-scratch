""" 
Split the extracted document text into smaller chunks for use in the RAG pipeline.

This script will:
- Receive the pages extracted from the PDF from load_documents.py, the chunk size and the overlap
- Split each page into smaller text chunks
- Keep metadata such as the original page number
- Assign a chunk number to each chunk
- Return the chunks for the next step : embeddings

"""

def chunk_documents(pages, chunk_size=500, overlap=50):
    
    chunks = []
    
    chunk_number = 1
    
    for page in pages:
        text = page["text"]
        page_number = page["page"]
        
        start = 0
        
        while start < len(text):
            
            end = start + chunk_size
            
            chunk_text = text[start:end]
            
            chunks.append({
                
                "chunk" : chunk_number,
                "page" : page_number,
                "text" : chunk_text
                
            })
            
            chunk_number += 1
            start = end - overlap
            
    return chunks