param(
    [string]$RepoRoot = ".",
    [string]$Feature = ""
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$detectScript = Join-Path $scriptDir "detect-next-step.ps1"

if (!(Test-Path $detectScript)) {
    $out = [ordered]@{
        current_step = "Unknown"
        current_step_done = $false
        next_step = "Blocked"
        next_command = ""
        can_proceed = $false
        reason = "detect-next-step.ps1 not found"
    }
    $out | ConvertTo-Json -Depth 4 -Compress
    exit 0
}

$detectJson = pwsh -NoProfile -File $detectScript -RepoRoot $RepoRoot -Feature $Feature
$detect = $detectJson | ConvertFrom-Json

$currentStep = "None"
$currentDone = $false
$nextStep = $detect.detected_step
$nextCommand = ""
$canProceed = [bool]$detect.can_proceed
$reason = [string]$detect.reason

switch ($nextStep) {
    "Specify" {
        $currentStep = "None"
        $currentDone = $false
        $nextCommand = "/sp.specify"
    }
    "Plan" {
        $currentStep = "Specify"
        $currentDone = $true
        $nextCommand = "/sp.plan"
    }
    "Tasks" {
        $currentStep = "Plan"
        $currentDone = $true
        $nextCommand = "/sp.tasks"
    }
    "Implement" {
        $currentStep = "Tasks"
        $currentDone = $true
        $nextCommand = "/sp.implement"
    }
    default {
        $currentStep = "Unknown"
        $currentDone = $false
        $nextCommand = ""
    }
}

$message = if ($canProceed -and $nextCommand) {
    "Current step: $currentStep (done: $currentDone). Next step: $nextStep. Proceed with ${nextCommand}?"
} else {
    "Workflow is blocked. $reason"
}

$out = [ordered]@{
    phase = $detect.phase
    branch_type = $detect.branch_type
    active_feature = $detect.active_feature
    current_step = $currentStep
    current_step_done = $currentDone
    next_step = $nextStep
    next_command = $nextCommand
    can_proceed = $canProceed
    missing_artifacts = @($detect.missing_artifacts)
    reason = $reason
    message = $message
}

$out | ConvertTo-Json -Depth 6 -Compress
