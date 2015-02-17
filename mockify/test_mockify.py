#!/usr/bin/env python3.4 -B

from mockify import generate_mock_boilerplate
from mockify import MockError
import unittest
import textwrap


class BoilerPlateGeneration(unittest.TestCase):
    def ExpectedMockFromProto(self, mock_function, prototype):
        self.assertEqual(textwrap.dedent(mock_function).strip("\n"),
                         generate_mock_boilerplate(prototype))

    def test_SimplestPossible(self):
        self.ExpectedMockFromProto(
            """
            void f() {
                mock().actualCall("f");
            }
            """,
            "void f();")

    def test_GracefullyHandleParseErrors(self):
        # Missing ``;`` at end of ``void f()`` is a syntax error
        self.assertRaises(MockError, generate_mock_boilerplate, "void f()")

    def test_GracefullyHandleDeclarationsThatAreNotFunctions(self):
        self.assertRaises(MockError, generate_mock_boilerplate, "int i;")


if __name__ == '__main__':
    unittest.main()
