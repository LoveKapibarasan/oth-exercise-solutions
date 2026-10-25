#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../data/.env.local"
PSQL="psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE"
PSQL_R="psql -h localhost -p "$PGPORT" -U postgres"

# Backup
BACKUP_DB="${PGDATABASE}_backup"
$PSQL -c "DROP DATABASE IF EXISTS $BACKUP_DB;"
$PSQL -c "CREATE DATABASE $BACKUP_DB WITH TEMPLATE $PGDATABASE;"

echo "Without join."

echo "Ex2-1"
# 1
echo "1. ID and Name of Students taking Comp. Sci."
$PSQL -c "
SELECT DISTINCT s.student_id, s.name
FROM student s
WHERE EXISTS (
    SELECT 1
    FROM takes t
    WHERE t.student_id = s.student_id
    AND EXISTS (
        SELECT 1
        FROM course c
        WHERE c.course_id = t.course_id
        AND c.dept_name = 'Comp. Sci.'
    )
);
"
echo "IN can be also OK."

# 2
echo "2. ID and Name of Students not taking courses before 2017"
$PSQL -c "
SELECT DISTINCT student_id, name
FROM student
WHERE student_id NOT IN (
    SELECT DISTINCT student_id
    FROM takes
    WHERE year < 2017
);
"
echo "NOT EXISTS can be also OK."

# 3, 4
$PSQL -c "
WITH deb_max(debt_name, value) as 
(SELECT debt_name, MAX(salary)
FROM instructor
GROUP BY debt_name;)
SELECT MIN(value) 
FROM deb_max; 
"

# 5
$PSQL -c "
SELECT student_id, course_id
FROM takes
GROUP BY student_id, course_id
COUNT(*) > 3;
"

echo "Ex2-3"
echo "I assume that A is a kind of grade, not one."
$PSQL -c "
WITH a_course(c_id) AS (
	SELECT course_id
	FROM takes AS t
	WHERE t.grade = 'A'
),
a_instructor(i_id) AS (
	SELECT DISTINCT te.ID
	FROM teaches te
	WHERE te.course_id IN (SELECT c_id FROM a_course)
)
SELECT DISTINCT i.ID, i.name
FROM instructor AS i
WHERE i.ID NOT IN (SELECT i_id FROM a_instructor);
"

