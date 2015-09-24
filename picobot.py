import argparse, csv, matplotlib.colors as colors, matplotlib.pyplot as plt, \
    numpy, random, sys, time

# Each cell in the environment can be one of the following.
EMPTY   = 0
WALL    = 1
VISITED = 2
BOT     = 3

def neighborhood(env, brow, bcol):
    """
    Given the environment matrix and the coordinates of the bot, returns the 
    neighborhood string. 
    """

    s = ""
    s += "N" if env[brow - 1][bcol] == WALL else "X"
    s += "E" if env[brow][bcol + 1] == WALL else "X"
    s += "W" if env[brow][bcol - 1] == WALL else "X"
    s += "S" if env[brow + 1][bcol] == WALL else "X"
    return s

def matching_rule(rules, state, neighborhood):
    """
    From the given list of rules, return the one that maches the given state 
    and neighborhood. Otherwise, return None.
    """

    if state in rules:
        for item in rules[state]:
            if neighborhood in item[1]:
                return item
    return None

def expand_rule(rule):
    """
    Return the set of rules obtained by replacing each wildcard in the given 
    rule by either X (blank) or the appropriate direction (N, E, W, or S) 
    symbol. For example, N*WS yields NEWS and NXWS.
    """

    rules = set()
    for n in "NX":
        for e in "EX":
            for w in "WX":
                for s in "SX":
                    l = list(rule)
                    l[0] = n if l[0] == "*" else l[0]
                    l[1] = e if l[1] == "*" else l[1]
                    l[2] = w if l[2] == "*" else l[2]
                    l[3] = s if l[3] == "*" else l[3]
                    rules.add("".join(l))
    return rules

def main(args):
    """
    Entry point.
    """

    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description = """An implementation of the 
    PicoBot programming language""")
    parser.add_argument("-e", dest = "env_file", type = str, 
                        required = True, default = None, 
                        help = """environment file""")
    parser.add_argument("-r", dest = "rules_file", type = str, 
                        required = False, default = None, 
                        help = """rules file; 
                        default = rules are read from standard input""")
    parser.add_argument("-b", dest = "bot_home", type = str, 
                        required = False, default = None, 
                        help = """starting cell (as "<row>, <col>") for 
                        the bot; default = random non-wall cell""")
    parser.add_argument("-n", dest = "max_steps", type = int, 
                        required = False, default = None, 
                        help = """number of steps allowed for the bot; 
                        default = governed by the rules""")
    parser.add_argument("-g", action = "store_true", default = False, 
                        help = """graphical output; 
                        default = terminal output""")
    args = parser.parse_args()

    # Create the environment for the bot.
    M = list(csv.reader(open(args.env_file, "r"), delimiter = " "))
    env = numpy.ones((numpy.shape(M)[0] + 2, numpy.shape(M)[1] + 2), 
                     dtype = 'int')
    nrows, ncols = numpy.shape(env)
    for i in range(1, nrows - 1):
        for j in range(1, ncols - 1):
            env[i, j] = M[i - 1][j - 1]

    # Read the rules.
    rules = {}
    lines = sys.stdin.readlines() if args.rules_file == None else \
            open(args.rules_file, "r").readlines()
    for line in lines:
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        a, b, c, d, e = line.split()[:5]
        rule = b.upper()
        rules.setdefault(int(a), [])
        rules[int(a)].append((rule, expand_rule(rule), d.upper(), int(e)))

    # Initialize starting cell for the bot.
    if args.bot_home == None:
        bhome = random.randint(1, (nrows - 2) * (ncols - 2))
        while env[(bhome - 1) / (ncols - 2) + 1, (bhome - 1) % (ncols - 2)]:
            bhome = random.randint(1, (nrows - 2) * (ncols - 2))
        brow, bcol = (bhome - 1) / (ncols - 2) + 1, (bhome - 1) % (ncols - 2)
    else:
        brow, bcol = map(int, args.bot_home.split(","))
        if brow < 1 or brow > nrows - 2 or bcol < 1 or bcol > ncols - 2:
            sys.exit("Error: bot_home = (%s) is invalid!" %(args.bot_home))
        if env[brow, bcol] == WALL:
            sys.exit("Error: bot_home = (%s) is a wall!" %(args.bot_home))
    env[brow, bcol] = VISITED

    # Check for repeat rules.
    for state in rules.keys():
        for i in range(0, len(rules[state])):
            a = rules[state][i]
            for j in range(i + 1, len(rules[state])):
                b = rules[state][j]
                if not a[1].intersection(b[1]) == set():
                    sys.exit("Error: repeat rules %s and %s in state %d!" \
                             %(a[0], b[0], state))

    # Bot dynamics.
    prev_rule, rule = None, None
    prev_state, state = 0, 0
    prev_brow, prev_bcol = brow, bcol
    steps = 0
    visited = sum([1 for j in range(ncols) 
                   for i in range(nrows) if env[i, j] == EMPTY])
    if args.g:
        cmap = colors.ListedColormap(['white', 'blue', 'grey', 'green'])
        fig = plt.figure(1, figsize = (9, 9))
        fig.canvas.set_window_title("PicoBot")
        plt.ion()
        plt.draw()
    while True:
        steps += 1
        nhood = neighborhood(env, brow, bcol)
        mrule = matching_rule(rules, state, nhood)
        prev_brow, prev_bcol = brow, bcol
        if mrule == None:
            sys.exit("Error: no rule for state %d and neighborhood %s!" \
                     %(state, nhood))
        prev_rule = rule
        prev_state = state
        rule, action, state = mrule[0], mrule[2], mrule[3]
        if action == 'N':
            if env[brow - 1, bcol] == WALL:
                print("Error: cannot move to the north!")
                break
            brow -= 1
        elif action == 'E':
            if env[brow, bcol + 1] == WALL:
                print("Error: cannot move to the east!")
                break
            bcol += 1
        elif action == 'W':
            if env[brow, bcol - 1] == WALL:
                print("Error: cannot move to the west!")
                break
            bcol -= 1
        elif action == 'S':
            if env[brow + 1, bcol] == WALL:
                print("Error: cannot move to the south!")
                break
            brow += 1
        else:
            pass
        if not env[brow, bcol] == VISITED:
            env[brow, bcol] = VISITED
            visited -= 1
        msg = "bot at: (%d, %d), cells left: %d" %(brow, bcol, visited)
        if args.g:
            plt.subplot(111).clear()
            envp = env.copy()
            envp[brow, bcol] = BOT
            plt.title(msg)
            plt.imshow(envp[1:nrows - 1, 1:ncols - 1], cmap = cmap, 
                       interpolation = "nearest")
            plt.axis("off")
            plt.draw()
            time.sleep(0.01)
        else:
            print(msg)
        if visited == 0:
            print("Coverage reached!")
            break
        if prev_state == state and prev_rule == rule and \
           prev_brow == brow and prev_bcol == bcol:
            print("Bot stopped!")
            break
        if not args.max_steps == None and steps >= args.max_steps:
            print("Max. steps reached!")
            break

    if args.g:
        plt.show(block = True)
        plt.close(1)

if __name__ == "__main__":
    main(sys.argv[1:])
