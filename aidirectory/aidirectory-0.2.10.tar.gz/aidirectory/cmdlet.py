def cmd():
    text = """
ECHO scoop reset python> run.ps1
ECHO pip install aithermal -q>> run.ps1 
ECHO pip install aithermal -U -q >> run.ps1 
ECHO Write-Output("Creating Structure") >> run.ps1 
ECHO python -m aithermal.runner>> run.ps1 
CLS
@ECHO OFF
SET ThisScriptsDirectory=%~dp0
SET PowerShellScriptPath=%ThisScriptsDirectory%run.ps1
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& '%PowerShellScriptPath%'"

"""
    return text
