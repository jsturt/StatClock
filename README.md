# StatClock
### ***A set of python routines designed for analysing Team Fortress 2 console logs***

Console logs can be generated via the `con_logfile <filename>` console command. All text registered in the console that session is then output to a text file in the /tf/ subdirectory of the TF2 installation with the chosen filename.

These console outputs log each frag and each death along with information such as the weapon used, the players involved, and whether it was a critical hit or not. This is the information that `StatClock` parses.

**NB:** `StatClock` cannot measure or track:
- Damage
- Health
- Time

The program simply extracts kill/death information from the last game recorded in the console. This means that fine-grained information such as dpm, health remaining, etc. cannot be tracked (owing to the fact that they would require a server-side plugin).

Basic python skills are required to interface with the routines in order to extract what information you want. The routines are essentially wrappers for `pandas` calls and text processing, meaning one can focus on the abstracted information rather than indexing through dataframes.

An example analysis file `analysis.py` is provided alongside the routines (`statclock.py`) to demonstrate a simple use of the routines for analysing killstreak frequency over a single match. A sample logfile is also provided (`testdata.txt`).

#### Requries:
- `python` > 3.6 (verified with [`vermin`](https://github.com/netromdk/vermin))
- [`pandas`](https://pandas.pydata.org/)
- [`numpy`](https://numpy.org/)

#### TODO:
- Provide more filtering options 
- Provide more statistics methods 
- Add example plotting method
- Long-term statistics over serveral samples
