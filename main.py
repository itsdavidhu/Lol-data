from lol_data import LolData
from analysis import LolAnalysis

def collect_data():
    """
    Function to collect all necessary data for analysis.
    """
    lol_data = LolData()
    lol_data.load_general_accounts()
    lol_data.load_high_elo_accounts()
    lol_data.load_general_matches()
    lol_data.load_high_elo_matches()
    lol_data.load_general_match_data()
    lol_data.load_high_elo_match_data()
    lol_data.verify_data()

def main():
    lol_analysis = LolAnalysis()
    lol_analysis.breaks()

if __name__ == "__main__":
    main()
    