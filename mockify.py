#!/usr/bin/env python3 -B

# Copyright (c) 2015, Marco Molteni.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Simple script to generate a skeleton mock file and function for CppUMock.
It expects to be run in the directory containing the mocks.
"""


import sys
import os.path

from pycparser import c_parser, c_ast


FILE_HEADER = '''
// autogenerated by mockify.py

extern "C" {
#include "@include@"
}

'''

VOID_MOCK = '''
{return_type} {function}({args}) {{
    mock().actualCall("{function}");
}}'''.lstrip("\n")

NON_VOID_MOCK = '''
{return_type} {function}({args}) {{
    mock().actualCall("{function}");
    if mock().hasReturnValue() {{
        return mock().{return_value};
    }}
    return WRITEME;
}}'''.lstrip("\n")


class MockError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def main(args):
    if len(args) != 2:
        print("Usage: mockify mock_file mock_prototype")
        sys.exit(1)
    mock_filename = "{0}_mock.cpp".format(args[0])
    include_filename = "{0}.h".format(args[0])
    mock_prototype = args[1]
    print("working directory: " + os.getcwd())
    print("mock_filename: " + mock_filename)
    print("include_filename: " + include_filename)
    print("mock_prototype: " + mock_prototype)
    if os.path.exists(mock_filename):
        print("Mock file exists")
        mock_file = open(mock_filename, "a")
    else:
        print("Creating mock file")
        mock_file = open(mock_filename, "w")
        write_header(mock_file, FILE_HEADER, include_filename)
    add_mock_function(mock_file, mock_prototype)
    mock_file.close()


def write_header(file, header, include):
    print("Adding file header")
    header = header.replace("@include@", include)
    file.write(header)


def add_mock_function(file, prototype):
    print("Adding mock function")
    # TODO: parse file to see if mock function is already there...
    try:
        mock_function = generate_mock_boilerplate(prototype)
        file.write("\n" + mock_function + "\n")
    except MockError as e:
        print("Error: " + e.value)


def generate_mock_boilerplate(prototype):
    # Thanks to cdecl.py from pycparser

    parser = c_parser.CParser()
    try:
        ast = parser.parse(prototype)
    except c_parser.ParseError:
        e = sys.exc_info()[1]
        raise MockError("Parse error:" + str(e))
    decl = ast.ext[-1]
    if not isinstance(decl, c_ast.Decl):
        raise MockError("Not a valid declaration: " + prototype)
    # decl.show(); print("")

    if not isinstance(decl.type, c_ast.FuncDecl):
        raise MockError("Not a function declaration: " + prototype)

    # storage is, for example, "static" in "static void f();"
    if decl.storage:
        storage = ' '.join(decl.storage)
        raise MockError("Cannot mock a function with storage: " + storage)

    func_decl = decl.type
    function_name = decl.name

    pointer = False
    if isinstance(func_decl.type, c_ast.PtrDecl):
        # void* f(); =>
        # Decl: f, [], [], []
        #   FuncDecl:
        #     PtrDecl: []                   <== here
        #       TypeDecl: f, []
        #         IdentifierType: ['void']
        type_decl = func_decl.type.type
        pointer = True
    elif isinstance(func_decl.type, c_ast.TypeDecl):
        # void f(); =>
        # Decl: f, [], [], []
        #   FuncDecl:
        #     TypeDecl: f, []               <== here
        #       IdentifierType: ['void']
        type_decl = func_decl.type
    else:
        raise MockError("Internal error parsing: " + prototype)

    identifier_type = type_decl.type

    # e.g.: "int" in "int f()"
    type_name = ' '.join(identifier_type.names)
    if pointer:
        type_name += '*'
    # e.g.: "const" in "const char* f()"
    if len(type_decl.quals) > 0:
        type_name = type_decl.quals[0] + " " + type_name

    if func_decl.args:
        func_decl.args.show()

    return_values = {
        # All the return values supported by CppUMock.
        'int':               'intReturnValue()',
        'unsigned int':      'unsignedIntReturnValue()',
        'long int':          'longIntReturnValue()',
        'unsigned long int': 'unsignedLongIntReturnValue()',
        'const char*':       'stringReturnValue()',
        'double':            'doubleReturnValue()',
        'void*':             'pointerReturnValue()',
        'const void*':       'constPointerReturnValue()',

        # Synthetic case
        'char*':             'pointerReturnValue()',
    }

    if type_name == 'void':
        mock = VOID_MOCK.format(
            return_type=type_name,
            function=function_name,
            args="")
    elif type_name in return_values:
        mock = NON_VOID_MOCK.format(
            return_type=type_name,
            function=function_name,
            args="",
            return_value=return_values[type_name])
    else:
        raise MockError("Internal error, cannot handle: {0} [{1}]".format(
            prototype, type_name))

    return mock

    # "withParameters" can only use int, double, const char* or const void*
    # void f(int i, const char* p); =>
    # void f(int i, const char* p) {
    #     mock().actualCall("f")
    #         .withParameter("i", i)
    #         .withParameter("p", p);
    # }
    #
    # Output parameters:
    #
    # void Foo(int *bar)
    # {
    #     mock().actualCall("foo").
    #         withOutputParameter("bar", bar);
    # }


if __name__ == "__main__":
    main(sys.argv[1:])
