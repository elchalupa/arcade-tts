# Cloud Deployment Guide

Deploy Arcade TTS to RunPod Serverless for zero local GPU usage.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
- [Docker Hub](https://hub.docker.com/) account
- [RunPod](https://runpod.io/) account with credits

## Step 1: Prepare Your Voice File

Ensure your voice reference is in the `voices/` folder and named appropriately.

## Step 2: Build the Docker Image

```bash
docker build -t yourusername/arcade-tts:latest .
```

## Step 3: Test Locally (Optional)

```bash
docker-compose up
```

Test with:
```bash
curl "http://localhost:5000/health"
curl "http://localhost:5000/speak?text=Hello%20world"
```

## Step 4: Push to Docker Hub

```bash
docker login
docker push yourusername/arcade-tts:latest
```

## Step 5: Create RunPod Serverless Endpoint

1. Go to [RunPod Console](https://www.runpod.io/console/serverless)
2. Click **New Endpoint**
3. Configure:
   - **Name:** arcade-tts
   - **Container Image:** `yourusername/arcade-tts:latest`
   - **GPU:** RTX 3090 or similar (16GB+ recommended for fast cold starts)
   - **Container Disk:** 20 GB
   - **Idle Timeout:** 60 seconds (adjust based on stream frequency)
   - **Max Workers:** 1 (increase if needed)

4. Set Environment Variables:
   - `VOICE_REFERENCE`: `voices/default_voice.wav`
   - `PORT`: `5000`

5. Click **Create**

## Step 6: Get Your Endpoint URL

After creation, you'll receive an endpoint URL like:
```
https://api.runpod.ai/v2/your-endpoint-id/runsync
```

## Step 7: Update Streamer.bot

Change your Fetch URL sub-action from:
```
http://localhost:5000/speak?text=%rawInput%
```

To:
```
https://api.runpod.ai/v2/your-endpoint-id/runsync
```

With headers:
- `Authorization`: `Bearer YOUR_RUNPOD_API_KEY`
- `Content-Type`: `application/json`

And body:
```json
{
  "input": {
    "text": "%rawInput%"
  }
}
```

## Cost Optimization

### Idle Timeout
- Lower = cheaper but more cold starts
- Higher = faster response but pay for idle time
- Recommended: 60-120 seconds during stream hours

### Worker Count
- 1 worker handles ~8-12 requests/minute
- Increase only if you expect high redemption volume

### GPU Selection
- RTX 3090: Good balance of cost/performance
- RTX 4090: Faster generation, higher cost
- A4000: Budget option, slower

## Monitoring

View logs and usage in the RunPod Console:
- Request count
- Average response time
- GPU utilization
- Cost breakdown

## Troubleshooting

### "Container failed to start"
- Check Docker Hub image is public or RunPod has access
- Verify GPU requirements match selected GPU

### "Request timeout"
- First request has cold start (~30-45 seconds)
- Increase timeout in Streamer.bot

### "Out of memory"
- Select GPU with more VRAM
- Check for memory leaks in logs

## Estimated Costs

| Usage | Monthly Cost |
|-------|-------------|
| 16 requests/month (2/stream × 8 streams) | $0.10 - $0.50 |
| 50 requests/month | $0.30 - $1.50 |
| 200 requests/month | $1.00 - $5.00 |

Costs vary based on:
- Cold start frequency
- GPU tier selected
- Idle timeout settings
