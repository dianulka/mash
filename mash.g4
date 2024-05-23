grammar mash;

program : statement* EOF;

// dodane if_statement | while_statement | for_statement
statement : echo_function | var_declar | assignment | if_statement | while_statement | for_statement;

echo_function : 'echo' (expression | IDENTIFIER);

expression : arithmetic_expression | string_expression | logical_expression | int_expression | IDENTIFIER;

string_expression : STRING;
int_expression: INTEGER;

arithmetic_expression : additive_expression;

additive_expression : multiplicative_expression
                     | additive_expression '+' multiplicative_expression
                     | additive_expression '-' multiplicative_expression;

multiplicative_expression : primary_expression
                           | multiplicative_expression '*' primary_expression
                           | multiplicative_expression '/' primary_expression;

primary_expression : INTEGER
                    | IDENTIFIER
                    | '(' additive_expression ')';

logical_expression : comparison_expression
                    | logical_expression 'and' logical_expression
                    | logical_expression 'or' logical_expression
                    | 'not' logical_expression
                    | '(' logical_expression ')'
                    | 'true'
                    | 'false';

comparison_expression : arithmetic_expression ('<' | '>' | '==' | '!=') arithmetic_expression
                      | IDENTIFIER ('<' | '>' | '==' | '!=') IDENTIFIER;

var_declar : type IDENTIFIER ('=' (expression | IDENTIFIER))? ;

type : 'string_var' | 'int_var';

assignment : IDENTIFIER '=' (expression | IDENTIFIER);

///////////////////////////////////////////////////////
while_statement : 'while' '(' logical_expression ')' '{' statement* '}';

for_statement : 'for' '(' assignment ';' logical_expression ';' assignment ')' '{' statement* '}';

if_statement : 'if' '(' logical_expression ')' '{' statement* '}' elif_block* else_block?;

elif_block : 'elif' '(' logical_expression ')' '{' statement* '}';

else_block : 'else' '{' statement* '}';

/////////////////////////////////////////////////////

INTEGER : [0-9]+;
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*;
STRING : '"' .*? '"';
COMMENT : '#' .*? '\n' -> skip;
WS : [ \t\n\r]+ -> skip;
