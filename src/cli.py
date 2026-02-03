#!/usr/bin/env python3
"""
Command-line interface for Conway's Game of Life.

Usage:
    python -m src.cli [OPTIONS]

Examples:
    python -m src.cli --pattern glider_gun
    python -m src.cli --random --density 0.4
    python -m src.cli --pattern pulsar --speed fast
    python -m src.cli --list-patterns
"""

import argparse
import sys

from .game_of_life import (
    GameOfLife,
    PATTERNS,
    render,
    run_simulation,
    Colors,
    clear_screen,
)


SPEED_PRESETS = {
    "slow": 0.3,
    "normal": 0.15,
    "fast": 0.08,
    "ludicrous": 0.02,
}


def show_banner() -> None:
    """Display a fancy ASCII art banner."""
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   {Colors.GREEN}  ██████╗  █████╗ ███╗   ███╗███████╗                     {Colors.CYAN}║
║   {Colors.GREEN} ██╔════╝ ██╔══██╗████╗ ████║██╔════╝                     {Colors.CYAN}║
║   {Colors.GREEN} ██║  ███╗███████║██╔████╔██║█████╗                       {Colors.CYAN}║
║   {Colors.GREEN} ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝                       {Colors.CYAN}║
║   {Colors.GREEN} ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗                     {Colors.CYAN}║
║   {Colors.GREEN}  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝                     {Colors.CYAN}║
║                                                               ║
║   {Colors.YELLOW}  ██████╗ ███████╗    ██╗     ██╗███████╗███████╗        {Colors.CYAN}║
║   {Colors.YELLOW} ██╔═══██╗██╔════╝    ██║     ██║██╔════╝██╔════╝        {Colors.CYAN}║
║   {Colors.YELLOW} ██║   ██║█████╗      ██║     ██║█████╗  █████╗          {Colors.CYAN}║
║   {Colors.YELLOW} ██║   ██║██╔══╝      ██║     ██║██╔══╝  ██╔══╝          {Colors.CYAN}║
║   {Colors.YELLOW} ╚██████╔╝██║         ███████╗██║██║     ███████╗        {Colors.CYAN}║
║   {Colors.YELLOW}  ╚═════╝ ╚═╝         ╚══════╝╚═╝╚═╝     ╚══════╝        {Colors.CYAN}║
║                                                               ║
║   {Colors.MAGENTA}Conway's Cellular Automaton - A Mathematical Universe{Colors.CYAN}     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def list_patterns() -> None:
    """Display available patterns with descriptions."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}Available Patterns:{Colors.RESET}\n")

    descriptions = {
        "glider": "The famous glider - a spaceship that travels diagonally",
        "blinker": "Simplest oscillator - period 2",
        "toad": "Period 2 oscillator",
        "beacon": "Period 2 oscillator with a flashing effect",
        "pulsar": "Beautiful period 3 oscillator - mesmerizing!",
        "glider_gun": "Gosper's glider gun - creates infinite gliders!",
        "lightweight_spaceship": "A small spaceship (LWSS) that travels horizontally",
        "r_pentomino": "Small but chaotic - evolves for 1103 generations!",
        "diehard": "Disappears after exactly 130 generations",
        "acorn": "Tiny pattern that grows for 5206 generations!",
        "block": "Simplest still life - completely stable",
        "beehive": "Common still life",
        "loaf": "Another common still life",
    }

    for name, desc in descriptions.items():
        pattern = PATTERNS.get(name, [])
        height = len(pattern)
        width = max(len(row) for row in pattern) if pattern else 0
        print(f"  {Colors.GREEN}{name:22}{Colors.RESET} ({width}x{height}) - {desc}")

    print(f"\n{Colors.DIM}Use --pattern <name> to run a specific pattern{Colors.RESET}\n")


def interactive_menu() -> None:
    """Show an interactive menu for pattern selection."""
    clear_screen()
    show_banner()

    print(f"\n{Colors.HEADER}Select a demo:{Colors.RESET}\n")
    print(f"  {Colors.GREEN}1.{Colors.RESET} Glider Gun (infinite gliders!)")
    print(f"  {Colors.GREEN}2.{Colors.RESET} Random Soup (chaotic life)")
    print(f"  {Colors.GREEN}3.{Colors.RESET} Pulsar (beautiful oscillator)")
    print(f"  {Colors.GREEN}4.{Colors.RESET} Acorn (small seed, huge growth)")
    print(f"  {Colors.GREEN}5.{Colors.RESET} R-pentomino (legendary chaos)")
    print(f"  {Colors.GREEN}6.{Colors.RESET} Spaceship Fleet")
    print(f"  {Colors.GREEN}7.{Colors.RESET} Pattern Zoo (multiple patterns)")
    print(f"  {Colors.GREEN}q.{Colors.RESET} Quit")

    choice = input(f"\n{Colors.CYAN}Enter choice (1-7 or q): {Colors.RESET}").strip().lower()

    game = GameOfLife(70, 30)

    if choice == '1':
        game.add_pattern(PATTERNS["glider_gun"], 2, 2)
    elif choice == '2':
        game.randomize(0.35)
    elif choice == '3':
        game.add_pattern(PATTERNS["pulsar"], 8, 28)
    elif choice == '4':
        game.add_pattern(PATTERNS["acorn"], 15, 35)
    elif choice == '5':
        game.add_pattern(PATTERNS["r_pentomino"], 15, 35)
    elif choice == '6':
        # Fleet of spaceships!
        for i in range(5):
            game.add_pattern(PATTERNS["lightweight_spaceship"], 3 + i * 5, 5)
            game.add_pattern(PATTERNS["glider"], 5 + i * 5, 50)
    elif choice == '7':
        # Pattern zoo
        game.add_pattern(PATTERNS["glider"], 2, 5)
        game.add_pattern(PATTERNS["blinker"], 5, 20)
        game.add_pattern(PATTERNS["toad"], 10, 5)
        game.add_pattern(PATTERNS["beacon"], 10, 20)
        game.add_pattern(PATTERNS["pulsar"], 15, 30)
        game.add_pattern(PATTERNS["block"], 3, 60)
        game.add_pattern(PATTERNS["beehive"], 8, 55)
        game.add_pattern(PATTERNS["loaf"], 12, 60)
    elif choice == 'q':
        print(f"\n{Colors.MAGENTA}Thanks for playing! Life finds a way...{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.YELLOW}Invalid choice. Running random soup!{Colors.RESET}")
        game.randomize(0.3)

    run_simulation(game, generations=500, delay=0.1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life - A cellular automaton simulation",
        epilog="Example: python -m src.cli --pattern glider_gun --speed fast"
    )

    parser.add_argument(
        "--pattern", "-p",
        choices=list(PATTERNS.keys()),
        help="Pattern to simulate"
    )
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Start with random cells"
    )
    parser.add_argument(
        "--density", "-d",
        type=float,
        default=0.3,
        help="Density for random fill (0.0 to 1.0, default: 0.3)"
    )
    parser.add_argument(
        "--speed", "-s",
        choices=list(SPEED_PRESETS.keys()),
        default="normal",
        help="Simulation speed (default: normal)"
    )
    parser.add_argument(
        "--generations", "-g",
        type=int,
        default=500,
        help="Number of generations to run (default: 500)"
    )
    parser.add_argument(
        "--width", "-W",
        type=int,
        default=70,
        help="Grid width (default: 70)"
    )
    parser.add_argument(
        "--height", "-H",
        type=int,
        default=30,
        help="Grid height (default: 30)"
    )
    parser.add_argument(
        "--list-patterns", "-l",
        action="store_true",
        help="List available patterns and exit"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run interactive menu"
    )

    args = parser.parse_args()

    # List patterns and exit
    if args.list_patterns:
        list_patterns()
        sys.exit(0)

    # Interactive menu
    if args.interactive:
        interactive_menu()
        sys.exit(0)

    # Create game
    game = GameOfLife(args.width, args.height)

    # Set up initial state
    if args.random:
        game.randomize(args.density)
    elif args.pattern:
        # Center the pattern
        pattern = PATTERNS[args.pattern]
        pattern_height = len(pattern)
        pattern_width = max(len(row) for row in pattern) if pattern else 0
        offset_row = max(0, (args.height - pattern_height) // 2)
        offset_col = max(0, (args.width - pattern_width) // 2)
        game.add_pattern(pattern, offset_row, offset_col)
    else:
        # Default: show interactive menu
        interactive_menu()
        sys.exit(0)

    # Run simulation
    delay = SPEED_PRESETS[args.speed]
    run_simulation(
        game,
        generations=args.generations,
        delay=delay,
        use_color=not args.no_color
    )


if __name__ == "__main__":
    main()
