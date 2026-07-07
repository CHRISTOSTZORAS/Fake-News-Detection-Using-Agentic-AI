@echo off
set BACKUP_DIR=C:\Users\tzwrakos\.flowise\backups

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

copy C:\Users\tzwrakos\.flowise\database.sqlite "%BACKUP_DIR%\database_BACKUP_%date:/=-%_%time::=-%.sqlite"

echo Flowise database backup completed.
pause