import unittest
from unittest import mock

import cached_taplo_lint


@mock.patch("subprocess.run")
class TestCachedTaploLint(unittest.TestCase):
    def test_success(self, mock_run: mock.Mock):
        mock_run.return_value.returncode = 0

        try:
            cached_taplo_lint.main()
        except SystemExit as e:
            self.assertEqual(e.code, 0)

        mock_run.assert_called()

    def test_failure(self, mock_run: mock.Mock):
        mock_run.return_value.returncode = 1

        with self.assertRaises(SystemExit) as cm:
            cached_taplo_lint.main()
        self.assertNotEqual(cm.exception.code, 0)

        mock_run.assert_called()

    def test_add_cache_argument(self, mock_run: mock.Mock):
        mock_run.return_value.returncode = 0

        test_args = ["cached-taplo-lint", "--foo", "bar"]
        with mock.patch("sys.argv", test_args):
            try:
                cached_taplo_lint.main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

        called_args = mock_run.call_args[0][0]
        self.assertEqual(
            called_args,
            [
                "taplo",
                "lint",
                "--foo",
                "bar",
                "--cache-path",
                mock.ANY,
            ],
        )

    def test_keep_cache_argument(self, mock_run: mock.Mock):
        mock_run.return_value.returncode = 0

        test_args = ["cached-taplo-lint", "--foo", "bar", "--cache-path", "/tmp/cache"]
        with mock.patch("sys.argv", test_args):
            try:
                cached_taplo_lint.main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

        called_args = mock_run.call_args[0][0]
        self.assertEqual(
            called_args,
            [
                "taplo",
                "lint",
                "--foo",
                "bar",
                "--cache-path",
                "/tmp/cache",
            ],
        )

    def test_keep_cache_argument_with_equals(self, mock_run: mock.Mock):
        mock_run.return_value.returncode = 0

        test_args = ["cached-taplo-lint", "--foo", "bar", "--cache-path=/tmp/cache"]
        with mock.patch("sys.argv", test_args):
            try:
                cached_taplo_lint.main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

        called_args = mock_run.call_args[0][0]
        self.assertEqual(
            called_args,
            [
                "taplo",
                "lint",
                "--foo",
                "bar",
                "--cache-path=/tmp/cache",
            ],
        )


if __name__ == "__main__":
    unittest.main()
