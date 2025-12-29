#!/usr/bin/env python3
"""Simple hello helper: asks for a name and how many times to say the name is cool."""
import sys


def get_name(prompt: str = "Enter a name: ") -> str:
    name = input(prompt).strip()
    if not name:
        print("Error: name cannot be empty.")
        sys.exit(1)
    return name


def get_count(prompt: str = "How many times? ") -> int:
    try:
        val = int(input(prompt).strip())
    except Exception:
        print("Error: please enter a whole number for the count.")
        sys.exit(1)
    if val < 0:
        print("Error: count must be zero or positive.")
        sys.exit(1)
    return val


def main() -> None:
    name = get_name()
    count = get_count()
    for _ in range(count):
        print(f"{name} is cool")


if __name__ == "__main__":
    main()
