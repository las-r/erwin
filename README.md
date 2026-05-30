# Erwin
A quantum-inspired constraint satisfaction language that evaluates code by searching parallel realities over variable superpositions, collapsing invalid universes via constraints.

### Commands
| Command | Syntax | Description |
| --- | --- | --- |
| **`LET`** | `LET [var] [expr]` <br> `LET [var] super [min] [max]` | Assigns a static value **OR** initializes a variable into an integer superposition. |
| **`ENT`** | `ENT [target] [source] [op] [modifier]` | Entangles `target` value to `source` using a math modifier (`add`, `sub`, `mul`, `div`, `pow`). |
| **`PEP`** | `PEP [count] [var1] [var2] ...` | Pauli Exclusion Principle: Asserts the next `count` variables must have unique values. |
| **`CHK`** | `CHK [expr]` | Asserts a reality constraint. Fails/collapses the universe if `expr` evaluates to false. |
| **`OBS`** | `OBS [var]` | Observes and prints the finalized, collapsed value of a variable to stdout. |
| **`MUT`** | `MUT [var]` | Mutates reality by deleting the variable from the timeline. |

*Note: Expressions use **prefix (Polish) notation** (e.g., `add x y`, `eq b 6`, `gr x 6`).*

## Arithmetic & Boolean Logic
Erwin uses **prefix (Polish) notation** where operators precede their arguments (e.g., `add 1 2`).

* **Arithmetic:** `add`, `sub`, `mul`, `div`, `pow`, `floor`, `ceil`
* **Comparisons:** `eq` (=), `ls` (<), `gr` (>), `els` (<=), `egr` (>=)
* **Logicals:** `not`

## Usage
```bash
python erwin.py script.cat
python erwin.py script.cat -i  # Verbose
```