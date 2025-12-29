#!/usr/bin/env python3
"""Simple elevator helper: asks for current and destination floor and prints direction and number of floors."""
import sys


def get_floor(prompt: str, min_floor: int = 0, max_floor: int = 30, excluded: int = 13) -> int:
    try:
        val = int(input(prompt).strip())
    except Exception:
        print(f"Error: please enter a whole number between {min_floor} and {max_floor} for the floor.")
        sys.exit(1)
    if val < min_floor or val > max_floor:
        print(f"Error: floor must be between {min_floor} and {max_floor}.")
        sys.exit(1)
    if val == excluded:
        print(f"Error: floor {excluded} does not exist.")
        sys.exit(1)
    return val


def main() -> None:
    current = get_floor("Enter current floor (0-30, no 13): ", 0, 30)
    dest = get_floor("Enter destination floor (0-30, no 13): ", 0, 30)
    diff = dest - current

    if diff == 0:
        print(f"You're already on floor {current}.")
    else:
        direction = "up" if diff > 0 else "down"
        floors = abs(diff)
        # If the trip crosses the non-existent floor 13, subtract one physical floor
        if (current < 13 < dest) or (dest < 13 < current):
            floors -= 1
        floor_word = "floor" if floors == 1 else "floors"
        print(f"Direction: {direction}, {floors} {floor_word}")


if __name__ == "__main__":
    main()
