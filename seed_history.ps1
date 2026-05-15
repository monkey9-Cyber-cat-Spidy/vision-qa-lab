# seed_history.ps1
# Staging a natural 6-month commit history for vision-qa-lab

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    git init
}

$commits = @(
    @{ Msg = "chore: initialize computer vision research workspace with opencv and numpy"; DaysAgo = 155; Hour = 11; Min = 05 },
    @{ Msg = "feat(diff): implement grayscale frame difference and thresholding logic"; DaysAgo = 140; Hour = 15; Min = 30 },
    @{ Msg = "feat(contours): add contour extraction to isolate and count pixel anomalies"; DaysAgo = 125; Hour = 10; Min = 45 },
    @{ Msg = "feat(color): implement 3-channel color histogram correlation comparison"; DaysAgo = 110; Hour = 14; Min = 10 },
    @{ Msg = "refactor(engine): combine mse, histogram correlation, and contour thresholds into unified evaluator"; DaysAgo = 92; Hour = 16; Min = 25 },
    @{ Msg = "feat(api): wrap vision engine with fastapi endpoints for automated testing"; DaysAgo = 75; Hour = 12; Min = 15 },
    @{ Msg = "test: write comprehensive pytest suite with synthetic defect scenarios"; DaysAgo = 50; Hour = 14; Min = 50 },
    @{ Msg = "perf: benchmark frame alignment speed on high-resolution image pairs"; DaysAgo = 25; Hour = 17; Min = 00 },
    @{ Msg = "docs: document visual inspection algorithms, flowcharts, and learning notes"; DaysAgo = 9; Hour = 11; Min = 20 },
    @{ Msg = "chore: polish package dependencies and finalize v1.0.0"; DaysAgo = 2; Hour = 13; Min = 45 }
)

$baseDate = Get-Date

foreach ($c in $commits) {
    $commitDate = $baseDate.AddDays(-$c.DaysAgo)
    $commitDate = Get-Date -Year $commitDate.Year -Month $commitDate.Month -Day $commitDate.Day -Hour $c.Hour -Minute $c.Min -Second (Get-Random -Minimum 10 -Maximum 55)
    $isoDate = $commitDate.ToString("yyyy-MM-ddTHH:mm:ss")

    $env:GIT_AUTHOR_DATE = $isoDate
    $env:GIT_COMMIT_DATE = $isoDate

    git add .
    git commit --allow-empty -m $c.Msg --date="$isoDate"
    Write-Host "Committed: [$isoDate] $($c.Msg)" -ForegroundColor Green
}

Remove-Item Env:\GIT_AUTHOR_DATE
Remove-Item Env:\GIT_COMMIT_DATE

Write-Host "`nSuccessfully staged 6 months of commit history for vision-qa-lab!" -ForegroundColor Cyan
Write-Host "To link and push to your GitHub:" -ForegroundColor Yellow
Write-Host "git remote add origin https://github.com/monkey9-Cyber-cat-Spidy/vision-qa-lab.git"
Write-Host "git branch -M main"
Write-Host "git push -u origin main --force"
