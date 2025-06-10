@echo off
setlocal EnableExtensions DisableDelayedExpansion

rem // Comma-separated list of quoted exclusions for directories:
set _DEXCL="node_modules","__pycache__",".vscode",".git"
rem // Comma-separated list of quoted exclusions for files:
set _FEXCL=
set "_FILES=1"// (set to non-empty value to include files as well)

rem // Global ariable indicating current directory level used for indent:
set /A "$LEVEL=0"

set "ITEM=%~1" & rem // (first command line argument specifies root directory)
rem // No root directory has been specified, so use current directory:
if not defined ITEM set "ITEM=."
rem // Check given root directory for existence and quit script if not found:
if not exist "%ITEM%\" exit /B 1 & rem (trailing "\" to not find files)
rem // Check given root directory against wild-cards and quit if some occur:
set "FLAG=#" & for %%J in ("%ITEM%") do if "%%~J"=="%ITEM%" set "FLAG="
if defined FLAG exit /B 1

rem // Process root directory in sub-routine:
call :PROCESS "%ITEM%"

endlocal
exit /B


:PROCESS  val_dir_path
rem // Display name of provided directory:
set "PTH=%~nx1"
setlocal EnableDelayedExpansion
call :INDENT PAD %$LEVEL%
echo(!PAD!!PTH!
endlocal
rem // Increase indent:
set /A "$LEVEL+=1"
rem // Process all sub-directories:
for /D %%D in ("%~1\*") do (
    rem // Check iterated directory against exclusion list:
    set "FLAG="
    for %%E in (%_DEXCL%) do (
        if /I "%%~nxD"=="%%~E" set "FLAG=#"
    )
    rem // Process iterated directory in sub-routine recursively:
    if not defined FLAG (
        call :PROCESS "%%~D"
    )
)
rem // Process all files in case they are to be included:
if defined _FILES (
    for %%F in ("%~1\*.*") do (
        rem // Check iterated file against exclusion list:
        set "FLAG="
        for %%E in (%_FEXCL%) do (
            if /I "%%~nxF"=="%%~E" set "FLAG=#"
        )
        rem // Display name of iterated file:
        if not defined FLAG (
            set "FILE=%%~nxF"
            setlocal EnableDelayedExpansion
            call :INDENT PAD %$LEVEL%
            echo(!PAD!!FILE!
            endlocal
        )
    )
)
rem // Decrease indent:
set /A "$LEVEL-=1"
exit /B


:INDENT  rtn_string  val_number
rem // Build indent string consisting of spaces:
setlocal EnableDelayedExpansion
set "IND="
for /L %%I in (1,1,%~2) do set "IND=!IND!  "
endlocal & set "%~1=%IND%"
exit /B