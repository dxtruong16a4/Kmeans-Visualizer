LEVEL = {
    "NOSHOW"    : 0,
    "SUCCESS"   : 1,
    "ERROR"     : 2,
    "WARNING"   : 3
}

def show_msg(level, msg):
    if level == LEVEL["NOSHOW"]:
        return

    level_map = {
        LEVEL["SUCCESS"]: ("\033[92m[SUCCESS]\033[0m", msg),
        LEVEL["ERROR"]: ("\033[91m[ERROR]\033[0m", msg),
        LEVEL["WARNING"]: ("\033[93m[WARNING]\033[0m", msg),
    }

    if level in level_map:
        print(f"{level_map[level][0]} {level_map[level][1]}")
    else:
        print(f"\033[91m[ERROR]\033[0m Invalid level: {level}")

if __name__ == "__main__":
    # Example usage of show_msg function
    show_msg(LEVEL["SUCCESS"], "This is a success message.")
    show_msg(LEVEL["ERROR"], "This is an error message.")
    show_msg(LEVEL["WARNING"], "This is a warning message.")
    show_msg(LEVEL["NOSHOW"], "This message will not be shown.")
    show_msg(4, "This is an invalid level message.")