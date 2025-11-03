Write-Host '=== Fixing Git Branch Issues ===' -ForegroundColor Cyan

# Check current directory
Write-Host "Current directory: $PWD" -ForegroundColor Yellow

# Check git status
Write-Host "1. Checking Git status..." -ForegroundColor Yellow
git status
git branch -a

# Remove sensitive files
Write-Host "2. Removing sensitive files..." -ForegroundColor Yellow
Remove-Item -Force token.pickle -ErrorAction SilentlyContinue
Remove-Item -Force credentials.json -ErrorAction SilentlyContinue

# Rename branch to main if needed
Write-Host "3. Ensuring main branch..." -ForegroundColor Yellow
$currentBranch = git branch --show-current
if ($currentBranch -eq 'master') {
    git branch -M main
    Write-Host "   Renamed master to main" -ForegroundColor Green
}

# Add and commit
Write-Host "4. Committing changes..." -ForegroundColor Yellow
git add .
git commit -m "Final Docker CI/CD setup"

# Push
Write-Host "5. Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host '=== Complete ===' -ForegroundColor Green
