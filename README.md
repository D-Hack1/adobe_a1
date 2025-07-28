# Persona-Driven Document Intelligence Pipeline (Adobe A1)

## Approach
This solution is designed to intelligently analyze a collection of PDFs and extract the most relevant sections based on a user persona and their job-to-be-done. The pipeline is robust and generic, supporting a wide variety of document types (e.g., research papers, recipes, reports) and user personas (e.g., researcher, food contractor, travel planner).

The methodology involves:
- **PDF Parsing and Outline Extraction:** Using PyMuPDF (fitz), the system parses each PDF, extracting text blocks with font size, position, and page number. A custom outline extractor merges adjacent word spans into lines and applies heuristics to identify likely section headings (H1, H2) or, for recipes, dish names. This process is Unicode-aware and supports multilingual documents.
- **Section/Dish Detection and Filtering:** For general documents, only prominent headings are considered as candidate sections. For recipes, additional heuristics detect likely dish names (short, capitalized, food-related lines), filtering out instructions or ingredient lists.
- **Refined Text Extraction:** For each detected section or dish, the pipeline extracts the next block(s) of text that likely represent a summary, recipe, or ingredient list, using heuristics (numbers, food words, or length).
- **Relevance Scoring and Ranking:** Each candidate section is scored for relevance based on overlap with persona/job keywords, scenario-specific terms (e.g., "vegetarian", "gluten-free", "dinner", "side"), and document filename. The top N (usually 5) most relevant sections are selected for output.
- **Output Format:** The output is a structured JSON file containing metadata, extracted sections (document, section title, importance rank, page), and subsection analysis. This format is generic and can be used for any persona, job, and document set.

## Models and Libraries Used
- **PyMuPDF (fitz):** For parsing and extracting text, font, and layout information from PDFs.
- **pandas:** For data manipulation and processing (as required by the pipeline).
- **Standard Python libraries:** `os`, `json`, `datetime`, `re`, `unicodedata`, and `collections` for file handling, text processing, and data organization.
- **No external machine learning models** are used; the approach is heuristic and rule-based for robustness and speed.

## How to Build and Run the Solution

### Dockerfile
```dockerfile
FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Execution Instructions

1. **Prepare Input:**
   - Place all PDF files and the required input JSON in the `input/` directory.

2. **Build the Docker Image:**
   - Open a terminal in the `adobe_a1` directory.
   - Run:
     ```
     docker build -t adobe_a1 .
     ```

3. **Run the Docker Container:**
   - Execute:
     ```
     docker run --rm -v "$PWD/input:/app/input" -v "$PWD/output:/app/output" adobe_a1
     ```
   - On Windows PowerShell, you may need to use:
     ```
     docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output adobe_a1
     ```

4. **Check Output:**
   - The processed JSON output will be available in the `output/` directory.

---

This README is for documentation purposes. The solution is fully containerized and should run as described in the "Expected Execution" section above. 