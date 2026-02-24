# 🔄 Keeping Render Free Tier Awake

## The Problem
Render free tier spins down after 15 minutes of inactivity. Cold starts take 30-60+ seconds (especially with ML models).

## Solutions Implemented

### 1. GitHub Actions (Automated)
- **File**: `.github/workflows/keep-alive.yml`
- **Frequency**: Every 14 minutes
- **Setup**: 
  1. After deploying to Render, get your service URL
  2. Edit `.github/workflows/keep-alive.yml`
  3. Replace `https://your-service.onrender.com` with your actual URL
  4. Commit and push
  5. GitHub will automatically ping your service

### 2. Cron-Job.org (Recommended)
1. Go to https://cron-job.org
2. Create free account
3. Add new cron job:
   - **Title**: SkillSwap Matching Service Keep-Alive
   - **URL**: `https://your-service.onrender.com/health`
   - **Schedule**: Every 14 minutes
   - **Method**: GET
4. Save and enable

### 3. UptimeRobot (Alternative)
1. Go to https://uptimerobot.com
2. Create free account
3. Add new monitor:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: SkillSwap Matching
   - **URL**: `https://your-service.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
4. Create monitor

### 4. Node.js Backend Integration
See `examples/nodejs-integration.js` for code that:
- Wakes up the service on Node.js startup
- Handles cold starts gracefully (2-minute timeout)
- Optionally pings every 10 minutes

## Best Practice: Use Multiple Methods

**Recommended Setup:**
1. ✅ GitHub Actions (primary, free, automated)
2. ✅ Cron-Job.org (backup, more reliable than GitHub)
3. ✅ Node.js keep-alive (bonus when main backend is active)

This ensures your service is **always warm** and users never experience cold starts.

## After Deployment Checklist

- [ ] Deploy to Render and get service URL
- [ ] Update `.github/workflows/keep-alive.yml` with real URL
- [ ] Commit and push changes
- [ ] Set up Cron-Job.org monitor
- [ ] (Optional) Set up UptimeRobot monitor
- [ ] (Optional) Add keep-alive to Node.js backend
- [ ] Test: Wait 20 minutes, then call API (should be instant)

## Monitoring

Check if it's working:
- GitHub Actions: Go to repo → Actions tab → See workflow runs
- Cron-Job.org: Dashboard shows execution history
- UptimeRobot: Dashboard shows uptime percentage

## Cost
**$0** - All solutions are completely free!
