[User Interface] ──(Upload V1 & V2 PDFs)──> [FastAPI Backend]
                                                    │
             ┌──────────────────────────────────────┴─────────────────────────────────────┐
             ▼                                      ▼                                     ▼
     [Parsers & Chunkers]                [Vector DB: Pinecone/Chroma]            [Asynchronous Queue]
   • Strip formatting from PDF          • Store embeddings of clauses            • Celery / Redis Queue
   • Extract semantic clauses            • Cross-reference V1 vs V2               • Process large files in bg
             │                                                                            │
             └──────────────────────────────────────┬─────────────────────────────────────┘
                                                    ▼
                                          [LLM Reasoning Layer]
                                       • Compare semantic changes
                                       • Highlight missing liabilities
🛠️ Step-by-Step Implementation Guide
Phase 1: Robust PDF Parsing & Clause Chunking (The Data Layer)
Contracts are notoriously painful to parse. Recruiters will be deeply impressed if you show you can handle messy data extraction instead of using standard text splitters.
• The Tech: PyMuPDF or Marker (for layout-aware PDF text extraction).
• The Strategy: Do not just split text by character counts. Write a custom Python script that chunks text by logical elements (e.g., Title, Recitals, Section 1.1, Section 1.2, Indemnification).
• Recruiter Talking Point: "I built a custom layout-aware parser to ensure legal definitions remained bound to their operational clauses during tokenization."
Phase 2: Asynchronous Background Processing (The Backend Layer)
Processing two 50-page legal documents takes time. If a user uploads them to a web server and waits, the connection will time out. You must handle this asynchronously.
• The Tech: FastAPI (for the web framework) + Celery (with Redis) or Python’s native asyncio background tasks.
• The Strategy: When the user uploads Version 1 and Version 2, FastAPI immediately returns a 202 Accepted status code with a unique Task ID. In the background, your worker picks up the PDFs, extracts the text, and calculates the embeddings.
• Recruiter Talking Point: "Decoupled the ingestion API from the processing engine using an asynchronous worker queue, allowing the system to handle multi-megabyte document streams without blocking the main event loop."
Phase 3: Semantic Diff & Vector Cross-Referencing (The AI Layer)
This is the core of the project. If Version 1 says "Provider will pay for damages up to $10,000" and Version 2 says "Vendor liability is capped at ten thousand dollars", a standard text diff highlights this as a change. A semantic diff realizes they mean the exact same thing and ignores it. Conversely, if Version 2 silently deletes the word "not", the system needs to flag it immediately.
• The Tech: langchain-core, an embedding model (like text-embedding-3-small), and Chroma or Pinecone.
• The Strategy:
	1. Embed all chunks of Version 1 and upsert them to your Vector Database.
	2. Loop through every chunk of Version 2 and perform a similarity search against the Version 1 index.
	3. If a chunk from V2 has a highly similar match in V1, pass both clauses to an LLM (e.g., GPT-4o-mini or Claude Haiku) with a prompt like: "Compare these two clauses. Identify if there is a substantive change in legal obligation, liability, or timelines. If the change is purely stylistic, return 'None'."
	4. If a chunk from V1 has no match in V2, flag it as "Deleted Clause". If a chunk from V2 has no match in V1, flag it as "New Clause".
Phase 4: Production Elements (The "Secret Sauce")
To separate yourself from the sea of junior developers, you need to wrap this in engineering best practices:
• Testing: Use pytest to mock your LLM calls using unittest.mock. Recruiters hate seeing people burn through API credits running unit tests. Show you know how to mock external APIs.
• Dockerization: Write a Dockerfile for your FastAPI app and a docker-compose.yml that stands up the FastAPI app, your Redis worker, and your local database automatically.
• Observability: Integrate LangSmith or Arize Phoenix to track token usage, latency, and cost per contract analysis.
🎨 How to Build the UI Quickly
Don't waste weeks building a complex React/Vue frontend unless you want to be a frontend developer. Use Streamlit or Gradio in Python.
1. Side-by-side file uploaders for V1 and V2 PDFs.
2. A "Process" button that polls your FastAPI backend.
3. A clean table rendering the changes categorized by severity: 🔴 Critical Change (e.g., Liability limits shifted), 🟡 Moderate Change (e.g., Payment terms changed from 30 to 45 days), 🟢 Stylistic Only.
Would you like to start by setting up the project blueprint? I can generate the initial FastAPI file structure and the core Docker Compose configuration so you can spin up the environment right away!
Ready to create a plan?
Use Canvas to save, edit, and share your planning progress
Get started
