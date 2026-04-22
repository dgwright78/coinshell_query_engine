DATA_DIR = "data/"

DB_FILE = DATA_DIR + "coins.db"
MONARCH_FILE = DATA_DIR + "monarchs.csv"
GRADES_FILE = DATA_DIR + "grades.csv"
DENOMS_FILE = DATA_DIR + "denoms.csv"
METALS_FILE = DATA_DIR + "metals.csv"

COMMANDS = [
    "date",
    "year",
    "before",
    "after",
    "monarch",
    "denomination",
    "metal",
    "silver",
    #"silverweight",
    "grade",
    "mintmark",
    "variety",
    "fineness",
    "weight",
    "sort",
    "and",
    "count",
    "random",
    "limit",
    "help",
    "quit",
]

TYPE_WORDS = {"random", "count", "show", "and", "limit", "help"}
STOP_WORDS = {"and", "sort", "count", "limit", "random", "quit", "show", "help"}

TOKEN_ALIASES = {
    "date": "year",
    "denom": "denomination",
    "mint": "mintmark",
    "var": "variety"
}

ALLOWED_SORT_COLUMNS = {"year", "denomination", "monarch", "metal", "fineness", "mintmark", "variety", "grade"}