﻿# === 設定 ===

$InputDir = ".\input"
$OutputDir = ".\output"
$ContainerWorkDir = "/home/openface-build"
$ContainerProcessedDir = "/home/openface-build/processed"

# === スクリプト自身の場所を基準にパスを構築 ===
$BaseDir = $PSScriptRoot

Write-Host "$ContainerID = $ContainerID"
Write-Host "$ContainerName = $ContainerName"

# === Docker設定を読み込み ===
. "$BaseDir\config.ps1"

Write-Host "Docker: $ContainerName ($ContainerID)"

docker start $ContainerID /bin/bash

function Check-DockerRunning {
    try {
        docker version | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Start-DockerDesktop {
    $dockerProcess = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue
    if (-not $dockerProcess) {
        Write-Host "Docker Desktop is not running. Starting it now..."
        Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
        # 起動完了まで待機（最大60秒）
        for ($i=0; $i -lt 60; $i++) {
            Start-Sleep -Seconds 1
            if (Check-DockerRunning) {
                Write-Host "Docker Desktop has started."
                return $true
            }
        }
        Write-Host "Failed to start Docker Desktop. Please start it manually."
        return $false
    } else {
        Write-Host "Docker Desktop is already running."
        return $true
    }
}

# メイン処理開始
if (-not (Check-DockerRunning)) {
    $started = Start-DockerDesktop
    if (-not $started) {
        exit 1
    }
}

# ここからDockerコマンドを安全に実行可能
Write-Host "Docker environment is ready. Continuing process."

# 例：コンテナ起動
docker start $ContainerID
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start the Docker container."
    exit 1
}

# === 動画ファイル一覧取得 ===
$mp4Files = Get-ChildItem -Path $InputDir -Filter *.mp4

if ($mp4Files.Count -eq 0) {
    Write-Host "No video files found in input folder: $InputDir"
    exit 1
}

# === ホストからコンテナに動画をコピー ===
foreach ($file in $mp4Files) {
    $src = $file.FullName
    $dest = "{0}:{1}" -f $ContainerID, $ContainerWorkDir
    Write-Host "コピー中: $($file.Name)"
    docker cp "$src" "$dest"
}

# === コンテナ内でFeatureExtraction実行 ===
foreach ($file in $mp4Files) {
    $fileName = $file.Name
    $ContainerCmd = "./build/bin/FeatureExtraction -f $ContainerWorkDir/$fileName -au_static"
    Write-Host "prosessing...: $fileName"
    docker exec $ContainerID bash -c "$ContainerCmd"
}

# === 処理結果をホスト側にコピー ===
foreach ($file in $mp4Files) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $csvName = "$baseName.csv"
    $ContainerCsvPath = "$ContainerProcessedDir/$csvName"
    $hostDestPath = Join-Path -Path $OutputDir -ChildPath $csvName
    Write-Host "copying result file...: $csvName"
    $destCsv = "{0}:{1}" -f $ContainerID, $ContainerCsvPath
    docker cp "$destCsv" "$hostDestPath"
}

Write-Host "=== All processing completed successfully ==="