# Flying Red Panda - lab 1 - variant 7

The example project with limited implementation on dictionary
based on hash-map (collision resolution: separate chaining).

## Project structure

- `hashmap.py` -- implementation of `HashMap` class.
- `hashmap_test.py` -- unit and PBT tests for `HashMap`.

## Features

Using a hashmap to implement various operations of the dictionary,
and use separate chaining to solve the conflict problem flexibly.

- `PTB:` -- test_init
- `PTB:` -- test_hashFuction
- `PTB:` -- test_add
- `PTB:` -- test_remove
- `PTB:` -- test_access_size
- `PTB:` -- test_access_member
- `PTB:` -- test_dict_to_hash
- `PTB:` -- test_hash_to_dict
- `PTB:` -- test_filter
- `PTB:` -- test_map
- `PTB:` -- test_reduce
- `PTB:` -- test_iter
- `PTB:` -- test_monoid_associativity
- `PTB:` -- test_monoid_identify

## Contribution

- Enya Shi (212320002@hdu.edu.cn) -- Complete the 'hashmap.py'.
- Yuxuan Liu (212320004@hdu.edu.cn) -- Complete the 'hashmap_test.py'.
- Team members communicate and collaborate to complete tasks.

## Changelog

- 2022.05.08 - 7
  - Update README. Data type change to configurable.
- 2022.05.02 - 6
  - Update README and CI config. Add type hints and docstrings for all functions.
- 2022.04.24 - 5
  - Update README. Modify part of functions and add test cases.
  as suggested.
- 2022.04.18 - 4
  - Update README. Modify part of functions and add test cases.
  as suggested.
- 2022.04.11 - 3
  - Update README. Chek code style and type annotation.
- 2022.04.09 - 2
  - Update README.
  - Add test sections.
  - Add test coverage and modify the code for better coverage.
- 2022.04.08 - 1
  - Update README. Add formal sections.
- 2022.04.07 - 0
  - Set environment according to 'check.yml' and learning
  corresponding information about hashmap (separate chaining).

## Design notes

- Implementation restrictions
  - hashFuction(key): Determine the mapping index of the element
  in the hashmap according to the key. As for different types of
  the key, if the type of key is int, using the mapping function
  directly. If the type of key is float, using the integer part
  of the key to determine the hashmap index. If the type of key
  is str, definiting the mapping with the first character of the
  string.
  - add(key, value): The type of key can be char, int, or float.
  If key has already existed in the dictionay, value will be
  modified according to the parameter.
  - remove(key): Remove an element by key.
  - access_member(key): Get an element's value in the dictionary
  by key.
  - dict_to_hash(dict): Parameter 'dict' should be dictionary
  type in python.
  - filter(func): Determine whether the value corresponding to
  the key in the dictionary satisfy the predicate 'func'. If the
  value doesn't satisfy the 'func', remove the element from the
  dictionary.
  - map(func): Pay attention to the different value types of the
  elements in the dictionary, some operations can only operate on
  numeric types but not on string types, and some operations can
  only operate on character types but not on numeric types. If
  the element value in the dictionary has both numeric and string
  types, attention need to be paid on the choice of parameter 'func'.
  - reduce(func, initValue): Different 'initValue' are required
  for different 'func'. Pay attention to the data type of dictionary
  elements and select the appropriate operation function 'func'.
  - empty(): A mutable operation on the structure. Empty the structure.
  - concat(hashMap): A mutable operation on the structure. Connect
  another structure to the original structure

- Analysis advantages and disadvantages of unittest and PBT tests
  - Advantages: After the unit test is completed, the actual result
  is compared with the expected result (assertion), so as to determine
  whether the execution of the use case is passed or not. The unit
  test framework provides a wealth of assertion methods. Code coverage
  can be obtained through unit testing to modify test cases to check
  the correctness and integrity of the code.
  - Disadvantages: Testers need to be familiar with the interface
  information of the project, which takes time to understand the
  code to better ensure the coverage of use cases. In addition, it
  is difficult for test cases to cover all code branches at one
  time, and test cases need to be added and modified to get better
  coverage.