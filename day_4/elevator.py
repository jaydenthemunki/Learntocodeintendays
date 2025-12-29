#!/usr/bin/env python3
"""Simple elevator helper: asks for current and destination floor and prints direction and number of floors."""
import sys
from typing import Optional


def get_floor(prompt: str, min_floor: int = 0, max_floor: int = 30, excluded: Optional[int] = None) -> int:
    try:
        val = int(input(prompt).strip())
    except Exception:
        print(f"Error: please enter a whole number between {min_floor} and {max_floor} for the floor.")
        sys.exit(1)
    if val < min_floor or val > max_floor:
        print(f"Error: floor must be between {min_floor} and {max_floor}.")
        sys.exit(1)
    if excluded is not None and val == excluded:
        print(f"Error: floor {excluded} does not exist.")
        sys.exit(1)
    return val


def main() -> None:
    # Ask the user which floor to ignore (blank for none)
    raw = input("Enter floor to ignore (0-30) or press Enter for none: ").strip()
    excluded: Optional[int] = None
    if raw:
        try:
            ex_val = int(raw)
        except Exception:
            print("Error: please enter a whole number between 0 and 30 for the excluded floor.")
            sys.exit(1)
        if ex_val < 0 or ex_val > 30:
            print("Error: excluded floor must be between 0 and 30.")
            sys.exit(1)
        excluded = ex_val

    prompt = "Enter current floor (0-30): "
    if excluded is not None:
        prompt = f"Enter current floor (0-30, no {excluded}): "
    current = get_floor(prompt, 0, 30, excluded)

    prompt = "Enter destination floor (0-30): "
    if excluded is not None:
        prompt = f"Enter destination floor (0-30, no {excluded}): "
    dest = get_floor(prompt, 0, 30, excluded)

    diff = dest - current

    if diff == 0:
        print(f"You're already on floor {current}.")
    else:
        direction = "up" if diff > 0 else "down"
        floors = abs(diff)
        # If the trip crosses the non-existent floor, subtract one physical floor
        if excluded is not None and ((current < excluded < dest) or (dest < excluded < current)):
            floors -= 1
        floor_word = "floor" if floors == 1 else "floors"
        print(f"Direction: {direction}, {floors} {floor_word}")


if __name__ == "__main__":
    main()
