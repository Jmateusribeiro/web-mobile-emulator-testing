set dir=%CD%
set test_dir=%CD%\tests

set browser=Edge

echo The test directory is %test_dir%

python -m pytest "%test_dir%" --Browser="%browser%"

pause