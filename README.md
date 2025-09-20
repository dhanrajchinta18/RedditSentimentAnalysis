# Reddit Sentiment App

A Django web application for analyzing Reddit post sentiment, with support for Spark-based data processing and CSV data exploration.

## Features

- Sentiment analysis of Reddit posts
- CSV data ingestion and cleaning
- Spark and non-Spark data processing demos
- Django web interface for search and visualization

## Project Structure

- `reddit_sentiment_app/` – Django project settings and URLs
- `sentiment/` – Main app: views, templates, Spark integration
- `data.csv`, `reddit_data.csv`, `cleaned.csv` – Reddit datasets
- `temp.csv`, `selected_output.csv` – Intermediate/processed CSVs

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run migrations**
   ```sh
   python manage.py migrate
   ```
4. **Start the server**
   ```sh
   python manage.py runserver
   ```

## Spark Integration

- Requires a working PySpark installation.
- See `sentiment/temp1.py` and `sentiment/views.py` for Spark usage examples.

## Configuration

- Edit `reddit_sentiment_app/settings.py` for database and Django settings.
- Place your CSV data in the project root as needed.

## License

- This is for educational purpose only.

## Author
- Dhanraj Chinta