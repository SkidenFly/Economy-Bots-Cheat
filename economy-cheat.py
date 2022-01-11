import os
import yaml

import requests

import time
import random

class EconomyCheat():

    @property
    def get_config(self):
        with open("./config/config.yaml") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config

    def __init__(self):
        self.config = self.get_config

        self.token = self.config["TOKEN"]
        self.channels = self.config["CHANNELS"]

        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

        if not self.token:
            print("Error: Invalid token")
            os.system("pause")
            exit()
        
        if not self.channels:
            print("Error: No channels specified")
            os.system("pause")
            exit()
    
    @property
    def get_cooldown(self) -> int:
        cooldown = self.config["COOLDOWN"]
        
        if self.config["RANDOMIZED-COOLDOWN"]:
            return random.randint(cooldown, cooldown + self.config["RANDOMIZATION-RANGE"])
        else:
            return cooldown

    def send_sequences(self):
        for channel in self.channels:
            print(f"\nStarting sequence in channel {channel}")
            
            for command in self.channels[channel]["SEQUENCE"]:
                request = requests.post(
                    url= f"https://discordapp.com/api/v6/channels/{channel}/messages", 
                    headers= self.headers, 
                    json= {"content": self.channels[channel]["PREFIX"] + command}
                )

                if request.status_code != 200:
                    print(f"Error: {request.status_code}")
                    print(request.json())
                    break
                
                print(f"Command: {command} sended!".rjust(5))
                time.sleep(self.channels[channel]["DELAY-PER-COMMAND"])

    def execute(self):
        while True:
            self.send_sequences()
            time.sleep(self.get_cooldown)

def main():
    cheat = EconomyCheat()
    cheat.execute()

if __name__ == "__main__":
    main()
