Write-Host '=== Complete Docker CI/CD Verification ===' -ForegroundColor Cyan

# 1. Check all files exist
Write-Host '1. File Structure Check:' -ForegroundColor Yellow
$files = @(
    'backend/app.py',
    'requirements.txt', 
    'Dockerfile',
    '.github/workflows/docker-ci.yml',
    'backend/tests/test_basic.py'
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host \"   ✓ $file\" -ForegroundColor Green
    } else {
        Write-Host \"   ✗ Missing: $file\" -ForegroundColor Red
    }
}

# 2. Test Python code syntax
Write-Host '2. Python Syntax Check:' -ForegroundColor Yellow
try {
    $output = python -m py_compile backend/app.py 2>&1
    Write-Host '   ✓ backend/app.py syntax valid' -ForegroundColor Green
} catch {
    Write-Host '   ✗ backend/app.py has syntax errors' -ForegroundColor Red
}

# 3. Test requirements
Write-Host '3. Requirements Check:' -ForegroundColor Yellow
if (Test-Path 'requirements.txt') {
    $reqs = Get-Content 'requirements.txt'
    if ($reqs.Count -gt 0) {
        Write-Host \"   ✓ requirements.txt has $($reqs.Count) packages\" -ForegroundColor Green
    } else {
        Write-Host '   ✗ requirements.txt is empty' -ForegroundColor Red
    }
}

# 4. Docker build
Write-Host '4. Docker Build Test:' -ForegroundColor Yellow
docker build -t booking-ai-agent . 2>&1 | Out-Host
if ($LASTEXITCODE -eq 0) {
    Write-Host '   ✓ Docker build successful' -ForegroundColor Green
} else {
    Write-Host '   ✗ Docker build failed' -ForegroundColor Red
    exit 1
}

# 5. Container tests
Write-Host '5. Container Tests:' -ForegroundColor Yellow
$tests = @(
    @{Name='Python Version'; Command='python --version'},
    @{Name='Flask Import'; Command='python -c \"import flask; print(\\\"✓ Flask works\\\")\"'},
    @{Name='Pytest'; Command='python -m pytest backend/tests/ -v'}
)

foreach ($test in $tests) {
    docker run --rm booking-ai-agent $test.Command 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host \"   ✓ $($test.Name)\" -ForegroundColor Green
    } else {
        Write-Host \"   ✗ $($test.Name)\" -ForegroundColor Red
    }
}

Write-Host '=== All Checks Completed ===' -ForegroundColor Cyan
Write-Host 'Next: git add . && git commit -m \"Complete Docker setup\" && git push' -ForegroundColor White
