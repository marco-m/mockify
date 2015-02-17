#!/usr/bin/env python3.4

from mockify import generate_mock_boilerplate
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

    # def test_GracefullyHandleParseErrors(self):
    #     # Missing ``;`` at end of ``void f()`` is a syntax error
    #     self.assertEqual("ciao",
    #                      generate_mock_boilerplate("void f()"))

if __name__ == '__main__':
    unittest.main()
