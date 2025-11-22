# How to Push to GitHub - Updated Guide

## Method 1: Using GitHub CLI (Easiest) ✅

If you have GitHub CLI installed:

```bash
gh auth login
git push -u origin main
```

## Method 2: Using SSH Keys (Recommended)

### Step 1: Check if you have SSH keys
```bash
ls -la ~/.ssh
```

### Step 2: Generate SSH key (if you don't have one)
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default location
# Press Enter for no passphrase (or set one)
```

### Step 3: Copy your public key
```bash
cat ~/.ssh/id_ed25519.pub
# Copy the entire output
```

### Step 4: Add SSH key to GitHub
1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

### Step 5: Update remote and push
```bash
cd /Users/shankar/PROJECT/Ai_Powered_E_COM_Hub
git remote set-url origin git@github.com:shankar7055/backendfinal.git
git push -u origin main
```

## Method 3: Personal Access Token (Classic)

### Finding the Tokens Section:

1. **Go to GitHub Settings:**
   - Click your profile picture (top right)
   - Click "Settings"

2. **Navigate to Developer Settings:**
   - Scroll down in the left sidebar
   - Click "Developer settings" (at the bottom)

3. **Access Tokens:**
   - Click "Personal access tokens"
   - Click "Tokens (classic)" or "Fine-grained tokens"

4. **Generate Token:**
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: "backendfinal-push"
   - Expiration: Choose your preference
   - Scopes: Check `repo` (full control)
   - Click "Generate token"
   - **COPY THE TOKEN** (you won't see it again!)

5. **Use the token:**
   ```bash
   git push -u origin main
   # Username: shankar7055
   # Password: [paste your token here]
   ```

## Method 4: Using GitHub Desktop

1. Install GitHub Desktop: https://desktop.github.com/
2. Sign in with your GitHub account
3. Add the repository
4. Click "Push origin"

## Method 5: Direct Browser Upload (For Small Projects)

1. Go to: https://github.com/shankar7055/backendfinal
2. Click "uploading an existing file"
3. Drag and drop your files
4. Commit changes

## Quick Check: What Authentication Method Do You Have?

Run this to check:
```bash
# Check SSH
ls -la ~/.ssh/id_* 2>/dev/null && echo "✅ SSH keys found" || echo "❌ No SSH keys"

# Check GitHub CLI
which gh && echo "✅ GitHub CLI installed" || echo "❌ GitHub CLI not installed"
```

## Recommended: Use SSH (No Token Needed!)

SSH is the easiest once set up. Follow Method 2 above.

