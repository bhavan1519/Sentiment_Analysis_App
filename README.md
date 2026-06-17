# Sentiment Analysis Project

A Streamlit app for extracting and analyzing sentiment from product reviews stored in PDF files.

## Features

- Upload a PDF containing product reviews
- Extract review text from PDF pages using `PyPDF2`
- Analyze sentiment with `TextBlob`
- Display review-level sentiment categories: Positive, Negative, Neutral
- Show summary metrics and visualizations with `Plotly`
- Filter reviews by sentiment and inspect individual review details
- Download analysis results as a CSV file

## Requirements

The project dependencies are listed in `requirements.txt` and include:

- `streamlit`
- `pandas`
- `PyPDF2`
- `textblob`
- `plotly`

## Installation

1. Create and activate a Python virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. If needed, download the TextBlob corpora:

```bash
python -m textblob.download_corpora
```

## Usage

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

<<<<<<< HEAD
Open the URL shown in the terminal (usually `http://localhost:8501`) and upload a PDF file containing product reviews.
=======
Open the URL and upload a PDF file containing product reviews.
>>>>>>> e33aa8f99df9034d7d0e2fce500bc2e452143a64

## How It Works

- The app reads the uploaded PDF with `PyPDF2`.
- It splits the text into separate reviews using regular expressions.
- Each review is analyzed with `TextBlob` to compute a polarity score.
- Reviews are categorized as Positive, Negative, or Neutral.
- The app displays metrics, charts, and a review table, and allows export to CSV.

## Notes

- The PDF should contain review text in a recognizable format.
- The review splitter uses numbered review formatting (`1. Review text`, `2. Review text`, etc.).

## License

<<<<<<< HEAD
This project does not include a license file. Feel free to add one if you want to share or distribute it.
=======
This project is developed for academic purposes.
>>>>>>> e33aa8f99df9034d7d0e2fce500bc2e452143a64
