import os
import time
from typing import List, Set
from colr import color as colr


class Blacklist:
    def __init__(self, log=None):
        self.log = log
        self.blacklist_file = "blacklist.txt"
        self.blacklisted_players: Set[str] = set()
        self.last_modified = 0
        self.load_blacklist()
    
    def load_blacklist(self):
        """Loads the blacklist from blacklist.txt"""
        try:
            if os.path.exists(self.blacklist_file):
                # Update last modified timestamp
                self.last_modified = os.path.getmtime(self.blacklist_file)
                
                with open(self.blacklist_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                self.blacklisted_players.clear()
                for line in lines:
                    line = line.strip()
                    # Ignore empty lines and comments
                    if line and not line.startswith('#'):
                        # Normalize the name format (convert to lowercase for comparison)
                        normalized_name = line.lower()
                        self.blacklisted_players.add(normalized_name)
                
                if self.log:
                    self.log(f"Blacklist loaded: {len(self.blacklisted_players)} players")
            else:
                if self.log:
                    self.log("File blacklist.txt not found, creating empty file")
                self._create_empty_blacklist()
                self.last_modified = os.path.getmtime(self.blacklist_file) if os.path.exists(self.blacklist_file) else 0
        except Exception as e:
            if self.log:
                self.log(f"Error loading blacklist: {str(e)}")
    
    def _create_empty_blacklist(self):
        """Create an empty blacklist.txt file with instructions"""
        try:
            with open(self.blacklist_file, 'w', encoding='utf-8') as f:
                f.write("# VALORANT Player Blacklist\n")
                f.write("# Add one nickname per line (format: PlayerName#TAG)\n")
                f.write("# Lines that start with # are comments and will be ignored\n")
                f.write("# Examples:\n")
                f.write("# ToxicPlayer#BR1\n")
                f.write("# Cheater#NA1\n")
                f.write("# AnotherBadPlayer#EU1\n\n")
        except Exception as e:
            if self.log:
                self.log(f"Error creating blacklist.txt: {str(e)}")
    
    def reload_blacklist(self):
        """Reload the blacklist from file (useful if the file is modified while running)"""
        self.load_blacklist()
    
    def is_blacklisted(self, player_name: str) -> bool:
        """Checks if a player is on the blacklist"""
        if not player_name:
            return False
        
        # Normalize name to compare (lowercase)
        normalized_name = player_name.lower()
        return normalized_name in self.blacklisted_players
    
    def _check_file_modified(self):
        """Checks if the file was modified and reloads if necessary"""
        try:
            if os.path.exists(self.blacklist_file):
                current_modified = os.path.getmtime(self.blacklist_file)
                if current_modified > self.last_modified:
                    if self.log:
                        self.log("File blacklist.txt was modified, reloading...")
                    self.load_blacklist()
        except Exception as e:
            if self.log:
                self.log(f"Error checking blacklist file modification: {str(e)}")

    def check_players(self, names_dict: dict) -> List[dict]:
        """
        Checks which players in the list are on the blacklist
        
        Args:
            names_dict: Dictionary with {puuid: "PlayerName#TAG"}
            
        Returns:
            List of dictionaries with information about blacklisted players
        """
        # Check if the file was modified before checking players
        self._check_file_modified()
        
        blacklisted_found = []
        
        for puuid, player_name in names_dict.items():
            if self.is_blacklisted(player_name):
                blacklisted_found.append({
                    'puuid': puuid,
                    'name': player_name
                })
        
        return blacklisted_found
    
    def print_blacklist_warning(self, blacklisted_players: List[dict], game_state: str = ""):
        """
        Prints colored warnings for found blacklisted players
        
        Args:
            blacklisted_players: List of found blacklisted players
            game_state: Current game state (INGAME, PREGAME, MENUS)
        """
        if not blacklisted_players:
            return
        
        # Warning header
        warning_header = colr("⚠️  BLACKLISTED PLAYERS DETECTED ⚠️", fore=(255, 0, 0), style='bold')
        print(f"\n{warning_header}")
        
        state_text = ""
        if game_state == "INGAME":
            state_text = colr("in the match", fore=(241, 39, 39))
        elif game_state == "PREGAME":
            state_text = colr("in agent select", fore=(103, 237, 76))
        elif game_state == "MENUS":
            state_text = colr("in your party", fore=(238, 241, 54))
        
        if state_text:
            print(f"Found {colr(str(len(blacklisted_players)), fore=(255, 255, 0), style='bold')} blacklisted player(s) {state_text}:")
        else:
            print(f"Found {colr(str(len(blacklisted_players)), fore=(255, 255, 0), style='bold')} blacklisted player(s):")
        
        # List players
        for player in blacklisted_players:
            player_name_colored = colr(player['name'], fore=(255, 100, 100), style='bold')
            print(f"  • {player_name_colored}")
        
        print()  # Blank line after the warning
    
    def get_blacklist_size(self) -> int:
        """Returns the number of players on the blacklist"""
        return len(self.blacklisted_players)
    
    def get_blacklisted_players(self) -> List[str]:
        """Returns a list with all blacklisted players"""
        return list(self.blacklisted_players)
