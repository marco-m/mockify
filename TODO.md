THOUGHTS
--------

TODO
----

- Handle typedefs as return values and as arguments.

- Support typemap.yaml, that maps unknown type names to known type names.
Two of these maps: one that is shipped with mockify, one that is created by
the user.

    -   Standard types (the ones defined in stdint.h)

        int16_t => int (because CppUTest has int, not int16) 

    - User types example:

        foo_int -> int
        foo_bool -> int
        foo_bar -> unsigned int
    

- Add C++ tests that validate that the generated C++ code is correct!

- Add integration tests that check also the file generation.

- When stdout support is added, add this to integration tests.