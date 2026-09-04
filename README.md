# Oracle APEX Business Intelligence Dashboard

This project fetches business data from Oracle APEX REST API endpoints and
generates an interactive Plotly dashboard as a standalone HTML file. It
includes charts for products, customers, orders, inventory, and sales.

The application also includes an optional terminal-based natural-language
query interface powered by Ollama.

## Features

- Fetches live data from Oracle APEX REST APIs
- Generates interactive Plotly charts
- Exports the dashboard to `combined_dashboard.html`
- Opens the generated dashboard in a web browser
- Supports natural-language questions about the data through Ollama

## Project structure

All application files:

- `main.py` - application entry point
- `configer.py` - API endpoints and output configuration
- `fetcher.py` - API data retrieval and cleanup
- `chartProducts.py` - products chart
- `chartCustomers.py` - customers chart
- `chartOrders.py` - orders chart
- `chartInventory.py` - inventory chart
- `chartSales.py` - sales chart
- `llm_query.py` - Ollama-powered terminal query interface

## Requirements

- Python 3.10 or newer
- Python packages:
  - `pandas`
  - `plotly`
  - `requests`
  - `urllib3`
- Optional: [Ollama](https://ollama.com/) with the `llama3` model

Install the Python dependencies with:

```bash
python -m pip install pandas plotly requests urllib3
```

## Running the dashboard

Run the application from the directory containing `main.py`:

```bash
cd "File_name"
python main.py
```

The program fetches the data, creates `combined_dashboard.html`, and opens it
in the default browser. Type `exit` in the terminal to close the query
interface.

## Using the natural-language query interface

Install and start Ollama, then pull the model configured by the application:

```bash
ollama pull llama3
ollama serve
```

In a separate terminal, run the application:

```bash
cd "amu's stuff"
python main.py
```

If Ollama is unavailable, the dashboard is still generated; the query
interface reports that the Ollama server could not be reached.

## Data and configuration

The API URLs and dashboard output filename are defined in
`amu's stuff/configer.py`. Update that file if the API endpoints change.

The API data is retrieved at runtime, so an internet connection is required.
