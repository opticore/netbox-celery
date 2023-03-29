# Netbox Celery Plugin

<p align="center">
  <img src="https://raw.githubusercontent.com/opticore/netbox-celery/main/docs/images/netbox_celery.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/opticore/netbox-celery/actions"><img src="https://github.com/opticore/netbox-celery/actions/workflows/ci_integration.yml/badge.svg?branch=main"></a>
  <a href=""><img src="https://readthedocs.org/projects/netbox-celery/badge/"></a>
  <a href="https://pypi.org/project/netbox-celery/"><img src="https://img.shields.io/pypi/v/netbox-celery"></a>
  <a href="https://pypi.org/project/netbox-celery/"><img src="https://img.shields.io/pypi/dm/netbox-celery"></a>
  <br>
  An App for <a href="https://github.com/netbox-community/netbox">Netbox</a>.
</p>

## Overview

The Netbox Celery plugin is a Netbox plugin to provide support for celery. This plugin can be used base for any automation tasks.

### Screenshots

#### Celery Results List

![Overview](https://raw.githubusercontent.com/opticore/netbox-celery/main/docs/images/screenshot_celery_list.png)

#### Celery Result Details

![Overview](https://raw.githubusercontent.com/opticore/netbox-celery/main/docs/images/screenshot_celery_details.png)

## Installation

1. Install the package using pip:

``` bash
pip install netbox-celery
```

2. Add plugin to `PLUGINS` in configuration:

``` python
PLUGINS = [
    ...
    "netbox_celery",
    ...
]
```
