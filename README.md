## PicoBot: Python-based implementation of the PicoBot programming language

The script `picobot.py` provides a Python-based implementation of the [PicoBot programming language](https://www.cs.hmc.edu/csforall/Introduction/Introduction.html#picobot). The script supports the following command-line options:

```bash
> python picobot.py -h
usage: picobot.py [-h] -e ENV_FILE [-r RULES_FILE] [-b BOT_HOME]
                  [-n MAX_STEPS] [-g]

An implementation of the PicoBot programming language

optional arguments:
  -h, --help     show this help message and exit
  -e ENV_FILE    environment file
  -r RULES_FILE  rules file; default = rules are read from standard input
  -b BOT_HOME    starting cell (as "<row>, <col>") for the bot; default =
                 random non-wall cell
  -n MAX_STEPS   number of steps allowed for the bot; default = governed by
                 the rules
  -g             graphical output; default = terminal output
```

The files `env[1-7].txt` represent the seven environments (maps) that are supported by the online [PicoBot simulator](http://www.cs.hmc.edu/picobot/).

The file `rules.pb` is a sample PicoBot program that instructs a PicoBot to clean the cells that are above and to the left of its initial position.

## Software Dependencies

* [Python](https://www.python.org/) (2.7.6)
* [NumPy](http://www.numpy.org/) (1.8.2)
* [Matplotlib](http://matplotlib.org/) (1.3.1)

## Contact

If you have any questions about the software, please email swami.iyer@gmail.com.
