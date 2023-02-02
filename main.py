from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from champ_data import get_champs
from selenium import webdriver
import random
import time

def init():
    options = Options()
    options.binary_location = "/usr/bin/firefox"
    options.headless = False # set option headless
    
    driver = webdriver.Firefox(options=options, executable_path="/home/janseuwu/Documents/geckodriver")
    driver.implicitly_wait(10)
    driver.get("https://loldle.net/classic") 
    
    cookies_path = "/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/button[1]/p"
    cookies = driver.find_element(By.XPATH, cookies_path)
    cookies.click() 

    super_brain(driver)
    
def super_brain(driver):
    champs = get_champs()
    name = 1 # index where the name of the champion is, index 0 is the id
    guesses = []
    good_squares = [] # correct guesses
    partial_squares = [] # partially correct guesses
    bad_squares = [] # wrong guesses
    superior_squares = [] # means the champion is newer
    inferior_squares = [] # means the champion is older

    input_field_path = "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[1]/div[1]/div/input"
    input_field = driver.find_element(By.XPATH, input_field_path)
    submit_button_path = "/html/body/div[1]/div[4]/div/div[2]/div[1]/div[2]"
    guessed = False

    while not guessed:
        # guess a champ
        print("champ list:\n", champs)
        boop = random.randint(0,len(champs)-1)
        champion = champs[boop][name]
        input_field.send_keys(champion)
        driver.find_element(By.XPATH, submit_button_path).click()
        guesses.append(champion)
        champs.pop(boop)
        time.sleep(6) # time it takes for all the squares to show

        newest_guess = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[2]/div[4]/div[3]/div[last()]")
        newest_guess_squares_container = newest_guess.find_element(By.CLASS_NAME, "square-container")
        squares = newest_guess_squares_container.find_elements(By.CLASS_NAME, "square")
        squares.pop(0) # removes the first element, it's empty
        for i, square in enumerate(squares):
            answer_state = square.get_attribute("class")

            if "square-bad" in answer_state and square.text not in bad_squares:
                print("bad square found")
                bad_squares.append(square.text)

            if "square-partial" in answer_state and square.text not in partial_squares:
                partial_squares.append(square.text)

            if "square-good" in answer_state and square.text not in good_squares:
                good_squares.append(square.text)
            
            # 'release year' squares are handled down here due to being different
            if "square-superior" in answer_state and square.text not in superior_squares:
                bad_squares.append(square.text)
                superior_squares.append(square.text)

            if "square-inferior" in answer_state and square.text not in inferior_squares:
                bad_squares.append(square.text)
                inferior_squares.append(square.text)

        def champ_sorting():
            for bad_criteria in bad_squares:
                for champ in champs:
                    i = champs.index(champ)
                    if bad_criteria in champ:
                        champs.pop(i)
                        champ_sorting()

            #TODO fix, doesn't work properly for whatever reason, deletes the entire list after like 3 tries
            # for good_criteria in good_squares:
            #     for champ in champs:
            #         i = champs.index(champ)
            #         print(good_criteria)
            #         print(champ)
            #         if good_criteria not in champ:
            #             champs.pop(i)
            #             champ_sorting()

            for year in superior_squares:
                for champ in champs:
                    if int(year) in champ or champ[8] < int(year):
                        i = champs.index(champ)
                        champs.pop(i)
                        champ_sorting()
            
            for year in inferior_squares:
                for champ in champs:
                    if int(year) in champ or champ[8] > int(year):
                        i = champs.index(champ)
                        champs.pop(i)
                        champ_sorting()
        champ_sorting()

if __name__ == "__main__":
    init()
