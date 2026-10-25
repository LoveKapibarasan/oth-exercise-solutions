#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../data/.env.local"
PSQL="psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE"
PSQL_R="psql -h localhost -p "$PGPORT" -U postgres"
echo "[DEBUG] PSQL is $PSQL"

BACKUP_DB="${PGDATABASE}_backup"
# Create DB role
$PSQL_R -c "ALTER ROLE $PGUSER CREATEDB;"
$PSQL -c "DROP DATABASE IF EXISTS $BACKUP_DB;"
$PSQL -c "CREATE DATABASE $BACKUP_DB WITH TEMPLATE $PGDATABASE;"

# 1
echo "1. Comp. Sci. courses with 3 credits"
$PSQL -c "
SELECT title 
FROM course 
WHERE dept_name = 'Comp. Sci.' AND credits = 3;
"
echo ""

# 2
echo "2. Students taught by Einstein"
$PSQL -c "
SELECT DISTINCT takes.ID 
FROM takes, instructor, teaches 
WHERE takes.course_id = teaches.course_id 
  AND takes.sec_id = teaches.sec_id 
  AND takes.semester = teaches.semester 
  AND takes.year = teaches.year 
  AND teaches.id = instructor.id 
  AND instructor.name = 'Einstein';
"
echo ""

# 3
echo "3. Highest salary"
$PSQL -c "
SELECT MAX(salary) 
FROM instructor;
"
echo ""

# 4
echo "4. Instructors with highest salary"
$PSQL -c "
SELECT id, name 
FROM instructor 
WHERE salary = (SELECT MAX(salary) FROM instructor);
"
echo ""

# 5
echo "5. Increase Comp. Sci. salary by 10%"
$PSQL -c "
SELECT salary
from instructor
WHERE dept_name = 'Comp. Sci.';
"
echo ""
$PSQL -c "
UPDATE instructor 
SET salary = salary * 1.10 
WHERE dept_name = 'Comp. Sci.';
"
echo ""
$PSQL -c "
SELECT salary
from instructor
WHERE dept_name = 'Comp. Sci.';
"
echo ""

# 6
echo "6. Delete courses never offered"
$PSQL -c "
-- step1: Delete prereq
-- Some cources are not offered but it is prerequisites
DELETE FROM prereq 
WHERE course_id NOT IN (SELECT course_id FROM section)
   OR prereq_id NOT IN (SELECT course_id FROM section);
"
$PSQL -c "
DELETE FROM course 
WHERE course_id NOT IN (SELECT course_id FROM section);
"
echo ""
$PSQL -c "
SELECT course_id 
FROM course 
WHERE course_id NOT IN (SELECT course_id FROM section);
"
echo ""

# 7
echo "7. Promote students to instructors"
echo "Before:"
$PSQL -c "
SELECT COUNT(*) as instructor_count_before 
FROM instructor;
"
# check constraints
echo "====="
$PSQL -c "\d instructor"
# CHECK (salary > 29000) 
echo "====="
$PSQL -c "
INSERT INTO instructor 
SELECT ID, name, dept_name, 29001 
FROM student 
WHERE tot_cred > 100 AND ID NOT IN (SELECT ID FROM instructor); -- To avoid ID duplication 
"
echo ""
echo ”After:”
$PSQL -c "
SELECT COUNT(*) as instructor_count_after 
FROM instructor;
"
# escape into postgre
$PSQL_R -c "DROP DATABASE $PGDATABASE;"
$PSQL_R -c "CREATE DATABASE $PGDATABASE WITH TEMPLATE $BACKUP_DB;"
$PSQL_R -c "DROP DATABASE $BACKUP_DB;"
echo "Database restored"
