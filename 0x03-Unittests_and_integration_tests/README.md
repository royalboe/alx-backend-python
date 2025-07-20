# 0x03. Unittests and Integration Tests

In this project, you will learn the difference between **unit tests** and **integration tests**, and practice common testing patterns such as **mocking**, **parameterization**, and **fixtures** using Python’s built‑in `unittest` framework and the `parameterized` library.

---

## 📚 Resources

- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)  
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)  
- [How to mock a readonly property with mock?](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock)  
- [parameterized](https://github.com/wolever/parameterized)  
- [Memoization](https://en.wikipedia.org/wiki/Memoization)  

---

## 🎯 Learning Objectives

By the end of this project, you should be able to explain **without Google**:

1. The difference between **unit** and **integration** tests.  
2. Common testing patterns:
   - **Mocking** external dependencies  
   - **Parameterizing** tests for multiple inputs  
   - Using **fixtures** to drive integration scenarios  
3. When to mock and what to leave un‑mocked.  
4. How to organize test suites in `unittest`.

---

## ⚙️ Requirements

- All code will run on **Ubuntu 18.04 LTS** with **Python 3.7**.  
- Every file must end with a newline and begin with:
  ```bash
  #!/usr/bin/env python3
- A README.md at the project root is mandatory.
- Conform to pycodestyle 2.5 styling.
- All files must be executable (chmod +x).
- Every module, class, and function must have a proper docstring.
- Type‑annotate all functions and coroutines.
- Execute your tests with:

```bash
$ python3 -m unittest path/to/test_file.py
```

## 📝 Tasks

0. Parameterize a unit test (mandatory)
File: test_utils.py

Write TestAccessNestedMap.test_access_nested_map using @parameterized.expand to test:

{"a": 1}, ("a",) → 1

{"a": {"b": 2}}, ("a",) → {"b": 2}

{"a": {"b": 2}}, ("a", "b") → 2

1. Exception cases (mandatory)
File: test_utils.py

Write TestAccessNestedMap.test_access_nested_map_exception to assert that a KeyError is raised (and carries the missing key) for:

{}, ("a",)

{"a": 1}, ("a", "b")

2. Mock HTTP calls (mandatory)
File: test_utils.py

Test utils.get_json by patching requests.get to return a mock whose .json() returns:

URL "http://example.com", payload {"payload": True}

URL "http://holberton.io", payload {"payload": False}

3. Test memoization (mandatory)
File: test_utils.py

Test the @memoize decorator so that a method decorated as property calls its underlying method only once.

4. Parameterize and patch as decorators (mandatory)
File: test_client.py

Test GithubOrgClient.org using @patch to mock get_json and @parameterized.expand for org names google, abc.

5. Mocking a property (mandatory)
File: test_client.py

Test GithubOrgClient._public_repos_url by mocking the org property with PropertyMock.

6. More patching (mandatory)
File: test_client.py

Test GithubOrgClient.public_repos by patching:

get_json with a fake payload

_public_repos_url as a property

7. Parameterize license check (mandatory)
File: test_client.py

Test GithubOrgClient.has_license for:

{"license": {"key": "my_license"}}, "my_license" → True

{"license": {"key": "other_license"}}, "my_license" → False

8. Integration test: fixtures (mandatory)
File: test_client.py

Using @parameterized_class(TEST_PAYLOAD), test GithubOrgClient.public_repos end‑to‑end by patching only requests.get to return the org_payload and repos_payload fixtures.

9. Advanced integration (optional)
File: test_client.py

Implement test_public_repos and test_public_repos_with_license to validate filtering by license (e.g., "apache-2.0") against fixture data.