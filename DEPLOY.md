# Deploy to Render

## 🚀 Quick Deploy

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-detect `render.yaml`

3. **Add Environment Variables (Secret):**
   In Render dashboard, add these as **Secret** environment variables:
   
   ```
   DATABASE_URL = <your-supabase-connection-string>
   REDIS_UPSTASH_REST_URL = <your-upstash-redis-url>
   REDIS_UPSTASH_REST_TOKEN = <your-upstash-token>
   ```
   
   Get these from:
   - DATABASE_URL: Supabase Project Settings → Database → Connection String
   - REDIS: Upstash Console → Your Database → REST API

4. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy automatically

## 🔒 Security Features

✅ Environment variables stored as **encrypted secrets** in Render
✅ Never committed to git
✅ Automatically injected at runtime
✅ Can be updated without redeploying

## 📝 Local Development

Use `.env` file (already in `.gitignore`):
```bash
cp .env.example .env
# Edit .env with your local credentials
```

## 🔄 Updates

Push to GitHub → Render auto-deploys (if auto-deploy enabled)
