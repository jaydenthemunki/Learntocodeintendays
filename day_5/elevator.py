#!/usr/bin/env python3
"""Elevator sequence evaluator for any number of passengers.

- Supports arbitrary number of passengers (pickup floor -> destination floor)
- Evaluates sequences of stops while enforcing that each passenger is picked up before dropped off
- For small N, performs exact search over valid event orders; for larger N, uses heuristics
- Provides metrics: pickup waits, arrival times, total travel, averages and maxima

Usage examples:
  python day_5/elevator.py                       # interactive prompt
  python day_5/elevator.py --start 5 --p 2:1 10:6 15:19  # non-interactive

"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

# Threshold for attempting exact enumeration of all valid event orders
EXACT_ENUM_LIMIT = 6  # safe for typical machines; increases work factor quickly


@dataclass
class Passenger:
    id: int
    pickup: int
    drop: int
    name: Optional[str] = None


Event = Tuple[str, int]  # ('p' or 'd', passenger_id)


def simulate_events(events: Sequence[Event], start: int, passengers: Sequence[Passenger]) -> Dict:
    """Simulate elevator moving through the given events (list of ('p'/'d', id)).

    Returns metrics dict including total_travel, pickup_times, arrival_times, total_pickup_wait, etc.
    Time is measured as floors travelled (1 per floor).
    """
    pos_map = {('p', p.id): p.pickup for p in passengers}
    pos_map.update({('d', p.id): p.drop for p in passengers})

    time = 0
    cur = start
    pickup_times: Dict[int, int] = {}
    arrival_times: Dict[int, int] = {}

    # If the first event is at a different floor, travel there first
    for ev in events:
        floor = pos_map[ev]
        time += abs(floor - cur)
        cur = floor
        typ, pid = ev
        if typ == 'p':
            pickup_times[pid] = time
        else:
            arrival_times[pid] = time

    total_travel = time

    waits = {pid: pickup_times.get(pid, math.inf) for pid in [p.id for p in passengers]}
    arrivals = {pid: arrival_times.get(pid, math.inf) for pid in [p.id for p in passengers]}

    total_pickup_wait = sum(v if v != math.inf else 0 for v in waits.values())
    max_pickup_wait = max(v if v != math.inf else 0 for v in waits.values()) if waits else 0
    avg_pickup_wait = total_pickup_wait / len(waits) if waits else 0

    total_arrival_time = sum(v if v != math.inf else 0 for v in arrivals.values())
    max_arrival_time = max(v if v != math.inf else 0 for v in arrivals.values()) if arrivals else 0
    avg_arrival_time = total_arrival_time / len(arrivals) if arrivals else 0

    return {
        'events': events,
        'total_travel': total_travel,
        'pickup_times': pickup_times,
        'arrival_times': arrival_times,
        'total_pickup_wait': total_pickup_wait,
        'avg_pickup_wait': avg_pickup_wait,
        'max_pickup_wait': max_pickup_wait,
        'avg_arrival_time': avg_arrival_time,
        'max_arrival_time': max_arrival_time,
    }


def generate_valid_event_orders(passengers: Sequence[Passenger]) -> Iterable[List[Event]]:
    """Generate all valid event orders (pickup before drop for each passenger).

    Warning: count grows very fast (combinatorial). Only use with small number of passengers.
    """
    n = len(passengers)
    if n == 0:
        yield []
        return

    # quick guard
    if n > EXACT_ENUM_LIMIT:
        raise ValueError(f"Too many passengers ({n}) for exact enumeration; use heuristics instead")

    picked = set()
    dropped = set()

    id_list = [p.id for p in passengers]

    def backtrack(seq: List[Event]):
        if len(seq) == 2 * n:
            yield list(seq)
            return
        # we can pick up any passenger not yet picked
        for pid in id_list:
            if pid not in picked:
                # pick pid
                picked.add(pid)
                seq.append(('p', pid))
                yield from backtrack(seq)
                seq.pop()
                picked.remove(pid)
        # we can drop any passenger already picked but not yet dropped
        for pid in id_list:
            if pid in picked and pid not in dropped:
                dropped.add(pid)
                seq.append(('d', pid))
                yield from backtrack(seq)
                seq.pop()
                dropped.remove(pid)

    yield from backtrack([])


def build_sequence_from_pickup_order(start: int, passengers: Sequence[Passenger], pickup_order: Sequence[int], drop_policy: str = 'defer_nearest') -> List[Event]:
    """Construct a sequence of events from an ordering of pickups.

    drop_policy:
      - 'defer_nearest': after finishing pickups, service drops by greedy nearest-first
      - 'immediate': after picking a passenger, immediately go to their drop (in place)
    """
    seq: List[Event] = []
    cur = start

    picked = set()
    undropped = set()

    # perform pickups in the provided order
    for pid in pickup_order:
        seq.append(('p', pid))
        picked.add(pid)
        undropped.add(pid)
        if drop_policy == 'immediate':
            seq.append(('d', pid))
            undropped.remove(pid)
    # if drops remain, service them greedily (nearest-first) from current position after last pickup
    if undropped:
        # compute current position after pickups
        if seq:
            # find position of last event
            last_ev = seq[-1]
            # determine floor
            last_floor = next((p.drop if last_ev[0] == 'd' else p.pickup for p in passengers if p.id == last_ev[1]), start)
        else:
            last_floor = start
        remaining = set(undropped)
        cur_floor = last_floor
        while remaining:
            # choose passenger whose drop is nearest to cur_floor
            pid = min(remaining, key=lambda pidx: abs(next(p.drop for p in passengers if p.id == pidx) - cur_floor))
            seq.append(('d', pid))
            cur_floor = next(p.drop for p in passengers if p.id == pid)
            remaining.remove(pid)
    return seq


def heuristics_for_large_n(start: int, passengers: Sequence[Passenger], tries: int = 200) -> List[List[Event]]:
    """Return a list of candidate event sequences from simple heuristics for larger N.

    Strategies:
      - nearest pickup first (NPF)
      - farthest pickup first (FPF)
      - random pickup orders with greedy drop service
    """
    ids = [p.id for p in passengers]
    candidates: List[List[Event]] = []

    # nearest pickup first
    ids_sorted_nearest = sorted(ids, key=lambda pid: abs(next(p.pickup for p in passengers if p.id == pid) - start))
    candidates.append(build_sequence_from_pickup_order(start, passengers, ids_sorted_nearest, drop_policy='defer_nearest'))

    # farthest pickup first
    ids_sorted_far = list(reversed(ids_sorted_nearest))
    candidates.append(build_sequence_from_pickup_order(start, passengers, ids_sorted_far, drop_policy='defer_nearest'))

    # try random pickups
    for _ in range(min(tries, 500)):
        order = ids[:]
        random.shuffle(order)
        candidates.append(build_sequence_from_pickup_order(start, passengers, order, drop_policy='defer_nearest'))

    return candidates


def find_best_sequences(start: int, passengers: Sequence[Passenger]) -> Dict[str, Dict]:
    """Find best sequences for different objectives.

    Returns a dict mapping objective string to best result (metrics + sequence).
    Objectives: 'min_avg_pickup_wait', 'min_max_pickup_wait', 'min_total_travel', 'min_avg_arrival_time'
    """
    n = len(passengers)
    candidates: List[List[Event]] = []

    if n <= EXACT_ENUM_LIMIT:
        # Enumerate all valid event orders (may be large but reasonable for small n)
        for ev in generate_valid_event_orders(passengers):
            candidates.append(ev)
    else:
        # Use heuristics for candidate sequences
        candidates.extend(heuristics_for_large_n(start, passengers))

    # Also include sequences built from pickup permutations for moderate n (up to 8)
    if n <= 8:
        # consider permutations of pickups (not full event perms) and greedy drop handling
        from itertools import permutations

        ids = [p.id for p in passengers]
        for perm in permutations(ids):
            candidates.append(build_sequence_from_pickup_order(start, passengers, perm, drop_policy='defer_nearest'))
            candidates.append(build_sequence_from_pickup_order(start, passengers, perm, drop_policy='immediate'))

    # Evaluate candidates and track best for each objective
    best = {
        'min_avg_pickup_wait': None,
        'min_max_pickup_wait': None,
        'min_total_travel': None,
        'min_avg_arrival_time': None,
    }

    def update_best(key: str, result: Dict):
        cur = best[key]
        if cur is None:
            best[key] = result
            return
        # comparison depending on key, with sensible tie-breakers
        if key == 'min_avg_pickup_wait':
            if result['avg_pickup_wait'] < cur['avg_pickup_wait'] or (
                math.isclose(result['avg_pickup_wait'], cur['avg_pickup_wait']) and result['total_travel'] < cur['total_travel']
            ):
                best[key] = result
        elif key == 'min_max_pickup_wait':
            # prefer smaller max pickup wait, then smaller average pickup wait, then smaller total travel
            if (
                result['max_pickup_wait'] < cur['max_pickup_wait']
                or (
                    result['max_pickup_wait'] == cur['max_pickup_wait']
                    and (
                        result['avg_pickup_wait'] < cur['avg_pickup_wait']
                        or (math.isclose(result['avg_pickup_wait'], cur['avg_pickup_wait']) and result['total_travel'] < cur['total_travel'])
                    )
                )
            ):
                best[key] = result
        elif key == 'min_total_travel':
            if result['total_travel'] < cur['total_travel']:
                best[key] = result
        elif key == 'min_avg_arrival_time':
            if result['avg_arrival_time'] < cur['avg_arrival_time'] or (
                math.isclose(result['avg_arrival_time'], cur['avg_arrival_time']) and result['total_travel'] < cur['total_travel']
            ):
                best[key] = result

    for seq in candidates:
        metrics = simulate_events(seq, start, passengers)
        # avoid duplicates: store only unique event lists by tuple
        metrics['events'] = seq
        update_best('min_avg_pickup_wait', metrics)
        update_best('min_max_pickup_wait', metrics)
        update_best('min_total_travel', metrics)
        update_best('min_avg_arrival_time', metrics)

    return best


def format_events_readable(events: Sequence[Event], passengers: Sequence[Passenger], start: int) -> str:
    name_map = {p.id: p.name or str(p.id) for p in passengers}

    def ev_label(ev: Event) -> str:
        typ, pid = ev
        if typ == 'p':
            floor = next(p.pickup for p in passengers if p.id == pid)
            return f"{floor} (pickup {name_map[pid]})"
        else:
            floor = next(p.drop for p in passengers if p.id == pid)
            return f"{floor} (drop {name_map[pid]})"

    return f"{start} → " + " → ".join(ev_label(e) for e in events)


def parse_passengers_from_args(arg_list: Sequence[str]) -> List[Passenger]:
    passengers: List[Passenger] = []
    for i, token in enumerate(arg_list):
        if ':' not in token:
            raise ValueError(f"Passenger token must be pickup:drop (e.g. 2:1), got '{token}'")
        pickup_s, drop_s = token.split(':', 1)
        p = Passenger(id=i + 1, pickup=int(pickup_s), drop=int(drop_s), name=f"P{i+1}")
        passengers.append(p)
    return passengers


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', '-s', type=int, default=None, help='elevator start floor (e.g. 5)')
    parser.add_argument('--p', nargs='*', help='passengers as pickup:drop (e.g. 2:1 10:6 15:19)')

    args = parser.parse_args(argv)

    if args.start is None or not args.p:
        # interactive fallback
        print('Interactive mode — enter elevator start and passengers')
        start = int(input('Elevator start floor: ').strip())
        n = int(input('Number of passengers: ').strip())
        passengers: List[Passenger] = []
        for i in range(n):
            pickup = int(input(f'Passenger {i+1} pickup floor: ').strip())
            drop = int(input(f'Passenger {i+1} drop floor: ').strip())
            name = input(f'Passenger {i+1} name (optional): ').strip() or f'P{i+1}'
            passengers.append(Passenger(id=i + 1, pickup=pickup, drop=drop, name=name))
    else:
        start = args.start
        passengers = parse_passengers_from_args(args.p)

    # Validate basic constraints
    for p in passengers:
        if p.pickup == p.drop:
            print(f'Warning: passenger {p.name} pickup equals drop ({p.pickup}); ignoring passenger')
    passengers = [p for p in passengers if p.pickup != p.drop]

    if not passengers:
        print('No valid passengers to serve.')
        return

    print('\nScenario:')
    print(f'  Elevator at floor {start}')
    for p in passengers:
        print(f'  {p.name}: pickup {p.pickup} -> drop {p.drop}')

    best = find_best_sequences(start, passengers)

    print('\nBest sequences for each objective:')
    for key, res in best.items():
        if res is None:
            print(f'  {key}: no candidate found')
            continue
        print(f"\n== {key.replace('_', ' ').upper()} ==")
        print('Sequence:')
        print('  ' + format_events_readable(res['events'], passengers, start))
        print(f"Total travel: {res['total_travel']}")
        print(f"Avg pickup wait: {res['avg_pickup_wait']:.2f}, Max pickup wait: {res['max_pickup_wait']}")
        print(f"Avg arrival time: {res['avg_arrival_time']:.2f}, Max arrival time: {res['max_arrival_time']}")

    print('\nDone.')


if __name__ == '__main__':
    main()
