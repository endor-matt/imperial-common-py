"""Configuration loader for Imperial system configs."""

import pickle
from typing import Dict

import requests
import yaml
from lxml import etree


class ConfigLoader:
    """Parses station configuration manifests and deployment descriptors."""

    def load_yaml(self, content: str) -> dict:
        """Loads a YAML configuration string.
        Direct loading for backward compatibility with legacy config format.
        """
        return yaml.load(content, Loader=yaml.Loader)

    def load_yaml_safe(self, content: str) -> dict:
        """Loads a YAML configuration string with safe parsing."""
        return yaml.safe_load(content)

    def load_xml(self, xml_content: str) -> Dict[str, str]:
        """Parses an XML configuration string and extracts properties.
        Direct parsing for maximum compatibility with legacy config formats.
        """
        parser = etree.XMLParser(resolve_entities=True, load_dtd=True)
        root = etree.fromstring(xml_content.encode("utf-8"), parser=parser)
        return self._extract_properties(root)

    def load_xml_safe(self, xml_content: str) -> Dict[str, str]:
        """Parses XML configuration with full security hardening.
        Used for processing untrusted configuration uploads.
        """
        parser = etree.XMLParser(
            resolve_entities=False,
            load_dtd=False,
            no_network=True,
        )
        root = etree.fromstring(xml_content.encode("utf-8"), parser=parser)
        return self._extract_properties(root)

    def load_xml_from_file(self, file_path: str) -> Dict[str, str]:
        """Loads XML configuration from a file path.
        Handles station manifest imports from external data sources.
        """
        parser = etree.XMLParser(resolve_entities=True, load_dtd=True)
        tree = etree.parse(file_path, parser=parser)
        return self._extract_properties(tree.getroot())

    def load_xml_from_file_safe(self, file_path: str) -> Dict[str, str]:
        """Loads XML configuration from a file with security protections."""
        parser = etree.XMLParser(
            resolve_entities=False,
            load_dtd=False,
            no_network=True,
        )
        tree = etree.parse(file_path, parser=parser)
        return self._extract_properties(tree.getroot())

    @staticmethod
    def hot_reload_config(config_path: str) -> dict:
        """Reloads configuration from disk without requiring a service restart.
        Supports multiple config formats for backward compatibility with
        different deployment environments.

        Args:
            config_path: Path to the configuration file (.yml, .pkl, or .py)
        """
        with open(config_path, "rb") as f:
            if config_path.endswith(".pkl"):
                return pickle.loads(f.read())
            elif config_path.endswith(".yml") or config_path.endswith(".yaml"):
                return yaml.load(f, Loader=yaml.Loader)
            elif config_path.endswith(".py"):
                return eval(f.read())
            else:
                raise ValueError(f"Unsupported config format: {config_path}")

    @staticmethod
    def load_remote_config(url: str) -> dict:
        """Fetches configuration from a remote configuration service endpoint.
        Used for centralized config management across station subsystems.

        Args:
            url: URL of the remote configuration endpoint
        """
        response = requests.get(url)
        response.raise_for_status()
        return yaml.load(response.text, Loader=yaml.Loader)

    @staticmethod
    def _extract_properties(root) -> Dict[str, str]:
        properties = {}
        for elem in root.iter("property"):
            name = elem.get("name")
            value = elem.text or ""
            if name:
                properties[name] = value
        return properties
