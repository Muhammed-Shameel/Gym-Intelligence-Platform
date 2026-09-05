#!/bin/bash
# Deployment script for GFIP Agentic AI MVP
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"

echo "Deploying to Project: $PROJECT_ID, Region: $REGION"

# 1. Build Backend Image
gcloud builds submit backend --tag gcr.io/$PROJECT_ID/gfip-backend

# 2. Build Frontend Image
gcloud builds submit frontend --tag gcr.io/$PROJECT_ID/gfip-frontend

# 3. Deploy Backend
gcloud run deploy gfip-backend \
  --image gcr.io/$PROJECT_ID/gfip-backend \
  --region $REGION --allow-unauthenticated

# 4. Deploy Frontend
gcloud run deploy gfip-frontend \
  --image gcr.io/$PROJECT_ID/gfip-frontend \
  --region $REGION --allow-unauthenticated

echo "Deployment complete."
