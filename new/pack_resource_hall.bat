@echo off

SET CUR_DIR=%~dp0

cd "%CUR_DIR%..\.."

SET S=./res/new/hall/
@echo "原始文件目录：" + %S%

SET F=./src/new/hall/InitHallResource.js
@echo "需要写人的文件" + %F%


START /B python %CUR_DIR%pack_resource.py %S% %F%

pause