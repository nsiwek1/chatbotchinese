# 🚀 Deployment Guide - Ancient Chinese Philosophers App

## Recommended: Streamlit Community Cloud (FREE)

### Prerequisites
1. GitHub account
2. Your code in a GitHub repository
3. OpenAI API key

### Step-by-Step Instructions

#### 1. Prepare Your Repository

Make sure you have these files (already included ✅):
- `app.py` - Main application
- `utils.py` - Utilities
- `pages/1_Debate_Mode.py` - Debate page
- `requirements.txt` - Dependencies
- `confucius-2.png` - Image
- `mencius.png` - Image
- `.streamlit/config.toml` - Configuration

#### 2. Push to GitHub

```bash
# If not already a git repo
git init
git add .
git commit -m "Initial commit - Philosopher chat app"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

#### 3. Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign in with GitHub"**
3. Click **"New app"**
4. Fill in the form:
   - **Repository:** Select your repository
   - **Branch:** main
   - **Main file path:** `app.py`
   - **App URL:** Choose a custom name (optional)

5. Click **"Advanced settings"**
6. Add **Secrets** (important!):
   ```toml
   [openai]
   api_key = "your-openai-api-key-here"
   ```
   
   *Alternative flat structure (also works):*
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

7. Click **"Deploy!"**

#### 4. Wait for Deployment

The app will:
- Install dependencies from `requirements.txt`
- Start the Streamlit server
- Give you a public URL like: `https://your-app-name.streamlit.app`

#### 5. Update Your App

Every time you push to GitHub:
```bash
git add .
git commit -m "Update features"
git push
```

Streamlit Cloud will automatically redeploy! 🎉

---

## Alternative: Railway.app

### Quick Deploy

1. Go to **[railway.app](https://railway.app)**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Add environment variable:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key
6. Railway auto-detects Python and deploys!

**Advantages:**
- Very fast
- Automatic HTTPS
- Good free tier
- Easy to use

---

## Alternative: Heroku

### Files Needed

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Deploy

```bash
# Install Heroku CLI first
heroku login
heroku create your-philosopher-app
git push heroku main
heroku config:set OPENAI_API_KEY="your-key-here"
heroku open
```

---

## ⚠️ Important Notes

### 1. Keep Your API Key Secret!

Never commit your `.env` file or expose your API key in code!

Add to `.gitignore`:
```
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

### 2. Environment Variables

Your app uses `python-dotenv` which loads from `.env` locally, but in production:
- **Streamlit Cloud:** Use Secrets management
- **Railway/Heroku:** Use environment variables in dashboard
- **AWS/GCP:** Use their secrets managers

### 3. Free Tier Limits

**Streamlit Cloud:**
- 1 GB memory per app
- Unlimited public apps
- Private repos allowed
- Community support

**Railway:**
- $5 free credit per month
- ~500 hours of uptime
- Automatic scaling

**Heroku:**
- Limited free tier (check current pricing)
- Sleep after 30 mins of inactivity

---

## 🎯 Recommended Flow

1. **Development:** Run locally with `streamlit run app.py`
2. **Testing:** Test all features (chat, debate, export, themes)
3. **Git:** Commit and push to GitHub
4. **Deploy:** Use Streamlit Cloud for easiest deployment
5. **Share:** Get your public URL and share!

---

## 📝 Troubleshooting

### "Module not found" Error
- Check `requirements.txt` includes all dependencies
- Redeploy or restart the app

### "API Key not found" Error
- Verify you added `OPENAI_API_KEY` to secrets/env vars
- Check for typos in the key name

### App Won't Start
- Check logs in deployment platform
- Verify `app.py` is in the root directory
- Ensure all files are committed to git

### Images Not Loading
- Verify image files are in root directory
- Check they're committed to git
- Use relative paths (already done ✅)

---

## 🌟 Your App is Ready!

All files are prepared for deployment. Just:
1. Push to GitHub
2. Deploy on Streamlit Cloud
3. Add your OpenAI API key to secrets
4. Share your app URL! 🎉

**Example URL:** `https://ancient-philosophers.streamlit.app`

