import sys as M_SYS
from module.command_modules import BREAK_DOWN_PARAMETERS;
from commands import add as ADD;
from commands import list as LIST;
from commands import create as CREATE;
from commands import delete as DELETE;
from commands import get as GET;
# ----------------- #
#     CALIBRATE     #
# ----------------- #
Commands = {
    "list": LIST.LIST,
    "add": ADD.ADD,
    "create": CREATE.CREATE,
    "open": CREATE.OPEN,
    "delete": DELETE.DELETE,
    "close": DELETE.CLOSE,
    "get": GET.GET
};
# ---------------------------------------- #
#          FUNCTION CONTINUATION           #
def PARSE_ARGUEMENT(ARGUEMENTS: list) -> type:
    for arg in ARGUEMENTS[1:]:
        if arg in Commands:
            Commands[arg](BREAK_DOWN_PARAMETERS(PARAMETER=ARGUEMENTS, START=arg));

PARSE_ARGUEMENT(M_SYS.argv);
#print(M_SYS.argv);
