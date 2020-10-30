#!/usr/bin/env python3

import sys
import sqlparse


class ColumnDef:
    def __init__(self, name: str):
        self.name = name


class TableDef:
    def __init__(self, name: str):
        self.name = name
        self.columns = []


def add_column(self, column: ColumnDef):
    self.columns.append(column)


def extract_definitions(token_list):
    # assumes that token_list is a parenthesis
    definitions = []
    tmp = []
    par_level = 0
    for token in token_list.flatten():
        if token.is_whitespace:
            continue
        elif token.match(sqlparse.tokens.Punctuation, '('):
            par_level += 1
            continue
        if token.match(sqlparse.tokens.Punctuation, ')'):
            if par_level == 0:
                break
            else:
                par_level -= 1
        elif token.match(sqlparse.tokens.Punctuation, ','):
            if tmp:
                definitions.append(tmp)
            tmp = []
        else:
            tmp.append(token)
    if tmp:
        definitions.append(tmp)
    return definitions


def is_garbage(token):
    return (token.is_whitespace or token.ttype is sqlparse.tokens.Comment.Single)


def is_create_table(statement):
    tokens = [t for t in statement.flatten() if not is_garbage(t)]
    return tokens[0].match(sqlparse.tokens.DDL, 'CREATE') and tokens[1].match(sqlparse.tokens.Keyword, 'TABLE')


# def dequote(s):
#     return s.replace('`', '')


# def arrange_column_def(column):
#     definition = []
#     first = dequote(column[0].value)

#     if first == 'PRIMARY':
#     else:
#         definition.append

#     definition.append()

#     return definition


def main(argv):
    fo = open(argv[1], 'r')
    parsed = sqlparse.parse(fo.read())
    fo.close()

    for statement in parsed:
        if not is_create_table(statement):
            continue

        _, par = statement.token_next_by(i=sqlparse.sql.Parenthesis)

        print(statement)

        columns = extract_definitions(par)

        # for column in columns:
            # print(arrange_column_def(column))
            # print('{name}\t{definition}'.format(
                # name=column[0], definition=' / '.join(str(t) for t in column[1:])))


if __name__ == '__main__':
    main(sys.argv)
