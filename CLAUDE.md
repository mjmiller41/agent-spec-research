# Claude Agent Guidelines

This repository follows the universal agent guidelines defined in [AGENTS.md](AGENTS.md) and the [OKF v0.2 Specification](SPEC.md).

## Quick Start
* **Initialize bundle**: `okf init --bundle ./bundle`
* **Scaffold concept**: `okf template <template_name> --out bundle/<folder>/<concept>.md`
* **After every change**: Run `okf validate && okf index && okf log Update "<message>" && okf viz`
