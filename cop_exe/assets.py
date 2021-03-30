CREDITS: str
with open('cop_exe/credits.txt', 'r') as fp:
    CREDITS = fp.read().strip()

HELP_TEXT: str
with open('cop_exe/help.txt', 'r') as fp:
    HELP_TEXT = fp.read().strip()
