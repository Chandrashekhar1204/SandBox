:: This file is used to build the example applications using the sandbox-sdk.

@echo off
setlocal EnableDelayedExpansion

::----------------------------------------------------------------------------------------------------------------------------
:: Bootstrap a python virtualenv containing some required utility tools
::----------------------------------------------------------------------------------------------------------------------------
call sandbox-sdk\tools\bootstrap_virtualenv.bat

:: Call SCons for building the example applications
call scons --site-dir sandbox-sdk\tools\site_scons %*

:exit