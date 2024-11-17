# AI Agent

This project is an AI-driven agent designed for automated web search, data extraction, and information processing. The agent integrates APIs, processes user-uploaded files, and provides an interactive dashboard for seamless user interaction.

---

## Features

- **User Dashboard**: Upload CSV files, input custom queries, and view/download results.
- **Web Search**: Uses SerpAPI to extract data from the web.
- **AI Integration**: Leverages Groq API for advanced data processing.
- **Dynamic Query Management**: Supports placeholder replacement in queries (e.g., `{company}`).
- **Data Handling**: Processes user files and integrates web-scraped data with uploaded datasets.
- **CSV Export**: Allows easy download of processed data for further analysis.

---


---

## Installation

### Prerequisites
- Python 3.10 or higher
- [pip](https://pip.pypa.io/en/stable/)
- [SerpAPI key](https://serpapi.com/)
- (Optional) [OpenAI/Groq API key](https://openai.com/)
---

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Mr-Mercury-P/Your-Search-Engine
   cd Your-Search-Engine
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the `env/` directory with:
     ```
     SERPAPI_KEY=your_serpapi_key
     OPENAI_API_KEY=your_openai_api_key
     ```

5. Run the application:
   ```bash
   python main.py
   ```

6. Access the dashboard:
   - Open `http://localhost:5000` in your browser.

---

## Usage

1. **Upload Files**: Add CSV files (e.g., Items) to the dashboard.
2. **Enter Query**: Input a dynamic query using placeholders, such as:
   ```
   "Find the Price of {Item}"
   ```
3. **View Results**: Review extracted data on the dashboard.
4. **Export Data**: Download the processed data as a CSV.

---

## Contribution

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your fork:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

---

## Acknowledgments

- **SerpAPI** for enabling web scraping.
- **Groq** for natural language processing.
- **Pandas** for data manipulation.
- **Flask** for the dashboard framework.

---

## License

This project is licensed under the MIT License. See `LICENSE` for more details.
```