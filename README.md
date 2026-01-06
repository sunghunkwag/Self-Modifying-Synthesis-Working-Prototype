# Self-Modifying Synthesis Working Prototype

**Status: Research Prototype / Work in Progress**

## Abstract
This repository contains a working prototype of a self-modifying neuro-symbolic engine. The system integrates bottom-up synthesis with unsupervised library learning (Stitch). It demonstrates the capability to spontaneously discover and add new operators to its domain-specific language (DSL) during runtime, without hardcoded templates or human intervention.

## Core Mechanisms
1.  **Bottom-Up Synthesis**: Enumerates ASTs to solve input/output examples.
2.  **Anti-Unification (Stitch)**: Compresses successful programs into reusable higher-order functions (abstractions).
3.  **Dynamic Grammar Evolution**: Updates the DSL at runtime with discovered abstractions.
4.  **Self-Critic**: Generates adversarial tasks to verify the generalization of discovered abstractions.

## Usage

### Prerequisites
- Python 3.8 or higher

### Replication
Run the verification script to observe the unguided evolution of operators:

```bash
python verify_organic.py
```

This script runs a 30-cycle evolution loop starting from basic arithmetic primitives.

## License
MIT License.
