# Quick Start Guide

Welcome to CodeCRISPR! This guide will get you up and running in minutes.

## Installation

```bash
pip install codecrispr
```

## Basic Usage

### 1. Inspect a File

```bash
codecrispr --inspect example.py
```

Output:
```
Inspecting 'example.py' [python]:
  greet_user: lines 0-3
  calculate_area: lines 4-8
  main: lines 9-14
```

### 2. Edit a Function

```bash
codecrispr example.py greet_user 'def greet_user(name):
    """Greet the user formally"""
    print(f"Greetings, {name}!")'
```

### 3. Preview Changes

```bash
codecrispr --inspect example.py --preview greet_user
```
