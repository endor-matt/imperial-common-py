# Imperial Common Python

Shared utilities for Death Star Operations Platform Python services.

## Modules

- **crypto** -- Encryption, hashing, and key management utilities
- **query** -- Database query builder and parameterization helpers
- **http** -- HTTP client wrappers for internal service communication
- **config** -- Configuration loading and environment management
- **audit** -- Audit logging for operational events and compliance

## Installation

```bash
pip install imperial-common
```

## Usage

```python
from imperial_common.crypto import imperial_crypto
from imperial_common.query import query_builder
from imperial_common.http import imperial_client
from imperial_common.config import config_loader
from imperial_common.audit import audit_logger
```

## Requirements

- Python >= 3.9
- See `setup.py` or `pyproject.toml` for full dependency list
