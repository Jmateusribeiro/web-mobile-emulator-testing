set dir=%CD%
set test_dir=%CD%\tests

set browser=Chrome

echo The test directory is %test_dir%
echo Running tests with browser: %browser%

python -m pytest "%test_dir%" --Browser=%browser% --driver=%browser%

pause