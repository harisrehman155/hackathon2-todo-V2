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

function Resolve-Feature {
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

    if (Test-Path $specsDir) {
        $latest = Get-ChildItem $specsDir -Directory |
            Where-Object { $_.Name -match '^[0-9]{3}-' } |
            Sort-Object Name -Descending |
            Select-Object -First 1
        if ($latest) {
            return $latest.Name
        }
    }

    return ""
}

function Add-Missing {
    param(
        [System.Collections.Generic.List[string]]$List,
        [string]$Item
    )
    if (-not $List.Contains($Item)) {
        $List.Add($Item)
    }
}

$root = Get-RepoRoot -Start $RepoRoot
$branch = Get-CurrentBranch -Root $root
$phase = "phase1"
$status = "incomplete"
$missing = New-Object System.Collections.Generic.List[string]

$gates = [ordered]@{
    spec_gate = "fail"
    plan_gate = "fail"
    tasks_gate = "fail"
    implementation_gate = "fail"
    pytest_gate = "fail"
    evidence_gate = "fail"
}

if (!($branch -match '^phase([1-5])$' -or $branch -match '^[0-9]{3}-[a-z0-9-]+$')) {
    $status = "blocked"
    Add-Missing -List $missing -Item "valid phase/feature branch context"
} elseif ($branch -match '^phase([1-5])$') {
    $phase = "phase$($Matches[1])"
} else {
    $phase = "phase1"
}

if ($status -ne "blocked" -and $phase -ne "phase1") {
    $status = "blocked"
    Add-Missing -List $missing -Item "phase1 context required for strict phase completion checker"
}

$featureName = Resolve-Feature -Root $root -Branch $branch -ExplicitFeature $Feature
if ($status -ne "blocked" -and -not $featureName) {
    $status = "blocked"
    Add-Missing -List $missing -Item "active feature under specs/"
}

if ($status -ne "blocked") {
    $featureDir = Join-Path (Join-Path $root "specs") $featureName
    $specPath = Join-Path $featureDir "spec.md"
    $planPath = Join-Path $featureDir "plan.md"
    $tasksPath = Join-Path $featureDir "tasks.md"
    $reqChecklist = Join-Path $featureDir "checklists\\requirements.md"
    $phaseChecklist = Join-Path $featureDir "checklists\\phase-completion.md"

    # spec gate
    if ((Test-Path $specPath) -and (Test-Path $reqChecklist)) {
        $gates.spec_gate = "pass"
    } else {
        Add-Missing -List $missing -Item "spec.md and requirements checklist"
    }

    # plan gate
    if (Test-Path $planPath) {
        $planText = Get-Content $planPath -Raw
        if ($planText -match 'Constitution Check') {
            $gates.plan_gate = "pass"
        } else {
            Add-Missing -List $missing -Item "plan.md missing Constitution Check section"
        }
    } else {
        Add-Missing -List $missing -Item "plan.md"
    }

    # tasks gate
    if (Test-Path $tasksPath) {
        $tasksText = Get-Content $tasksPath -Raw
        if (($tasksText -match '\[US[0-9]+\]') -and ($tasksText -match 'pytest')) {
            $gates.tasks_gate = "pass"
        } else {
            Add-Missing -List $missing -Item "tasks.md missing story mapping or pytest task coverage"
        }
    } else {
        Add-Missing -List $missing -Item "tasks.md"
    }

    # implementation gate
    $srcDir = Join-Path $root "src"
    if (Test-Path $srcDir) {
        $pyFiles = Get-ChildItem $srcDir -Recurse -Filter *.py -ErrorAction SilentlyContinue
        if ($pyFiles.Count -gt 0) {
            $allText = ($pyFiles | ForEach-Object { Get-Content $_.FullName -Raw }) -join "`n"
            $keywords = @("add", "update", "delete", "complete", "list")
            $hitCount = ($keywords | Where-Object { $allText -match $_ }).Count
            if ($hitCount -ge 4) {
                $gates.implementation_gate = "pass"
            } else {
                Add-Missing -List $missing -Item "source implementation does not cover all core Phase I actions"
            }
        } else {
            Add-Missing -List $missing -Item "python source files under src/"
        }
    } else {
        Add-Missing -List $missing -Item "src/ implementation directory"
    }

    # pytest gate
    $testsDir = Join-Path $root "tests"
    $pytestEvidence = Join-Path $featureDir "checklists\\pytest-evidence.md"
    if ((Test-Path $testsDir) -and (Get-ChildItem $testsDir -Recurse -Filter "test_*.py" -ErrorAction SilentlyContinue)) {
        if (Test-Path $pytestEvidence) {
            $evText = Get-Content $pytestEvidence -Raw
            if ($evText -match '(?i)pass|passed') {
                $gates.pytest_gate = "pass"
            } else {
                Add-Missing -List $missing -Item "pytest evidence exists but does not indicate passing run"
            }
        } else {
            Add-Missing -List $missing -Item "pytest evidence checklist (checklists/pytest-evidence.md)"
        }
    } else {
        Add-Missing -List $missing -Item "tests with pytest naming under tests/"
    }

    # evidence gate
    if (Test-Path $phaseChecklist) {
        $phaseText = Get-Content $phaseChecklist -Raw
        if (($phaseText -match '- \[x\]') -and -not ($phaseText -match '- \[ \]')) {
            $gates.evidence_gate = "pass"
        } else {
            Add-Missing -List $missing -Item "phase completion checklist has open items"
        }
    } else {
        Add-Missing -List $missing -Item "phase completion checklist (checklists/phase-completion.md)"
    }
}

if ($status -ne "blocked") {
    if (($gates.spec_gate -eq "pass") -and
        ($gates.plan_gate -eq "pass") -and
        ($gates.tasks_gate -eq "pass") -and
        ($gates.implementation_gate -eq "pass") -and
        ($gates.pytest_gate -eq "pass") -and
        ($gates.evidence_gate -eq "pass")) {
        $status = "complete"
        $recommendation = "self_test"
    } else {
        $status = "incomplete"
        $recommendation = "fix_blockers"
    }
} else {
    $recommendation = "fix_blockers"
}

$result = [ordered]@{
    phase = $phase
    status = $status
    gates = $gates
    missing_items = @($missing)
    recommendation = $recommendation
}

$result | ConvertTo-Json -Depth 6 -Compress
