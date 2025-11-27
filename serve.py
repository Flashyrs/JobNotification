import threading
import time
import os

def run_bot():
    os.system("python bot.py")


def run_scraper_loop():
    while True:
        print("🔄 Running scheduled scraper...")
        os.system("python main.py")
        time.sleep(15 * 60)  

if __name__ == "__main__":

    t1 = threading.Thread(target=run_bot)
    t1.start()


    run_scraper_loop()
