#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

source "${SCRIPT_DIR}/../Hasura/.env"
source "${SCRIPT_DIR}/../Hasura/hasura_util.sh"

echo "Ex2-1"
# 1
CS_QUERY='
query { 
  student(where: {takes: {course: {dept_name: {_eq: "Comp. Sci."}}}}) { 
    student_id 
    name 
  } 
}
'
query_hasura "$CS_QUERY"

# 2
Y_QUERY='
query {
  student(where: {
    _not: {
      takes: {
        year: { _lt: 2017 }
      }
    }
  }) {
    student_id
    name
  }
}
'
query_hasura "$Y_QUERY"

# 3 4

echo "No nested aggregate function."
S_QUERY='
query {
  instructor_aggregate(group_by: [dept_name]) {
    group_by {
      dept_name
    }
    aggregate {
      max {
        salary
      }
    }
  }
}
'
query_hasura "$S_Query" | jq '.data.instructor_aggregate[].aggregate.max.salary |  min'

# 5
T_QUERY='
query {
  takes_aggregate(group_by: [student_id, course_id]) {
    group_by {
      student_id
      course_id
    }
    aggregate {
      count
    }
  }
}
'
query_hasura "$T_QUERY" | jq '.data.takes_aggregate
|  map(select(.aggregate.count >= 3)'


echo "Ex2-3"
A_QUERY='
query {
  instructor(where: {
    _not: {
      teaches: {
        takes: {
          grade: { _eq: "A" }
        }
      }
    }
  }) {
    ID
    name
  }
}
'

query_hasura "$A_QUERY"
