param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
)

$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$targets = @(
    (Join-Path $RepoRoot "docs\novatech"),
    (Join-Path $RepoRoot "data\retrieval-corpus")
)

$denyRights =
    [System.Security.AccessControl.FileSystemRights]::Write `
    -bor [System.Security.AccessControl.FileSystemRights]::Delete `
    -bor [System.Security.AccessControl.FileSystemRights]::DeleteSubdirectoriesAndFiles
$inheritanceFlags =
    [System.Security.AccessControl.InheritanceFlags]::ContainerInherit `
    -bor [System.Security.AccessControl.InheritanceFlags]::ObjectInherit
$propagationFlags = [System.Security.AccessControl.PropagationFlags]::None

foreach ($target in $targets) {
    $acl = Get-Acl -Path $target
    $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
        $identity,
        $denyRights,
        $inheritanceFlags,
        $propagationFlags,
        [System.Security.AccessControl.AccessControlType]::Deny
    )

    $acl.RemoveAccessRuleAll($rule) | Out-Null
    Set-Acl -Path $target -AclObject $acl

    Write-Output "RULE_REMOVED $target"
}
