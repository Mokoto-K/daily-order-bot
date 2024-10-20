from exchange import main as run_program
from data import main as update_csv

# TODO - I think im going to leave this for now, it's taken on a few different forms and shapes and
#  I havent been happy with any of them but i'm wasting to much time. This works for any algo that
#  you throw into the algo class, providing it returns a string of the direction for the next trade.
#  Until I build a better algo or have a better idea of how I want the flow of this to work, im done.

def main() -> None:
    update_csv()
    run_program()


if __name__ == "__main__":
    main()

