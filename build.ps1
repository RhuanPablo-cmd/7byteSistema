$ErrorActionPreference = "Stop"

$root = $PSScriptRoot
$environment = Join-Path $root ".venv-build"
$python = Join-Path $environment "Scripts\python.exe"

if (-not (Test-Path $python)) {
    & py -m venv $environment
    if ($LASTEXITCODE -ne 0) {
        throw "Nao foi possivel criar o ambiente virtual de build."
    }
}

& $python -m pip install -r (Join-Path $root "requirements-build.txt")
if ($LASTEXITCODE -ne 0) {
    throw "Nao foi possivel instalar as dependencias de build."
}

$logoPath = Join-Path $root "img\7byte.png"
$iconPath = Join-Path ([System.IO.Path]::GetTempPath()) (
    "7byteSistema-" + [guid]::NewGuid().ToString() + ".ico"
)

try {
    & $python -c "from PIL import Image; import sys; Image.open(sys.argv[1]).convert('RGBA').save(sys.argv[2], format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])" $logoPath $iconPath
    if ($LASTEXITCODE -ne 0) {
        throw "Nao foi possivel converter o logo para o formato ICO."
    }

    $arguments = @(
        "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name", "7byteSistema",
        "--icon", $iconPath,
        "--add-data", "$root\Telas.ui;Telas.ui",
        "--add-data", "$root\img\7byte.png;img",
        "--add-data", "$root\base_dados\estoque.sql;base_dados",
        "--distpath", (Join-Path $root "dist"),
        "--workpath", (Join-Path $root "build\pyinstaller"),
        "--specpath", (Join-Path $root "build"),
        (Join-Path $root "gestao_estoque\main.py")
    )

    & $python @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "A geracao do executavel falhou."
    }

    Write-Output "Executavel criado em: $(Join-Path $root 'dist\7byteSistema.exe')"
}
finally {
    Remove-Item -LiteralPath $iconPath -Force -ErrorAction SilentlyContinue
}
