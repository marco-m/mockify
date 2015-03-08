#!/usr/bin/env python3

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


from mockify import generate_mock_boilerplate
from mockify import MockError
import unittest
import textwrap


class BoilerPlateGeneration(unittest.TestCase):
    def ExpectedMockFromProto(self, mock_function, prototype):
        self.assertEqual(textwrap.dedent(mock_function).strip("\n"),
                         generate_mock_boilerplate(prototype))

    def test_RefuseIncompleteInput(self):
        # Missing ``;`` at end of ``void f()`` is incomplete...
        self.assertRaises(MockError, generate_mock_boilerplate, "void f()")

    def test_RefuseStaticFunctions(self):
        self.assertRaises(MockError, generate_mock_boilerplate,
                          "static void f();")

    def test_RefuseDeclarationsThatAreNotFunctions(self):
        self.assertRaises(MockError, generate_mock_boilerplate, "int i;")

    def test_ParseError(self):
        self.assertRaises(MockError, generate_mock_boilerplate, "foo")

    def test_FunctionNonVoidUnnamedArgument(self):
        self.assertRaises(MockError, generate_mock_boilerplate, "void f(int);")

    def test_IntFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            int f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().intReturnValue();
                }
                return WRITEME;
            }
            """,
            "int f();")

    # We remove the "void" argument because the mock is written in C++,
    # not in C.
    def test_FunctionVoidUnnamedArgument(self):
        self.ExpectedMockFromProto(
            """
            int f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().intReturnValue();
                }
                return WRITEME;
            }
            """,
            "int f(void);")

    def test_UnsignedIntFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            unsigned int f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().unsignedIntReturnValue();
                }
                return WRITEME;
            }
            """,
            "unsigned int f();")

    def test_LongIntFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            long int f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().longIntReturnValue();
                }
                return WRITEME;
            }
            """,
            "long int f();")

    def test_UnsignedLongIntFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            unsigned long int f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().unsignedLongIntReturnValue();
                }
                return WRITEME;
            }
            """,
            "unsigned long int f();")

    def test_ConstCharPtrFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            const char* f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().stringReturnValue();
                }
                return WRITEME;
            }
            """,
            "const char* f();")

    def test_DoubleFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            double f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().doubleReturnValue();
                }
                return WRITEME;
            }
            """,
            "double f();")

    def test_VoidFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            void f() {
                mock().actualCall("f");
            }
            """,
            "void f();")

    def test_VoidPtrFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            void* f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().pointerReturnValue();
                }
                return WRITEME;
            }
            """,
            "void* f();")

    def test_ConstVoidPtrFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            const void* f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().constPointerReturnValue();
                }
                return WRITEME;
            }
            """,
            "const void* f();")

    def test_CharPtrFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            char* f() {
                mock().actualCall("f");
                if mock().hasReturnValue() {
                    return mock().pointerReturnValue();
                }
                return WRITEME;
            }
            """,
            "char* f();")

    def test_VoidFunctionOneSimpleArgument(self):
        self.ExpectedMockFromProto(
            """
            void f(int i) {
                mock().actualCall("f")
                    .withParameter("i", i);
            }
            """,
            "void f(int i);")

    def test_VoidFunctionThreeSimpleArguments(self):
        self.ExpectedMockFromProto(
            """
            void f(int i, double j, int k) {
                mock().actualCall("f")
                    .withParameter("i", i)
                    .withParameter("j", j)
                    .withParameter("k", k);
            }
            """,
            "void f(int i, double j, int k);")

    def test_CharPtrFunctionThreeSimpleArguments(self):
        self.ExpectedMockFromProto(
            """
            char* f(int i, double j, int k) {
                mock().actualCall("f")
                    .withParameter("i", i)
                    .withParameter("j", j)
                    .withParameter("k", k);
                if mock().hasReturnValue() {
                    return mock().pointerReturnValue();
                }
                return WRITEME;
            }
            """,
            "char* f(int i, double j, int k);")

    def test_ConstCharFunctionTwoComplexArguments(self):
        self.ExpectedMockFromProto(
            """
            const char* f(char* i, const char* m) {
                mock().actualCall("f")
                    .withParameter("i", i)
                    .withParameter("m", m);
                if mock().hasReturnValue() {
                    return mock().stringReturnValue();
                }
                return WRITEME;
            }
            """,
            "const char* f(char* i, const char* m);")

    # Here I get from pycparser:
    #
    #   Parse error: ':1:7: before: f' with input: 'foo_t f(int i);'
    #
    # which makes me think pycparser might not be the right tool for what
    # I want to do...
    #
    # Compare with the very informative message I get from clang:
    #
    #   clang foo.c
    #   foo.c:1:1: error: unknown type name 'foo_t'
    #   foo_t f(int i);
    #   ^
    #
    # This is exactly what I want to know, the _type_ of the error:
    #
    #     unknown type name 'foo_t'
    #
    # with that, I can re-run the parser with a fake input:
    #
    #     typedef int foo_t;
    #     foo_t f(int i);
    #
    # that would be enough to generate the mock boilerplate!
    # Clearly the typedef could be completely wrong, but in any case the
    # boilerplate would be there for the user to verify and edit, as opposed
    # to just a dumb error message and no boilerplate at all...
    #
    @unittest.skip("NOTYET")
    def test_TypedefFunctionOneArgument(self):
        self.ExpectedMockFromProto(
            """
            foo_t f(int i) {
                mock().actualCall("f")
                    .withParameter("i", i);
            }
            """,
            "foo_t f(int i);")

if __name__ == '__main__':
    unittest.main()
