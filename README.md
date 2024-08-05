The system architecture is split into four parts: 1) Data Collection 2) Data Processing 3) Retrieval & Query, 4) Synethesis & Analysis.

**1 Data Collection**

   1. Manually search using keywords on Google Scholar
   2. Download Google Scholar search result page in HTML format
   3. "google_scholar_doc_crawler.py" uses _BeautifulSoup4_ to extract for every research paper: Name, Authors, Publication Info, Year, URL. The data is organized and outputted into "extraced_data.csv"
  
**2 Data Processing and Indexing & Embedding**

  1. "data_processing.py" is the main python module for processing, indexing, and embedding text data. "data_processing.py" calls three submodules, respectively: "heading_extractor.py", "extract_text_under_headings.py", and "index_and_embed_research_papers.py".

  _2.1 Data Processing_
  
  1. "heading_extractor.py" reads "extracted_data.csv" and uses the URL to download and access the PDF using _requests_ api, which provides internet access. PDFs that can't be accessed or downloaded are skipped (an error message is printed out).
  2. "heading_extractor.py" uses _PDFMiner.six_, a PDF text extraction library that uses the underlying encoding of the PDF to identify relationships between characters, words, paragraphs, columns, etc, to extract the PDF text. To filter the headings, _PDFMiner.six_ extracts all the text from the PDF in a structered format.
  3. Based on criteria that matches the template format of four major AI conferences: ACM, IEEE, AAAI, and NeurIPS, "heading_extractor.py" extracts the headings of each research paper. PDFs that don't fit the heading criteria any of the four templates will be skipped because they are most likely not a research paper. The headings are organized their research paper and outputted to "headings.json". The metadata for each research paper is also added to "headings.json".
  4. "extract_text_under_headings.py" uses _PDFMiner.six_ to extract all the text in the PDF, outputted to "raw_text.txt".
  5. "extract_text_under_headings.py" uses "headings.json" to conduct a String comparison for finding headings within the "raw_text.txt" and extracts the text underneath each heading. The headings with the text corresponding to the heading is outputted to "headings_with_text.json" along with metadata extracted from "headings.json"

  _2.2 Indexing & Embedding_

  1. "index_and_embed_reserach_papers.py" initializes a _Pinecone_ vector database index if one does not already exist.
  2. "index_and_embed_reserach_papers.py" uses _OpenAIEmbeddings_ model _text-embedding-3-large_ to embed the text extracted from "headings_with_text.json". Then the metadata is extracted for the heading and "research_paper_reference_generator.py" is called to generate an APA scientific paper standard formated citation for the research paper the heading belongs to using the metadata of the heading.
  3. For each heading text entry indexed "index_and_embed_reserach_papers.py" uses _uuid_ to generate a unique ID for a hash-map function that stores text under each heading entry indexed to Pinecone. The following metadata values: authors, heading_title, id, paper_title, paper_url, publication_info (publication venue or destination), publications_year, text_snippet (first 100 words of text) are stored alongside the text embedding per each Pinecone entry. We only store the first 100 words for text_snippet to provide context for each vector entry. We use the full text stored in our json source file. 
  4. "hash_map.json" is created to store the metadata, complete text, and id for the headings of each research paper.
  5. "process_hash_map_text.py" processes "hash_map.json" by deleting any in-text citations (e.g. Input: I love apples [67]. Apples are great. Output: I love apples. Apples are great.) and outputs the processed hash-map to "processed_hash_map.json". This is because we will add citation references in []'s later in our sythesized result, so we do not want any previous citation in the text when we cite it (and the paper it belongs to).  

**3 Retrieval & Query**

  1. "research_retrieve_and_query_research_papers.py" retrieves and queries multiple research papers one-by-one sequentially using metadata filtering by paper_title. "prompt_templates.query_constants.py" stores the _SINGLE_REFERENCE_RESPONSE_TEMPLATE_ prompt used. 
  2. "user_retrieve_and_query_reserach_paper.py" retrieves and queries mutltiple research paper's all at once. "prompt_templates.query_constants.py" stores the _MULTIPLE_REFERENCE_RESPONSE_TEMPLATE_ prompt used.
  3. Both "research_retrieve_and_query_research_papers.py" and "user_retrieve_and_query_reserach_paper.py" retrieve the most relevant documents in _Pinecone_ by cosine similarity comparison to the user query which is also embedded as a vector using _Langchain.VectoreStore_.
  4. The id metadata value for each document retrieved is extracted and mapped onto the corresponding id value in "processed_hash_map.json". Then the text and reference values are extracted from the JSON, concatenated for every heading extracted then inputted as context for the prompt created using _Langchain.PromptTemplate_.
  5. _ChatOpenAI_ is used to invoke the LLM (_GPT-4o_), which provides a response.
  6. "research_retrieve_and_query_research_papers.py" writes the responses for each paper into "rai_definitions.json"
  7. "user_retrieve_and_query_reserach_paper.py" prints the response to the terminal and continues to take in user inputs.

**4 Synthesis & Analysis**

  1. "research_paper_synthesis_and_analysis.py" extracts the definitions of Responsible AI from each reserach paper by reading the "rai_definitions.json".
  2. The definitions are concatenated and inputted as context for the prompt, which invokes the LLM (_GPT-4o_).
  3. The LLM response is printed to the terminal.

**5 Reference management**

  1. "find_references.py" prints out for each numbered paper in Reference section of the paper, if it was referenced in the paper. You can run a grep command to only see the ones that weren't: 

% ../akagi/find_references.py | grep NO

NO  [7]  How different groups prioritize ethical values for responsible AI
NO  [8]  Measurement as governance in and for responsible AI
NO  [11]  Where responsible AI meets reality: Practitioner perspect...
....

  2. "key_points_alignment.py": it asks for a number representing the paper, retrieves relevant content for all the principles from this paper, and ask if the content retrieved agrees, disagrees or has no opinion of each of the principles in the paper. 

For example: 

% ../akagi/key_points_alignment.py

  >>> 7 

Analyze paper:  How different groups prioritize ethical values for responsible AI
....


**6 Retrieval methods
We have two methods: 
  1. vector database: we store chunks in vector database, and retrieve using its similiarity query.
  2. BM25: we store chunks in BM25 index, and retrieve using BM25's scores method.

The following scripts in the "bm25-retrieval" directory are implementation using BM25 method:
  1. user_index_papers.py: index the chucks in a JSON file of papers.
  2. user_query_papers.py: query all the papers using BM25 retrieval for the RAG part. 