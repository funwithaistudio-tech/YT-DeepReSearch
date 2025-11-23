# YT-DeepReSearch Deployment Guide

## Prerequisites

- Python 3.10+
- Docker (optional)
- Perplexity API key
- Google Cloud account with Vertex AI enabled

## Local Deployment

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/funwithaistudio-tech/YT-DeepReSearch.git
cd YT-DeepReSearch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `.env` file:

```env
PERPLEXITY_API_KEY=your_perplexity_key
GEMINI_API_KEY=your_gemini_key
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### 3. Google Cloud Setup

```bash
# Install gcloud CLI
# Visit: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Create service account (optional)
gcloud iam service-accounts create yt-deepresearch
gcloud iam service-accounts keys create credentials.json \
  --iam-account=yt-deepresearch@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 4. Run Application

**Single topic:**
```bash
python src/main.py --mode single --topic "Your Topic"
```

**Excel queue:**
```bash
python src/main.py --mode queue
```

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t yt-deepresearch:latest .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Docker Environment Variables

Edit `docker-compose.yml`:

```yaml
environment:
  - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
  - GEMINI_API_KEY=${GEMINI_API_KEY}
  - GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}
```

## Production Deployment

### Option 1: VM/Cloud Server

```bash
# SSH to server
ssh user@your-server

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3.10 python3-pip git

# Clone and setup
git clone https://github.com/funwithaistudio-tech/YT-DeepReSearch.git
cd YT-DeepReSearch
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your keys

# Run as service (systemd)
sudo nano /etc/systemd/system/yt-deepresearch.service
```

**Service file:**
```ini
[Unit]
Description=YT-DeepReSearch Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/YT-DeepReSearch
Environment="PATH=/home/ubuntu/YT-DeepReSearch/venv/bin"
ExecStart=/home/ubuntu/YT-DeepReSearch/venv/bin/python src/main.py --mode queue
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable yt-deepresearch
sudo systemctl start yt-deepresearch
sudo systemctl status yt-deepresearch
```

### Option 2: Cloud Run (GCP)

```bash
# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT/yt-deepresearch

# Deploy to Cloud Run
gcloud run deploy yt-deepresearch \
  --image gcr.io/YOUR_PROJECT/yt-deepresearch \
  --platform managed \
  --region us-central1 \
  --set-env-vars PERPLEXITY_API_KEY=your_key,GEMINI_API_KEY=your_key
```

### Option 3: Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yt-deepresearch
spec:
  replicas: 1
  selector:
    matchLabels:
      app: yt-deepresearch
  template:
    metadata:
      labels:
        app: yt-deepresearch
    spec:
      containers:
      - name: yt-deepresearch
        image: yt-deepresearch:latest
        env:
        - name: PERPLEXITY_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: perplexity
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: gemini
```

## Monitoring and Logs

### View Logs

```bash
# Local
tail -f logs/yt-deepresearch.log

# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u yt-deepresearch -f
```

### Monitoring Setup

1. **Application Logs**: Check `logs/` directory
2. **Excel Status**: Monitor `input/topics.xlsx` Status column
3. **Output Files**: Check `output/` directory

## Backup and Maintenance

### Backup

```bash
# Backup output and input
tar -czf backup-$(date +%Y%m%d).tar.gz output/ input/ logs/

# Backup to S3 (optional)
aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://your-bucket/backups/
```

### Maintenance Tasks

```bash
# Clean old outputs (older than 30 days)
find output/ -type d -mtime +30 -exec rm -rf {} \;

# Rotate logs
logrotate /etc/logrotate.d/yt-deepresearch
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify `.env` file has correct keys
   - Check API key validity on provider dashboards

2. **Google Cloud Auth**
   ```bash
   gcloud auth application-default login
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
   ```

3. **Import Errors**
   - Ensure Python path includes `src/` directory
   - Check virtual environment is activated

4. **Excel Permission Errors**
   - Close Excel file before running
   - Check file permissions

### Health Checks

```bash
# Test configuration
python src/main.py --help

# Test API connections
python -c "import sys; sys.path.insert(0, 'src'); from config.settings import Settings; s = Settings(); print('✓ Config loaded')"

# Run tests
pytest tests/ -v
```

## Scaling

### Horizontal Scaling

- Deploy multiple instances with separate Excel files
- Use load balancer for API requests
- Implement queue-based processing

### Vertical Scaling

- Increase `max_workers` in Phase 2 for parallel research
- Adjust `max_tokens_per_request` for larger batches
- Allocate more memory for large topics

## Security

### Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Limit file permissions** on credentials
5. **Use HTTPS** for all API calls
6. **Enable audit logging** in production

### Security Checklist

- [ ] API keys in environment variables
- [ ] `.env` in `.gitignore`
- [ ] Service account with minimal permissions
- [ ] Regular dependency updates
- [ ] Network security rules configured
- [ ] Backup encryption enabled

## Performance Optimization

1. **Reduce API latency**: Deploy in same region as APIs
2. **Cache results**: Implement Redis for repeated queries
3. **Batch processing**: Process multiple topics in parallel
4. **Optimize token usage**: Fine-tune chunking parameters

## Support

For deployment issues:
1. Check logs in `logs/yt-deepresearch.log`
2. Review documentation in `docs/`
3. Create GitHub issue with logs and configuration
