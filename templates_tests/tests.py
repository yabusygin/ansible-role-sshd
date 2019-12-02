"""/etc/ssh/sshd_config template tests."""

import unittest
import pathlib

from .utils import (
    relative_to_path,
    render_role_template,
    resource_abs_path,
    resource_str,
)


_ROLE_PATH = relative_to_path(
    base_path=pathlib.Path(__file__),
    relative_path=pathlib.Path(".."),
)
_TEMPLATE_FILENAME = "sshd_config.j2"


class DefaultParams(unittest.TestCase):
    """Test default params."""

    def test(self):
        """Render with default params."""
        expect = resource_str(
            resource_path=pathlib.Path("default", "sshd_config"),
            package=__name__,
        )
        actual = render_role_template(
            role_path=_ROLE_PATH,
            template_filename=_TEMPLATE_FILENAME,
        )
        self.assertEqual(expect, actual)


class ListenAddress(unittest.TestCase):
    """Specify address to listen."""

    def test_single(self):
        """Specify single address."""
        expect = resource_str(
            resource_path=pathlib.Path(
                "listen-address", "single", "sshd_config",
            ),
            package=__name__,
        )
        context_manager = resource_abs_path(
            resource_path=pathlib.Path("listen-address", "single", "vars.yml"),
            package=__name__,
        )
        with context_manager as variables_path:
            actual = render_role_template(
                role_path=_ROLE_PATH,
                template_filename=_TEMPLATE_FILENAME,
                variables_path=variables_path,
            )
        self.assertEqual(expect, actual)

    def test_multiple(self):
        """Specify multiple addresses."""
        expect = resource_str(
            resource_path=pathlib.Path(
                "listen-address", "multiple", "sshd_config",
            ),
            package=__name__,
        )
        context_manager = resource_abs_path(
            resource_path=pathlib.Path(
                "listen-address", "multiple", "vars.yml",
            ),
            package=__name__,
        )
        with context_manager as variables_path:
            actual = render_role_template(
                role_path=_ROLE_PATH,
                template_filename=_TEMPLATE_FILENAME,
                variables_path=variables_path,
            )
        self.assertEqual(expect, actual)


class Match(unittest.TestCase):
    """Specify Match option."""

    def test(self):
        """Specify public SFTP server options."""
        expect = resource_str(
            resource_path=pathlib.Path("match", "sshd_config"),
            package=__name__,
        )
        context_manager = resource_abs_path(
            resource_path=pathlib.Path("match", "vars.yml"),
            package=__name__,
        )
        with context_manager as variables_path:
            actual = render_role_template(
                role_path=_ROLE_PATH,
                template_filename=_TEMPLATE_FILENAME,
                variables_path=variables_path,
            )
        self.assertEqual(expect, actual)
