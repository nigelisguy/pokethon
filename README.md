# Pokethon

Pokethon is a terminal-based Pokémon-style battle game and Pokédex simulator. Choose and train original 151 Pokémon with stats and moves directly inspired by Generation 1, then battle them head-to-head in real-time combat!

## Features

- **Terminal-based Battle System**: Fight classic Pokémon in an interactive curses-based UI
- **Full Pokédex**: Stats for all original 151 Pokémon with type advantages
- **Move System**: Over 150+ moves with unique effects and descriptions  
- **Customizable Battles**: Select your Pokémon and move sets before battle
- **Text-speed Settings**: Adjust text output speed to your preference

## Project Structure

- **main.py** - Main menu and settings interface
- **fightui.py** - Battle system with UI, team selection, and battle menus
- **stats.py** - Pokémon and move data definitions
- **README.md** - This file

## Getting Started

### Requirements
- Python 3.8 or higher
- Linux, macOS, or Windows with terminal support (curses)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nigelisguy/pokethon.git
   cd pokethon
   ```

2. Run the game:
   ```bash
   python main.py
   ```

## How to Play

1. **Main Menu**: Use arrow keys (↑/↓) to navigate and press `Z` to select
   - **FightTest**: Start a battle between two randomly selected teams
   - **Pokedex**: Browse all 151 Pokémon and view their stats
   - **Settings**: Adjust text speed
   - **Exit**: Press `Z` to exit

2. **Team Selection**:
   - Select your Pokémon using arrow keys and press `Z` to confirm
   - Choose 4 moves for each Pokémon
   - Press `Z` again to start the battle

3. **Battle Controls**:
   - Navigate options with arrow keys
   - Press `Z` to select an action (Fight, Bag, Pokémon, Run)
   - Battle mechanics are turn-based

4. **Pokedex**:
   - Scroll through all Pokémon with arrow keys
   - Press `Z` to view detailed stats for each Pokémon

## Controls

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate menus |
| ← → | Adjust settings (text speed) |
| Z   | Select / Confirm |
| Q   | Quit / Go back |

## Gameplay Tips

- Each Pokémon has different stats (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed)
- Type advantages affect move effectiveness
- Different moves have different power, accuracy, and special effects
- Speed stat determines who attacks first in battle
- Experiment with different move combinations for optimal strategies

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- New Pokémon mechanics (evolutions, abilities)
- Battle features (status effects, critical hits)
- UI improvements and visual polish
- Code refactoring and optimization
- Bug fixes and issue reports

## Development Notes

### Code Improvements in Progress
- [ ] Refactor stats.py to use dataclasses for better readability
- [ ] Add type hints throughout the codebase
- [ ] Extract magic numbers into configuration constants
- [ ] Improve error handling and edge cases
- [ ] Add unit tests for game logic
- [ ] Modularize UI components for reusability

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the original Pokémon games
- Built with Python's `curses` library for terminal UI

## Roadmap

- [ ] Online multiplayer battles
- [ ] Pokémon evolution system
- [ ] Item system with bag management
- [ ] Save/load game progress
- [ ] Trainer battles with AI opponents
- [ ] Generation 2+ Pokémon and moves
- [ ] Web-based version

---

**Status**: Still extremely unfinished, but playable! Contributions welcome to help complete the project.