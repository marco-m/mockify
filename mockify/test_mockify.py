#!/usr/bin/env python3.4 -B

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

    def test_VoidFunctionZeroArguments(self):
        self.ExpectedMockFromProto(
            """
            void f() {
                mock().actualCall("f");
            }
            """,
            "void f();")

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

    # def test_UnsignedIntFunctionZeroArguments(self):
    #     self.ExpectedMockFromProto(
    #         """
    #         unsigned int f() {
    #             mock().actualCall("f");
    #             if mock().hasReturnValue() {
    #                 return mock().unsignedIntReturnValue();
    #             }
    #             return WRITEME;
    #         }
    #         """,
    #         "unsigned int f();")

    # def test_ConstCharPtrFunctionZeroArguments(self):
    #     self.ExpectedMockFromProto(
    #         """
    #         const char* f() {
    #             mock().actualCall("f");
    #             if mock().hasReturnValue() {
    #                 return mock().stringReturnValue();
    #             }
    #             return WRITEME;
    #         }
    #         """,
    #         "const char* f();")

if __name__ == '__main__':
    unittest.main()
