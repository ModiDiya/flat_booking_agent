Write-Host '=== CI/CD Pipeline Verification ===' -ForegroundColor Cyan

Write-Host '1. Git Status:' -ForegroundColor Yellow
git status

Write-Host '2. Docker Build Test:' -ForegroundColor Yellow
docker build -t booking-ai-agent . 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host '   ✓ Docker build successful' -ForegroundColor Green
} else {
    Write-Host '   ✗ Docker build failed' -ForegroundColor Red
    exit 1
}

Write-Host '3. Basic Container Tests:' -ForegroundColor Yellow
$basicTests = @(
    'python --version',
    'python -c \"import flask; print(\\\"✓ Flask imported\\\")\"',
    'python -c \"import sys; print(\\\"Python path:\\\", sys.path)\"'
)

foreach ($test in $basicTests) {
    docker run --rm booking-ai-agent $test 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host \"   ✓ $test\" -ForegroundColor Green
    } else {
        Write-Host \"   ✗ $test\" -ForegroundColor Red
    }
}

Write-Host '4. Application Structure Test:' -ForegroundColor Yellow
docker run --rm booking-ai-agent ls -la backend/ 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host '   ✓ Application files exist' -ForegroundColor Green
} else {
    Write-Host '   ✗ Application files missing' -ForegroundColor Red
}

Write-Host '5. Application Import Test:' -ForegroundColor Yellow
docker run --rm booking-ai-agent python -c \"
try:
    from backend.app import app
    print('✓ App imported successfully')
    exit(0)
except Exception as e:
    print('✗ App import failed:', e)
    exit(1)
\" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host '   ✓ Application imports correctly' -ForegroundColor Green
} else {
    Write-Host '   ✗ Application import failed' -ForegroundColor Red
}

Write-Host '6. Application Startup Test:' -ForegroundColor Yellow
$containerId = docker run -d -p 5000:5000 --name test-app booking-ai-agent
Start-Sleep -Seconds 5

$isRunning = docker ps --filter \"name=test-app\" --filter \"status=running\" --quiet
if ($isRunning) {
    Write-Host '   ✓ Application container is running' -ForegroundColor Green
    
    # Test health endpoint
    try {
        $response = Invoke-WebRequest -Uri \"http://localhost:5000/health\" -UseBasicParsing -TimeoutSec 5
        if ($response.Content -like '*healthy*') {
            Write-Host '   ✓ Application health check passed' -ForegroundColor Green
        } else {
            Write-Host '   ✗ Application health check failed' -ForegroundColor Yellow
        }
    } catch {
        Write-Host \"   ⚠ Health endpoint not accessible: $($_.Exception.Message)\" -ForegroundColor Yellow
    }
} else {
    Write-Host '   ✗ Application container failed to start' -ForegroundColor Red
    docker logs test-app
}

# Cleanup
docker stop test-app 2>&1 | Out-Null
docker rm test-app 2>&1 | Out-Null

Write-Host '=== VERIFICATION COMPLETE ===' -ForegroundColor Cyan
Write-Host 'Check GitHub Actions for full CI/CD pipeline status' -ForegroundColor White
