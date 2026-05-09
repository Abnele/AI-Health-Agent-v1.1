# Runner
import json
from input import get_user_data, save_data, load_data
from logic import analyze
from settings import get_settings

def main():
    dummy_data = get_settings()
    data = get_user_data(dummy_data) # Get data
    save_data(data) # Add it to total data
    recommendations, report_type = analyze()


    print(f"=== {report_type} REPORT ===")
    for advice in recommendations:
        print("- " + advice) # Give advice



if __name__ == "__main__":
    main()