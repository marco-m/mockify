# Mockify (work in progress!)

Generate complete boilerplate code for [CppUMock][] C/C++ mocks.

When writing mocks, the majority of the code is really boring boilerplate, for
example to mock:

    void* malloc(size_t size)

one has to write:

    1    void* malloc(size_t size) {
    2        mock().actualCall("malloc")
    3            .withParameter("size", size);
    4        if mock().hasReturnValue() {
    5            return mock().pointerReturnValue();
    6        }
    7        return real_malloc(size);
    8    }

where *everything* but line 7 is boilerplate. Multiply this for the tens of
mocks needed also for the smallest unit test and the task becomes quickly boring
and error-prone.

Mockify is written in Python and thanks to the excellent [pycparser][] parses
the C code of the function prototype to mock and generates all the needed
boilerplate :-)






[CppUMock]: https://cpputest.github.io
[pycparser]: https://github.com/eliben/pycparser