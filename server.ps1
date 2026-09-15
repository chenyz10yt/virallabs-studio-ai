# Viral Labs - Native PowerShell HTTP Server
# Runs without Node.js or Python using .NET HttpListener
$port = 8080
$prefix = "http://localhost:$port/"
$baseDir = $PSScriptRoot

if (-not $baseDir) {
    $baseDir = (Get-Location).Path
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($prefix)

try {
    $listener.Start()
    Write-Host "========================================================="
    Write-Host "  VIRAL LABS - SERVIDOR LOCAL EN VIVO ACTIVO"
    Write-Host "  URL: $prefix"
    Write-Host "  Fanpage: http://localhost:$port/fanpage.html"
    Write-Host "========================================================="
} catch {
    # If 8080 is in use, try 8081
    $port = 8081
    $prefix = "http://localhost:$port/"
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add($prefix)
    $listener.Start()
    Write-Host "Iniciado en puerto alternativo: $prefix"
}

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".png"  = "image/png"
    ".svg"  = "image/svg+xml"
    ".ico"  = "image/x-icon"
}

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        $rawUrl = $request.Url.AbsolutePath.TrimStart('/')
        if ([string]::IsNullOrWhiteSpace($rawUrl)) {
            $rawUrl = "index.html"
        }

        # URL decode
        $decodedUrl = [System.Uri]::UnescapeDataString($rawUrl)
        $filePath = Join-Path $baseDir $decodedUrl

        if (Test-Path $filePath -PathType Leaf) {
            $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
            $contentType = $mimeTypes[$ext]
            if (-not $contentType) { $contentType = "application/octet-stream" }

            $response.ContentType = $contentType
            $response.AddHeader("Access-Control-Allow-Origin", "*")
            $response.AddHeader("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
            $response.AddHeader("Pragma", "no-cache")
            $response.AddHeader("Expires", "0")

            $bytes = [System.IO.File]::ReadAllBytes($filePath)
            $response.ContentLength64 = $bytes.Length
            $response.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
            $response.StatusCode = 404
            $msg = [System.Text.Encoding]::UTF8.GetBytes("<h1>404 - Archivo no encontrado en Viral Labs</h1>")
            $response.ContentLength64 = $msg.Length
            $response.OutputStream.Write($msg, 0, $msg.Length)
        }
        $response.OutputStream.Close()
    } catch {
        # Catch individual request errors and keep server running
    }
}
