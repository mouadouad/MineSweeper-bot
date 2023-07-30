from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# empty_src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb3///97e3uVBMaVAAAAHklEQVQI12MIDQ0NARFBDAEMDFzkEl6rVq1i0AISAIlSC03msuDYAAAAAElFTkSuQmCC"
# one_src =   "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0AAP97e3u7pKrVAAAAJUlEQVQI12NYBQQMDQxAACUCgAQjiGAFEaIQLiYhGgojEHqBGAB4Gw2cMF3q+AAAAABJRU5ErkJggg=="
# two_src =   "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0AewB7e3vro336AAAANUlEQVQI12NYBQQMDQxAACFCQxkYGkNDHRgaA1gdgGJgIhQowRoCknUAygIZYCVgAqwNQQAA1rsQB7h1rwIAAAAASUVORK5CYII="
# three_src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb3/AAB7e3uBZQfoAAAAKUlEQVQI12NYBQQMDQxAACYaQ0PBhAOQywojWIFiIAIhBlICJiDaEAQAtlYPHU2zahQAAAAASUVORK5CYII="
# four_src =  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0AAHt7e3vZn4u5AAAAJklEQVQI12NYBQQMDQxAACFERWFECIxoDA11ABNAJUAuBsGARAAAgHoNeXfAhZYAAAAASUVORK5CYII="
# five_src =  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb17AAB7e3sERFEmAAAAKUlEQVQI12NYBQQMDQxAACYaQ0MdoEQAiBsAEYNIAJWwQgi4Oog2BAEA7gEQV+EiCoQAAAAASUVORK5CYII="
# six_src =    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0Ae3t7e3tXnVpnAAAAKklEQVQI12NYBQQMDQxAACFCQxkYGsFEAAOMgIo5ALmsEALMBSmGaEMQAOO9EHd34ZsRAAAAAElFTkSuQmCC"

empty_src = "///"
one_src = "AAP"
two_src = "Aew"
three_src = "/AA"
four_src = "AAH"
five_src = "7AA"
six_src = "Ae3"

#opening a window to play the game using selenium webdriver
my_url = "https://xn--dmineur-bya.eu/"
serv = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #keep the window open after finishing 
driver = webdriver.Chrome(service=serv, options=chrome_options)
driver.get(my_url)
driver.find_element(By.CLASS_NAME,"css-k8o10q").click() #accept cookies 
driver.set_window_size(1200, 1000)
#choose the difficulty
container = driver.find_element(By.ID, "difficulty")
container.click()
container.click()
#set the grid height and width
grid_height = 16
grid_width = 30

# -----------------creating an empties list that contains everything----------------------
def all_empties():
    empties = []
    for i in range(grid_height):
        for j in range(grid_width):
            empties.append((i, j))
    return empties

#--------------read new data from the game---------------------------------
def refresh(empties,numbers):
    new_empties = []
    #we make a new empties list because when we click we dont know whats empty and whats not so we check everything

    board = driver.find_element(By.ID, "board")
    cases = board.find_elements(By.TAG_NAME,"img")

    counter = 0
    # check for each previously empty case what value it has now by checking the img source of it
    for case in cases:

        #make i and j trackers to know the coordinates of the current case
        i = counter // grid_width
        j = counter % grid_width
        counter += 1
        place = (i,j)

        #comparing the img sources to know which number or still empty and updating the numbers dictionnary
        if place in empties:
            src = case.get_attribute("src")[81:84]
            if src == empty_src:
                new_empties.append(place)
            elif src == one_src:
                numbers[place] = 1
            elif src == two_src:
                numbers[place] = 2
            elif src == three_src:
                numbers[place] = 3
            elif src == four_src:
                numbers[place] = 4
            elif src == five_src:
                numbers[place] = 5
            elif src == six_src:
                numbers[place] = 6

    return new_empties, numbers

# -------------find adjacent cases-----------------------------------------
def adjacent(i, j):
    adjacentlist = []
    if i != 0:
        adjacentlist.append((i - 1, j))
        if j != 0:
            adjacentlist.append((i - 1, j - 1))
        if j != grid_width:
            adjacentlist.append((i - 1, j + 1))
    if i != grid_height:
        adjacentlist.append((i + 1, j))
        if j != 0:
            adjacentlist.append((i + 1, j - 1))
        if j != grid_width:
            adjacentlist.append((i + 1, j + 1))
    if j != 0:
        adjacentlist.append((i, j - 1))
    if j != grid_width:
        adjacentlist.append((i, j + 1))
    return adjacentlist

# -----------------click case----------------------------------------------
def click(i, j):
    x = i * grid_width + j
    driver.find_element(By.XPATH, "//div[@id='board']/img[{}]".format(x + 1)).click()
        
# -----------click empties list--------------------------------------------
def click_list(clickList, clicked):
    for i in clickList:
        if i not in clicked: #see if case not already clicked and click it
            click(*i)
            clicked.append(i) #add case to already clicked cases
            #dont remove clicked cases from empties because we want to check whats in there in the next refresh 
    return clicked

# -----------empties adjacent to a case------------------------------------
def num_empties(empties, adjacent):
    list_empties = []
    if empties == None:
        return list_empties
    for i in adjacent:
        if i in empties:
            list_empties.append(i)
    return list_empties

# -------------check available numbers that have empty adjacents-----------
def av_numb(empties, numbers):
    av_numb_list = []
    for n in numbers:
        if len(num_empties(empties, adjacent(*n))) > 0: 
            av_numb_list.append(n)
    return av_numb_list

# -------------place bombs-------------------------------------------------
def placeBombs(bombs, places, empties):
    for i in places: #places is a list where we want to place bombs
        bombs.append(i)
        empties.remove(i)
    return empties, bombs

# -------------bombs adjacent to a case------------------------------------
def num_bombs(bombs, adjacent):
    list_bombs = []
    for i in adjacent:
        if i in bombs:
            list_bombs.append(i)
    return list_bombs

# ---------------see if the number of empty cases adjacent to a number are equal to that number and place bombs-----
def check_for_bombs(numbers, bombs, empties, number): 
    #number contains the coordinates of the case we are on and numbers is a dictionnary contain the values
    adjacentV = adjacent(*number)
    num_emptiesV = num_empties(empties, adjacentV) # list of empty cases adjacent to this case
    #normal check if the number of empties adjacent equals to the number - (bombs that are already there) 
    if len(num_emptiesV) == numbers[number] - len(num_bombs(bombs, adjacentV)):
        return placeBombs(bombs, num_emptiesV, empties) #place bombs in all empty cases adjacent to this case and return empties and bombs list
    return empties, bombs

# ----------------see if the number of bombs adjacent is achieved and click OTHER empties-------
def check_if_maxed(numbers, bombs, empties, number, clicked):
    adjacentV = adjacent(*number)
    num_emptiesV = num_empties(empties, adjacentV) # list of empty cases adjacent to this case
    #check if number of bombs adjacent is equal to the number and click all the empty cases
    if len(num_bombs(bombs, adjacentV)) == numbers[number]:
        clicked = click_list(num_emptiesV, clicked) #return clicked list
    return clicked

# --------------------checking if the one with shared empties has clickable empties---------------------------------
def advanced_clicking(numbers, bombs, empties, number, clicked):
    shared, shared_em, len_bombs = shared_empties(numbers, bombs, empties, number) #find shared empties of a number with other numbers where all of the empties are included
    for item in shared:#iterate the numbers that share all the empties with the current number
        adjacentV = adjacent(*item)
        num_emptiesV = num_empties(empties, adjacentV)

        new_item = numbers[item] - len(num_bombs(bombs, adjacentV)) #rest of bombs needed by item
        new_number = numbers[number] - len_bombs #rest of bombs needed by current number

        if new_item <= new_number: # check if the bombs that the item needs are gonna be all provided by our current number 
            clicked = click_list([i for i in num_emptiesV if i not in shared_em], clicked) #click the empties of the item that aren't shared with the current number
    return clicked

# -----------------checking if the one with shared empties has bombs--------------------
def advanced_bombing(numbers, bombs, empties, number):
    shared, my_empties, len_bombs = shared_empties2(numbers, bombs, empties, number) #find shared empties of a number with other numbers where not all of the empties are included
    for item in shared:#iterate the numbers that have shared empties with current number
        adjacentV = adjacent(*item)
        num_emptiesV = num_empties(empties, adjacentV)

        new_item = numbers[item] - len(num_bombs(bombs, adjacentV)) #rest of bombs needed by item
        new_number = numbers[number] - len_bombs #rest of bombs needed by current number
        nb_of_not_shared_empties = len(num_emptiesV) - shared[item] #the number of empties of the item that aren't shared with the current number

        #see if we put bombs on all of the not shared empties of the item with the current number, the rest of required bombs for item can still satisfy the number
        if new_item - nb_of_not_shared_empties == new_number and new_item > new_number: 
            return placeBombs(bombs, [i for i in num_emptiesV if i not in my_empties], empties) #place bombs in the empties of the item that aren't shared with the current number
    return empties, bombs

# ---------------------find shared empties of a number with other numbers where all of the empties are included-------------
def shared_empties(numbers, bombs, empties, number):
    adjacentV = adjacent(*number)
    num_emptiesV = num_empties(empties, adjacentV)
    num_bombsV = num_bombs(bombs, adjacentV)
    dict_of_numbers = {}
    result_list = []
    for empty in num_emptiesV:
        for i in adjacent(*empty): #check the adjacent cases of each empty case and find if it is a number
            if i in numbers and i != number:
                if i in dict_of_numbers: #if it is a number and not the number we are working on and add it to the dictionnary or add 1 
                    dict_of_numbers[i] += 1
                else:
                    dict_of_numbers[i] = 1
                #the dictionnary contains how many shared empties the numbers have with the working number > 0
    for number in dict_of_numbers:#check for the numbers that we found have shared empties with our number, share all the empties with him
        if dict_of_numbers[number] == len(num_emptiesV):
            result_list.append(number)
    return result_list, num_emptiesV, len(num_bombsV)

# ---------------------find shared empties of a number with other numbers where not all of the empties are included-------------
def shared_empties2(numbers, bombs, empties, number):
    adjacentV = adjacent(*number)
    num_emptiesV = num_empties(empties, adjacentV)
    num_bombsV = num_bombs(bombs, adjacentV)
    dict_of_numbers = {}
    for empty in num_emptiesV: #check the adjacent cases of each empty case and find if it is a number
        for i in adjacent(*empty):
            if i in numbers and i != number:
                if i in dict_of_numbers: #if it is a number and not the number we are working on and add it to the dictionnary or add 1 
                    dict_of_numbers[i] += 1
                else:
                    dict_of_numbers[i] = 1
                #the dictionnary contains how many shared empties the numbers have with the working number > 0
    return dict_of_numbers, num_emptiesV, len(num_bombsV) 

# -------------MAIN--------------------------------------------------------
def main():
    
    #click the middle of the grid
    click(grid_height // 2, grid_width // 2)
    
    #creating the start empties list that contains everything and the numbers dictionnary and bombs list
    empties, numbers = refresh(all_empties(), {})
    bombs = []

    #while there is empty cases
    while len(empties) > 0 :
        #making a temporary bombs list to see if the list is updated and know if we are stuck
        temp = bombs.copy()
        for number in av_numb(empties, numbers): #checking for bombs and updating the empties and bombs list
            empties, bombs = check_for_bombs(numbers, bombs, empties, number)
            empties, bombs = advanced_bombing(numbers, bombs, empties, number)

        #clicking cases and updating clicked list
        clicked = []
        for number in av_numb(empties, numbers):
            clicked = check_if_maxed(numbers, bombs, empties, number, clicked)
            clicked = advanced_clicking(numbers, bombs, empties, number, clicked)

        #see if stuck by checking if bombs list and clicked list aren't updated
        if temp == bombs and clicked == []:
            print("am stuck ")
            break

        # check if lost       
        lost = driver.find_element(By.ID, "face")
        if lost.get_attribute("src")[107:108] == "U":
            print("YOUU LOST")
            break

        # get the new empties and numbers from the game 
        empties, numbers = refresh(empties, numbers)

    print("exit")

main()
