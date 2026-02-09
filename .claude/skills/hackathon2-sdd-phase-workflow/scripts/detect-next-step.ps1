param(
    [string]$RepoRoot = ".",
    [string]$Feature = ""
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    param([string]$Start)
    try {
        $root = git -C $Start rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0 -and $root) {
            return $root.Trim()
        }
    } catch {}
    return (Resolve-Path $Start).Path
}

function Get-CurrentBranch {
    param([string]$Root)
    try {
        $branch = git -C $Root branch --show-current 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $branch.Trim()
        }
    } catch {}
    return ""
}

function Get-ActiveFeature {
    param(
        [string]$Root,
        [string]$Branch,
        [string]$ExplicitFeature
    )
    if ($ExplicitFeature) {
        return $ExplicitFeature
    }

    $specsDir = Join-Path $Root "specs"
    if ($Branch -match '^[0-9]{3}-[a-z0-9-]+$') {
        $candidate = Join-Path $specsDir $Branch
        if (Test-Path $candidate) {
            return $Branch
        }
    }

    if (!(Test-Path $specsDir)) {
        return ""
    }

    $dirs = Get-ChildItem -Path $specsDir -Directory | Sort-Object Name
    if ($dirs.Count -eq 1) {
        return $dirs[0].Name
    }

    if ($dirs.Count -gt 1) {
        $latest = $dirs |
            Where-Object { $_.Name -match '^[0-9]{3}-' } |
            Sort-Object Name -Descending |
            Select-Object -First 1
        if ($latest) {
            return $latest.Name
        }
    }

    return ""
}

$root = Get-RepoRoot -Start $RepoRoot
$branch = Get-CurrentBranch -Root $root
$branchType = "invalid"
$phase = "phase1"

if ($branch -match '^phase([1-5])$') {
    $branchType = "phase"
    $phase = "phase$($Matches[1])"
} elseif ($branch -match '^[0-9]{3}-[a-z0-9-]+$') {
    $branchType = "feature"
    # Current default assumption from project plan: feature branches map to Phase 1 unless
    # phase context is explicitly set elsewhere.
    $phase = "phase1"
}

$activeFeature = Get-ActiveFeature -Root $root -Branch $branch -ExplicitFeature $Feature
$missing = New-Object System.Collections.Generic.List[string]
$detectedStep = "Blocked"
$reason = ""
$canProceed = $false

if ($branchType -eq "invalid") {
    $reason = "Current branch is not a valid phase branch or feature branch."
    $missing.Add("valid branch context")
} elseif (-not $activeFeature) {
    $reason = "Active feature could not be resolved under specs/<feature>."
    $missing.Add("active feature directory")
} else {
    $featureDir = Join-Path (Join-Path $root "specs") $activeFeature
    $specPath = Join-Path $featureDir "spec.md"
    $planPath = Join-Path $featureDir "plan.md"
    $tasksPath = Join-Path $featureDir "tasks.md"

    if (!(Test-Path $specPath)) {
        $detectedStep = "Specify"
        $missing.Add("spec.md")
        $reason = "Specification artifact is missing."
        $canProceed = $true
    } elseif (!(Test-Path $planPath)) {
        $detectedStep = "Plan"
        $missing.Add("plan.md")
        $reason = "Plan artifact is missing."
        $canProceed = $true
    } elseif (!(Test-Path $tasksPath)) {
        $detectedStep = "Tasks"
        $missing.Add("tasks.md")
        $reason = "Tasks artifact is missing."
        $canProceed = $true
    } else {
        $detectedStep = "Implement"
        $reason = "All prerequisite artifacts exist for implementation stage."
        $canProceed = $true
    }
}

$result = [ordered]@{
    phase = $phase
    branch_type = $branchType
    active_feature = $activeFeature
    detected_step = $detectedStep
    missing_artifacts = @($missing)
    reason = $reason
    can_proceed = $canProceed
}

$result | ConvertTo-Json -Depth 4 -Compress
