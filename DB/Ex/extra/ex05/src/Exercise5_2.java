/*
a)We need to know
0: The number of attributes.
(1: The type of each attribute)
2: The name of each attribute
[ How to get ]
Object attribute = result.getObject(i);
attribute.toString();
b)
ResultSetMetaData rsmd = result.getMetaData();
int numAttributes = rsmd.getColumnCount();
String attrName = rsmd.getColumnName(i);

 */

public class Exercise5_2 {
}
