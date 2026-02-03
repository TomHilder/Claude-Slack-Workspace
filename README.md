# Conway's Game of Life

A colorful terminal-based implementation of **Conway's Game of Life** - the legendary cellular automaton created by mathematician John Conway in 1970.

```
╔══════════════════════════════════════════════════════════════════════════╗
║ Conway's Game of Life                                                    ║
╠══════════════════════════════════════════════════════════════════════════╣
║ ·····█·····································································║
║ ···█·█·····································································║
║ ··█·█·······██···························██·······························║
║ ·█···█······██···························██·······························║
║ ██···█·█····██·····························································║
║ ██···█···█····█·█··························································║
║ ·····█·····█·······························································║
╚══════════════════════════════════════════════════════════════════════════╝
```

## The Rules

The Game of Life follows four simple rules:

1. **Underpopulation**: Any live cell with fewer than 2 neighbors dies
2. **Survival**: Any live cell with 2 or 3 neighbors lives on
3. **Overpopulation**: Any live cell with more than 3 neighbors dies
4. **Reproduction**: Any dead cell with exactly 3 neighbors becomes alive

From these simple rules emerges incredible complexity!

## Quick Start

```bash
# Run the interactive menu
python -m src

# Run a specific pattern
python -m src --pattern glider_gun

# Random soup (chaotic fun!)
python -m src --random --density 0.35

# List all available patterns
python -m src --list-patterns
```

## Features

- **Colorful ASCII visualization** with animated display
- **13 famous patterns** including gliders, spaceships, and oscillators
- **Interactive menu** for easy exploration
- **Adjustable speed** (slow/normal/fast/ludicrous)
- **Customizable grid size**
- **Well-tested** (23 tests covering all game rules)

## Available Patterns

| Pattern | Type | Description |
|---------|------|-------------|
| `glider` | Spaceship | The famous glider - travels diagonally forever |
| `glider_gun` | Gun | Gosper's gun - shoots infinite gliders! |
| `lightweight_spaceship` | Spaceship | LWSS - travels horizontally |
| `blinker` | Oscillator | Simplest oscillator (period 2) |
| `toad` | Oscillator | Period 2 oscillator |
| `beacon` | Oscillator | Flashing period 2 oscillator |
| `pulsar` | Oscillator | Beautiful period 3 oscillator |
| `block` | Still Life | Completely stable 2x2 square |
| `beehive` | Still Life | Common stable pattern |
| `loaf` | Still Life | Another stable pattern |
| `r_pentomino` | Methuselah | Evolves chaotically for 1103 generations! |
| `diehard` | Methuselah | Disappears after exactly 130 generations |
| `acorn` | Methuselah | Grows for 5206 generations from 7 cells! |

## CLI Options

```
Usage: python -m src [OPTIONS]

Options:
  -p, --pattern PATTERN   Pattern to simulate
  -r, --random           Start with random cells
  -d, --density FLOAT    Density for random fill (0.0-1.0)
  -s, --speed SPEED      slow/normal/fast/ludicrous
  -g, --generations INT  Number of generations to run
  -W, --width INT        Grid width
  -H, --height INT       Grid height
  -l, --list-patterns    List available patterns
  -i, --interactive      Run interactive menu
  --no-color             Disable colored output
```

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## About

This project was created by Claude Code through Slack as a demonstration of emergent complexity from simple rules - just like the Game of Life itself!

## License

MIT License - see [LICENSE](LICENSE) for details.
