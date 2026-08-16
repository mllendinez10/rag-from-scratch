""" 
Split the extracted document text into smaller chunks for use in the RAG pipeline.

This script will:
- Receive the pages extracted from the PDFs by load_documents.py, the chunk size and overlap
- Split each page into smaller text chunks
- Keep metadata such as the original page number and PDF source
- Assign a chunk number to each chunk
- Return the chunks for the next step: keyword search and semantic search

"""

def chunk_documents(pages, chunk_size=500, overlap=50):
    

    chunks = []
    
    chunk_number = 1
    
    # Define how far the next chunk moves
    step = chunk_size - overlap
    
    
    for page in pages:
        
        # Get text and metadata from current page
        text = page["text"]
        page_number = page["page"]
        source = page["source"]
        
        # Move through the page text in steps
        for i in range(0,len(text),step):
        
            #Create chunk with defined size
            chunk_text = text[i:i+chunk_size]
            
            # Store chunk text and metadata in the list
            chunks.append({
                
                "chunk": chunk_number,
                "source": source,
                "page": page_number,
                "text": chunk_text
                
            })
            
            chunk_number +=1
            
    return chunks