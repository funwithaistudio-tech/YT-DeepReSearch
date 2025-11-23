# Usage Guide

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## Running

### Single Topic Mode

```bash
python src/main.py --mode single --topic "Your Topic Here"
```

### Excel Queue Mode

```bash
python src/main.py --mode queue
```

## Docker

```bash
docker build -t yt-deepresearch .
docker-compose up
```

## Configuration

Edit `.env` file with your API keys and settings.

See full usage documentation for advanced features.
