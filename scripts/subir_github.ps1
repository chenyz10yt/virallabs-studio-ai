[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
[System.Net.ServicePointManager]::DefaultConnectionLimit = 20
[System.Net.ServicePointManager]::MaxServicePointIdleTime = 2000
$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   VIRAL LABS STUDIO AI - SINCRONIZADOR CON GITHUB        " -ForegroundColor White
Write-Host "   Destino: https://github.com/chenyz10yt/virallabs-studio-ai " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

$username = "chenyz10yt"
$repoName = "virallabs-studio-ai"

# 1. Solicitar o leer Token de GitHub
$Token = ""
$tokenFile = "C:\Users\Admin\.gemini\github_token.txt"
if (Test-Path $tokenFile) {
    $Token = (Get-Content $tokenFile -Raw).Trim()
}

if ([string]::IsNullOrWhiteSpace($Token)) {
    Write-Host "Para conectar con tu cuenta @$username necesitas tu Personal Access Token (ghp_...):" -ForegroundColor Yellow
    Write-Host "Si no lo tienes a mano, crealo en 30 segundos en:" -ForegroundColor Gray
    Write-Host "👉 https://github.com/settings/tokens/new?scopes=repo&description=ViralLabs" -ForegroundColor Cyan
    Write-Host ""
    $secToken = Read-Host -Prompt "Pega tu Token de GitHub (ghp_...)" -AsSecureString
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secToken)
    $Token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
}

if ([string]::IsNullOrWhiteSpace($Token)) {
    Write-Host "Error: No se proporciono un Token valido." -ForegroundColor Red
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $Token"
    "User-Agent"    = "ViralLabs-Uploader"
    "Accept"        = "application/vnd.github+json"
}

# 2. Verificar credenciales con GitHub
Write-Host "`n[1/4] Autenticando con GitHub..." -ForegroundColor Cyan
try {
    $userInfo = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -Method Get -TimeoutSec 15
    Write-Host " [OK] Autenticado exitosamente como: @$($userInfo.login)" -ForegroundColor Green
    $username = $userInfo.login
} catch {
    Write-Host " [ERROR] El token no es valido o ha expirado: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Guardar token localmente para futuras subidas comodas
try {
    $Token | Out-File -FilePath $tokenFile -Force
    Write-Host " Token guardado localmente de forma segura para proximas sincronizaciones." -ForegroundColor DarkGray
} catch {}

# 3. Crear o verificar el repositorio
Write-Host "`n[2/4] Verificando repositorio '$repoName'..." -ForegroundColor Cyan
$repoExists = $false
try {
    $repo = Invoke-RestMethod -Uri "https://api.github.com/repos/$username/$repoName" -Headers $headers -Method Get -TimeoutSec 15
    Write-Host " [OK] El repositorio ya existe. Procediendo a sincronizar..." -ForegroundColor Green
    $repoExists = $true
} catch {
    Write-Host " El repositorio no existe aun. Creandolo en tu cuenta..." -ForegroundColor Yellow
    $body = @{
        name        = $repoName
        description = "Viral Labs Studio v3.0 AI - Creator OS, Faceless Channels & Multi-Platform Engine"
        private     = $false
        auto_init   = $true
    } | ConvertTo-Json

    try {
        $created = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body -ContentType "application/json" -TimeoutSec 20
        Write-Host " [OK] Repositorio creado exitosamente: https://github.com/$username/$repoName" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } catch {
        Write-Host " [ERROR] Fallo al crear repositorio: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# 4. Subir todos los archivos del proyecto
Write-Host "`n[3/4] Escaneando y subiendo archivos del proyecto..." -ForegroundColor Cyan
$baseDir = Split-Path -Parent $PSScriptRoot
if (!(Test-Path (Join-Path $baseDir "index.html"))) {
    $baseDir = "c:\Users\Admin\Desktop\chenyz.app\web y app"
}

$filesToUpload = Get-ChildItem -Path $baseDir -Recurse -File | Where-Object {
    $_.FullName -notmatch '\\\.git\\' -and
    $_.FullName -notmatch '\\node_modules\\' -and
    $_.FullName -notmatch '\\\.gemini\\'
}

$total = $filesToUpload.Count
$count = 0
$failedFiles = @()

foreach ($file in $filesToUpload) {
    $count++
    $relPath = $file.FullName.Substring($baseDir.Length).TrimStart('\').Replace('\', '/')
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $b64 = [Convert]::ToBase64String($bytes)

    # Obtener SHA si ya existe
    $sha = $null
    try {
        $existing = Invoke-RestMethod -Uri "https://api.github.com/repos/$username/$repoName/contents/$relPath" -Headers $headers -Method Get -TimeoutSec 10 -ErrorAction SilentlyContinue
        if ($existing -and $existing.sha) {
            $sha = $existing.sha
        }
    } catch {}

    $bodyObj = @{
        message = "Viral Labs Sync: $relPath"
        content = $b64
        branch  = "main"
    }
    if ($sha) {
        $bodyObj["sha"] = $sha
    }

    $jsonBody = $bodyObj | ConvertTo-Json
    $uploaded = $false

    for ($attempt = 1; $attempt -le 3; $attempt++) {
        try {
            $upload = Invoke-RestMethod -Uri "https://api.github.com/repos/$username/$repoName/contents/$relPath" -Headers $headers -Method Put -Body $jsonBody -ContentType "application/json" -TimeoutSec 20
            Write-Host " [$count/$total] [SUBIDO] $relPath" -ForegroundColor Green
            $uploaded = $true
            break
        } catch {
            Write-Host "   Intento $attempt ($relPath): $($_.Exception.Message)" -ForegroundColor DarkYellow
            Start-Sleep -Milliseconds 800
        }
    }

    if (-not $uploaded) {
        Write-Host " [$count/$total] [ERROR] $relPath : No se pudo subir tras 3 intentos." -ForegroundColor Red
        $failedFiles += $relPath
    }

    Start-Sleep -Milliseconds 200
}

Write-Host "`n[4/4] ¡SINCRONIZACION COMPLETA CON EXITO!" -ForegroundColor Green
if ($failedFiles.Count -gt 0) {
    Write-Host " Archivos con error: $($failedFiles.Count)" -ForegroundColor Yellow
} else {
    Write-Host " Todos los $total archivos fueron subidos exitosamente a GitHub." -ForegroundColor Green
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Repositorio: https://github.com/$username/$repoName" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan

try { Start-Process "https://github.com/$username/$repoName" } catch {}
