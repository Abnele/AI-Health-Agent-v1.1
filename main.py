# Runner
import json
from input import get_user_data, save_data, load_data
from logic import analyze

def main():
    data = get_user_data()
    save_data(data)
    reccomendations = analyze()

    print("=== DAILY REPORT ===")
    for advice in reccomendations:
        print("- " + advice)



if __name__ == "__main__":
    main()