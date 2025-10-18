flowchart TD
    A["User Browser / Frontend (Node.js)"] -->|upload resume / view results| B["FastAPI Backend (Python)"]
    B -->|store resume & parsed data| C["S3 Bucket"]
    B -->|store structured metadata| D["DynamoDB"]
    B -->|reasoning & text generation| E["Amazon Bedrock LLM"]
    B -->|search/scrape program websites| F["External Web / SerpAPI"]
    B -->|faculty info matching| G["Faculty Web Pages"]
    B -->|generate tracker| H["Tracker (CSV/DB)"]
    A -->|display recommended programs + requirements + faculty + tracker| B
