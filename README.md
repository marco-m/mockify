# Mockify (work in progress!)


[![Build Status](https://travis-ci.org/marco-m/mockify.svg?branch=master
)](https://travis-ci.org/marco-m/mockify)

Generate complete boilerplate code for [CppUTest][] C/C++ mocks.

When writing mocks, the majority of the code is just boring boilerplate. For
example, to mock

    int zoo_cat(int a)

one has to write:

    1    int zoo_cat(int a) {
    2        mock().actualCall("zoo_cat")
    3            .withParameter("a", a);
    4        if mock().hasReturnValue() {
    5            return mock().intReturnValue();
    6        }
    7        return something(a);
    8    }

where *everything* but line 7 is boilerplate. Multiply this for the tens of
mocks needed also for the smallest unit test and the task quickly becomes
boring and error-prone.

Mockify is written in Python and thanks to the excellent [pycparser][] parses
the C code of the function prototype to mock and generates all the needed
boilerplate :-)

## Development status

Already usable with basic functionalities. Most important missing parts:

- support for basic typedefs (eg size_t) both as function type and as function
argument
- support for output parameters (eg void foo(int* bar))

## Usage

Mockify is designed to be used with any editor or IDE, or just from the shell.

Assuming that function `zoo_cat()` is declared in header file `zoo.h`, calling:

    mockify.py zoo "int zoo_cat(int a);"

will generate mock file `zoo_mock.cpp`, containing the mock boilerplate for
function `zoo_cat()`.

Subsequent calls to mockify matching on the header file will append the new
mock boilerplate to `zoo_mock.cpp`. For example

    mockify.py zoo "int zoo_dog(int b);"

will append the boilerplate mock for `zoo_dog()`.

## Suggested workflow

Bring a source file under unit test. Once the compilation is succesful, you
will start to have linker errors for all the functions you need to mock.

Copy the first unfound symbol from the linker, search for it (using your IDE,
cscope, ctags, ...), go to the corresponding header file. Copy and paste the
function declaration and pass it to mockify.

The above steps can be automated within your editor or IDE. For CLion, you can
use it as an "external tool" and pass it automatically the name of the header
file and the copy and paste of the function declaration.

Add the generated mock file to the build. Open the generated mock file, check
and complete the mock boilerplate.

Rinse and repeat :-)


[CppUTest]: https://cpputest.github.io
[pycparser]: https://github.com/eliben/pycparser
