"""
Game of Life Visualizations
Creates beautiful matplotlib plots showing the Game of Life patterns in action
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import sys
sys.path.insert(0, '/home/user/Claude-Slack-Workspace')
from src.game_of_life import GameOfLife, PATTERNS


def game_to_array(game: GameOfLife, padding: int = 2) -> np.ndarray:
    """Convert game state to numpy array for visualization."""
    # Find bounds of alive cells
    if not game.alive_cells:
        return np.zeros((10, 10))

    rows = [c[0] for c in game.alive_cells]
    cols = [c[1] for c in game.alive_cells]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Create array with padding
    height = max_r - min_r + 1 + 2 * padding
    width = max_c - min_c + 1 + 2 * padding

    arr = np.zeros((height, width))
    for r, c in game.alive_cells:
        arr[r - min_r + padding, c - min_c + padding] = 1

    return arr


def create_pattern_showcase():
    """Create a showcase of all famous patterns."""
    fig, axes = plt.subplots(3, 4, figsize=(14, 10))
    fig.suptitle("Conway's Game of Life - Famous Patterns", fontsize=16, fontweight='bold', y=0.98)

    # Custom colormap - dark blue to cyan
    colors = ['#0a1628', '#00d4ff']
    cmap = LinearSegmentedColormap.from_list('life', colors)

    pattern_names = ['glider', 'blinker', 'toad', 'beacon',
                     'pulsar', 'lightweight_spaceship', 'block', 'beehive',
                     'loaf', 'r_pentomino', 'diehard', 'acorn']

    pattern_types = ['Spaceship', 'Oscillator', 'Oscillator', 'Oscillator',
                     'Oscillator', 'Spaceship', 'Still Life', 'Still Life',
                     'Still Life', 'Methuselah', 'Methuselah', 'Methuselah']

    for idx, (ax, name, ptype) in enumerate(zip(axes.flat, pattern_names, pattern_types)):
        game = GameOfLife(50, 50)
        game.add_pattern(PATTERNS[name], 10, 10)
        arr = game_to_array(game, padding=1)

        ax.imshow(arr, cmap=cmap, interpolation='nearest', aspect='equal')
        ax.set_title(f"{name.replace('_', ' ').title()}\n({ptype})", fontsize=10)
        ax.axis('off')

        # Add border
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#00d4ff')
            spine.set_linewidth(2)

    plt.tight_layout()
    plt.savefig('/home/user/Claude-Slack-Workspace/pattern_showcase.png',
                dpi=150, facecolor='#0a1628', edgecolor='none', bbox_inches='tight')
    plt.close()
    print("Saved pattern_showcase.png")


def create_glider_evolution():
    """Create visualization showing glider moving across generations."""
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    fig.suptitle("Glider Evolution - The Simplest Spaceship", fontsize=16, fontweight='bold', y=0.98)

    colors = ['#1a0a2e', '#ff6b6b']
    cmap = LinearSegmentedColormap.from_list('life', colors)

    game = GameOfLife(20, 20)
    game.add_pattern(PATTERNS['glider'], 2, 2)

    for idx, ax in enumerate(axes.flat):
        # Create fixed-size array centered on the action
        arr = np.zeros((12, 12))
        for r, c in game.alive_cells:
            if 0 <= r < 12 and 0 <= c < 12:
                arr[r, c] = 1

        ax.imshow(arr, cmap=cmap, interpolation='nearest', aspect='equal')
        ax.set_title(f"Gen {game.generation}", fontsize=11, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])

        # Add grid
        ax.set_xticks(np.arange(-0.5, 12, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 12, 1), minor=True)
        ax.grid(which='minor', color='#333', linewidth=0.5)

        game.step()

    plt.tight_layout()
    plt.savefig('/home/user/Claude-Slack-Workspace/glider_evolution.png',
                dpi=150, facecolor='#1a0a2e', edgecolor='none', bbox_inches='tight')
    plt.close()
    print("Saved glider_evolution.png")


def create_glider_gun_sequence():
    """Create visualization showing the Gosper Glider Gun in action."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle("Gosper Glider Gun - Infinite Glider Factory", fontsize=16, fontweight='bold', y=0.98)

    colors = ['#0d1117', '#39d353']
    cmap = LinearSegmentedColormap.from_list('life', colors)

    game = GameOfLife(70, 40)
    game.add_pattern(PATTERNS['glider_gun'], 5, 2)

    generations = [0, 15, 30, 60, 90, 120]

    for ax, target_gen in zip(axes.flat, generations):
        while game.generation < target_gen:
            game.step()

        arr = np.zeros((35, 60))
        for r, c in game.alive_cells:
            if 0 <= r < 35 and 0 <= c < 60:
                arr[r, c] = 1

        ax.imshow(arr, cmap=cmap, interpolation='nearest', aspect='equal')
        ax.set_title(f"Generation {game.generation}", fontsize=12, fontweight='bold')
        ax.axis('off')

    # Add legend
    fig.text(0.5, 0.02,
             "The Gosper Glider Gun (1970) was the first known finite pattern that produces an infinite stream of gliders",
             ha='center', fontsize=10, style='italic', color='#888')

    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig('/home/user/Claude-Slack-Workspace/glider_gun_sequence.png',
                dpi=150, facecolor='#0d1117', edgecolor='none', bbox_inches='tight')
    plt.close()
    print("Saved glider_gun_sequence.png")


def create_population_dynamics():
    """Create a plot showing population over time for different patterns."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Game of Life Population Dynamics", fontsize=16, fontweight='bold')

    # Plot 1: R-pentomino chaos
    game = GameOfLife(100, 100)
    game.add_pattern(PATTERNS['r_pentomino'], 50, 50)

    generations = []
    populations = []

    for _ in range(200):
        generations.append(game.generation)
        populations.append(game.population())
        game.step()

    ax1.fill_between(generations, populations, alpha=0.3, color='#ff6b6b')
    ax1.plot(generations, populations, color='#ff6b6b', linewidth=2)
    ax1.set_xlabel('Generation', fontsize=11)
    ax1.set_ylabel('Population', fontsize=11)
    ax1.set_title('R-Pentomino: Chaotic Growth from 5 Cells', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor('#1a1a2e')

    # Plot 2: Compare multiple patterns
    patterns_to_compare = ['acorn', 'diehard', 'r_pentomino']
    colors_list = ['#00d4ff', '#ff6b6b', '#ffd93d']

    for name, color in zip(patterns_to_compare, colors_list):
        game = GameOfLife(150, 150)
        game.add_pattern(PATTERNS[name], 75, 75)

        gens = []
        pops = []

        for _ in range(150):
            gens.append(game.generation)
            pops.append(game.population())
            game.step()

        ax2.plot(gens, pops, color=color, linewidth=2, label=name.replace('_', ' ').title())

    ax2.set_xlabel('Generation', fontsize=11)
    ax2.set_ylabel('Population', fontsize=11)
    ax2.set_title('Methuselah Patterns: Small Starts, Big Growth', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_facecolor('#1a1a2e')

    plt.tight_layout()
    plt.savefig('/home/user/Claude-Slack-Workspace/population_dynamics.png',
                dpi=150, facecolor='#16213e', edgecolor='none', bbox_inches='tight')
    plt.close()
    print("Saved population_dynamics.png")


if __name__ == "__main__":
    print("Generating Game of Life visualizations...")
    create_pattern_showcase()
    create_glider_evolution()
    create_glider_gun_sequence()
    create_population_dynamics()
    print("All visualizations complete!")
