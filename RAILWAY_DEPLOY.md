# 🚂 Railway Deployment Guide (Vercel Alternative)

Railway.app is the closest alternative to Vercel for Streamlit apps. It offers a similar Git-based deployment experience.

## Why Railway?

- ✅ Git-based deployment (like Vercel)
- ✅ Automatic deploys on push (like Vercel)
- ✅ Easy environment variables (like Vercel)
- ✅ Free $5/month credit
- ✅ Custom domains supported
- ✅ Works with Streamlit perfectly

---

## 🚀 Quick Deploy (5 Minutes)

### Step 1: Push to GitHub

```bash
# If not already done
git init
git add .
git commit -m "Ready for Railway deployment"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to **[railway.app](https://railway.app)**
2. Click **"Login with GitHub"**
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway will auto-detect it's a Python app!

### Step 3: Add Environment Variable

1. In Railway dashboard, click your project
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add:
   ```
   OPENAI_API_KEY = sk-your-actual-key-here
   ```
5. Click **"Add"**

### Step 4: Wait for Deploy

- Railway automatically installs dependencies from `requirements.txt`
- Builds and deploys your app
- Gives you a public URL like: `https://your-app.up.railway.app`

### Step 5: Done! 🎉

Your app is live! Click the generated URL to visit it.

---

## 🔄 Auto-Deploy on Push

Every time you push to GitHub:
```bash
git add .
git commit -m "Update features"
git push
```

Railway **automatically redeploys** your app! (Just like Vercel)

---

## 🌐 Custom Domain (Optional)

1. In Railway dashboard, go to **Settings**
2. Click **"Domains"**
3. Click **"Custom Domain"**
4. Add your domain: `philosophers.yourdomain.com`
5. Update your DNS records as shown
6. Done!

---

## 💰 Pricing

**Free Tier:**
- $5 free credit per month
- ~500 hours of uptime
- Perfect for personal projects
- No credit card required to start

**Pro Plan:** $5/month
- $5 credit + usage-based pricing
- More resources
- Priority support

---

## 📊 Monitoring

Railway dashboard shows:
- ✅ Deploy status
- ✅ Logs (real-time)
- ✅ CPU/Memory usage
- ✅ Request metrics
- ✅ Build history

---

## 🐛 Troubleshooting

### "Module not found" Error
- Check `requirements.txt` is committed
- Redeploy: Settings → Redeploy

### "Port already in use"
- Railway sets `$PORT` automatically
- Your `railway.toml` handles this ✅

### App Not Loading
- Check logs in Railway dashboard
- Verify `OPENAI_API_KEY` is set
- Check build completed successfully

---

## 📁 Files You Already Have

✅ `railway.toml` - Railway configuration
✅ `requirements.txt` - Python dependencies  
✅ `app.py` - Main application
✅ `.streamlit/config.toml` - Streamlit config

Everything is ready! Just push to GitHub and deploy on Railway.

---

## 🆚 Railway vs Vercel

| Feature | Vercel | Railway |
|---------|--------|---------|
| Streamlit Support | ❌ No | ✅ Yes |
| Python Apps | ❌ Limited | ✅ Full |
| Git-based Deploy | ✅ Yes | ✅ Yes |
| Auto-deploy | ✅ Yes | ✅ Yes |
| Free Tier | ✅ Yes | ✅ Yes ($5 credit) |
| Custom Domains | ✅ Yes | ✅ Yes |
| Environment Vars | ✅ Yes | ✅ Yes |

**For Streamlit apps: Railway > Vercel** 🚂

---

## Alternative: Render.com

Another Vercel-like platform that supports Streamlit:

1. Go to **[render.com](https://render.com)**
2. Connect GitHub
3. Create **"New Web Service"**
4. Select your repo
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Add environment variable: `OPENAI_API_KEY`
7. Deploy!

**Free tier:** 750 hours/month

---

## 🎯 Recommended Choice

**For easiest Streamlit deployment:**
1. **Streamlit Community Cloud** - Simplest, made for Streamlit
2. **Railway.app** - Most Vercel-like experience
3. **Render.com** - Good alternative

All three are better than Vercel for your Streamlit app!

