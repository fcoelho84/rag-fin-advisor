# Stock Analyser RAG

I'm building this application to help me analyze Brazilian stocks while studying and experimenting with RAG (Retrieval-Augmented Generation) concepts.

## Main Objectives
### 1. Extract Risk Factors from CVM

The main challenge here is retrieving the required data from the CVM.

The CVM does not make it straightforward to search for companies using their stock tickers. Instead, the company's CNPJ is required. To work around this, I first search for the stock on B3 and extract its CNPJ.

Using the CNPJ, I can then retrieve the company's latest FRE (Formulário de Referência). The FRE provides a URL to an XML file containing the company's documents.

From this XML, I only need the Risk Factors section. However, the relevant document is stored as a Base64-encoded PDF inside the XML. Therefore, the extraction process involves several parsing and decoding steps:

 - Find comany's CPNJ on B3.
 - Use the CNPJ to retrieve the latest FRE from the CVM.
 - Locate the Risk Factors section in the XML.
 - Decode the XML Base64 content to PDF.
 - Extract the text from the Risk Factors PDF.

The final goal is to transform this data into clean, searchable text that can be used by the RAG pipeline.

2. Extract News from Yahoo Finance

Collect relevant news and articles related to the selected stocks from Yahoo Finance.

The extracted news will be processed and stored alongside the CVM data, providing additional context for the analysis.

3. Generate Embeddings and Store the Data

Once the data has been collected and cleaned, I will generate embeddings for the documents and store them in a vector database.

This will allow the application to retrieve relevant information based on semantic similarity rather than relying only on keyword matching.

The final objective is to combine these sources in a RAG-based application that can retrieve relevant information about Brazilian stocks and use that context for analysis.