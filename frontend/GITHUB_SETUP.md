# Setting up GitHub Repository for Drive2Gather Frontend

This guide will walk you through the process of setting up the Drive2Gather frontend on GitHub Pages.

## Initial Setup

1. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Name it "Drive2Gather"
   - Make it public
   - Don't initialize with any files

2. Push the frontend code to GitHub:
```bash
# Navigate to frontend directory
cd frontend

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add the remote repository
git remote add origin https://github.com/JasonOw718/Drive2Gather.git

# Push to GitHub
git push -u origin main
```

## Configure GitHub Pages

1. In your GitHub repository settings:
   - Go to Settings > Pages
   - Under "Build and deployment", select "GitHub Actions" as the source
   - GitHub will automatically detect and suggest the Vue.js workflow

2. Set up repository variables for the API URL:
   - Go to Settings > Secrets and variables > Actions
   - Click on "New repository variable"
   - Name: `VITE_API_BASE_URL`
   - Value: Your API URL (e.g., `http://127.0.0.1:5000/api` for development or your production API)
   - Click "Add variable"

## Manual Deployment

If you want to deploy manually instead of using GitHub Actions:

1. Install the gh-pages package:
```bash
npm install --save-dev gh-pages
```

2. Run the deployment script:
```bash
npm run deploy
```

## Testing the Deployment

1. Wait for the GitHub Actions workflow to complete (if using automatic deployment), or for the manual deployment to finish.

2. Visit `https://jasonow718.github.io/Drive2Gather/` to see your deployed application.

## Troubleshooting

If your routes don't work properly:
1. Make sure your Vue Router is using history mode
2. Confirm that the 404.html file is correctly set up
3. Check that the script in index.html for handling GitHub Pages routing is working properly

If API calls fail:
1. Verify the CORS configuration on your backend API
2. Check that the VITE_API_BASE_URL is correctly set in GitHub repository variables 