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
        self.assertRaises(MockError, generate_mock_boilerplate, "static void f();")

    def test_RefuseDeclarationsThatAreNotFunctions(self):
        self.assertRaises(MockError, generate_mock_boilerplate, "int i;")

    def test_ParseError(self):
        self.assertRaises(MockError, generate_mock_boilerplate, "foo")

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

    def test_VoidFunctionOneArgument(self):
        self.ExpectedMockFromProto(
            """
            void f(int i) {
                mock().actualCall("f")
                    .withParameter("i", i);
            }
            """,
            "void f(int i);")

    @unittest.skip("NOTYET")
    def test_VoidFunctionTwoArguments(self):
        self.ExpectedMockFromProto(
            """
            void f(int i, double j) {
                mock().actualCall("f")
                    .withParameter("i", i)
                    .withParameter("j", j);
            }
            """,
            "void f(int i, double j);")


if __name__ == '__main__':
    unittest.main()
