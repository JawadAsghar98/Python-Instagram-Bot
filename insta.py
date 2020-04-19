import random
import sys
import time
from hashlib import new

import autoit
from openpyxl.worksheet.dimensions import Dimension

from app import InstagramScraper
from instaloader import Instaloader
from selenium import webdriver
from selenium.webdriver.chrome.options import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC, ui
from selenium.webdriver.support.ui import WebDriverWait


def chrome_driver():
    browser = webdriver.Chrome("/Users/Jawad/Desktop/Automation/chromedriver.exe")
    # browser.minimize_window()
    browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    return browser


def signIn(browser):
    try:
        browser.implicitly_wait(20)
        emailInput = browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
        emailInput.send_keys("jawad.asghar@outlook.com")
        time.sleep(2)
        passwordInput = browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
        passwordInput.send_keys("Mjawad1998")
        time.sleep(2)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(1)
        popup_window(browser)
    except:
        print("Please Enter correct username and password to login and re-run the Program")
        time.sleep(3)
        sys.exit()


def popup_window(browser):
    popup = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]")
    popup.click()
    time.sleep(2)


def unfollow_user(browser, username):
    signIn(browser)
    search_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        )
    )
    search_box.send_keys(username)
    time.sleep(2)
    search_box.send_keys(Keys.ARROW_DOWN)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)

    try:
        a = browser.find_element_by_xpath("//button[contains(text(), 'Following')]")
        a.click()
        browser.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[1]").click()
        time.sleep(2)
        print("You successfully unfollow " + username)
        time.sleep(4)

    except:
        # browser.find_element_by_xpath("//button[contains(text(), 'Follow')]"):
        print("You are not following this user")
        time.sleep(10)
        # sys.exit()

    browser.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div").click()


def unfollow_users(browser, followers):
    signIn(browser)
    browser.find_element_by_css_selector(
        "#react-root > section > main > section > div.COOzN.MnWb5.YT6rB > div.m0NAq > div > div.RR-M-._2NjG_ > a").click()
    browser.find_element_by_css_selector(
        "#react-root > section > main > div > header > section > ul > li:nth-child(3)").click()
    for i in range(1, followers):
        str1 = "/html/body/div[4]/div/div[2]/ul/div/li["
        str2 = "]/div/div[3]"
        final_string = str1 + str(i) + str2
        browser.find_element_by_xpath(final_string).click()
        time.sleep(2)
        browser.find_element_by_css_selector(
            "body > div:nth-child(22) > div > div > div.mt3GC > button.aOOlW.-Cab_").click()
        time.sleep(2)
        # print('unfollow ' + final_string.get_attribute("text"))

        # print("You have no more followers to unfollow")


def comment_particular_picture(browser, search_tag, wComment, no_of_posts):
    signIn(browser)
    search_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        )
    )
    search_box.send_keys(search_tag)
    time.sleep(1)
    search_box.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    search_box = browser.find_element_by_xpath("//a[contains(@href, '/explore/tags/')]")
    search_box.send_keys(Keys.ENTER)
    delay = random.randint(1, 10)
    time.sleep(2)
    browser.find_element_by_css_selector(
        "#react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1) > a > div").click()
    commentSection = ui.WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
    browser.execute_script("arguments[0].scrollIntoView(true);", commentSection)
    i = 1
    while i < no_of_posts:
        try:
            commentSection = ui.WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
            commentSection.send_keys(wComment)
            commentSection.send_keys(Keys.ENTER)
            time.sleep(delay)
            browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
            time.sleep(delay)
            i += 1
        except:
            time.sleep(delay)


def like_particular_picture(browser, search_name, no_of_posts):
    signIn(browser)
    search_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        )
    )
    search_box.send_keys(search_name)
    time.sleep(1)
    search_box.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    search_box = browser.find_element_by_xpath("//a[contains(@href, '/explore/locations/')]")
    search_box.send_keys(Keys.ENTER)
    delay = random.randint(1, 10)
    time.sleep(2)
    browser.find_element_by_class_name("v1Nh3").click()
    i = 1
    while i < no_of_posts:
        time.sleep(delay)
        loc_set = browser.find_element_by_class_name("O4GlU")
        if search_name == loc_set.text:
            browser.find_element_by_class_name("fr66n").click()
            time.sleep(delay)
            browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
            time.sleep(delay)
            i += 1
        else:
            browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
            time.sleep(delay)
            i += 1


def another_user_followers(browser, acc_username, no_of_followers_to_follow):
    signIn(browser)
    search_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        )
    )
    search_box.send_keys(acc_username)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)
    try:
        browser.find_element_by_css_selector(
            "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a").click()
    except:
        print("This Account is Private or It is a Tag")
        browser.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div").click()
        sys.exit()
    time.sleep(2)
    browser.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
    time.sleep(2)
    browser.find_element_by_css_selector(
        "#react-root > section > main > div > header > section > ul > li:nth-child(2) > a").click()
    for i in range(1, no_of_followers_to_follow):
        followers_list = []
        str1 = "/html/body/div[4]/div/div[2]/ul/div/li["
        str2 = "]/div/div[3]"
        final_string = str1 + str(i) + str2
        a = browser.find_element_by_xpath(final_string)
        if i % 6 == 0:
            # followedPopup = browser.find_element_by_xpath("/html/body/div[4]/div/div[2]")
            followedPopup = browser.find_element_by_xpath("//div[@class='isgrP']")
            # followedPopup = WebDriverWait(browser, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//div[""@class='isgrP']")))
            #     browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followedPopup)
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                   followedPopup)
            time.sleep(1)
            # print(a)
            followers_list.append(a.text)
            time.sleep(1)

            print(followers_list)
        else:
            followers_list.append(a.text)
            time.sleep(1)
            print(followers_list)

        # a.click()
        # if browser.find_element_by_xpath("//button[text()='Cancel']").click():
        #     time.sleep(1)
        # fList = browser.find_elements_by_xpath("//div[@class='isgrP']//li")
        # print(followers_list)
        # print(fList)
        # time.sleep(2)

        # scr1 = browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
        # browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
        # print('try ' + final_string)
    time.sleep(2)
    # browser.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div").click()


def search_by_location(browser, search_name, no_of_posts):
    signIn(browser)
    search_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        )
    )
    search_box.send_keys(search_name)
    time.sleep(1)
    search_box.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    search_box = browser.find_element_by_xpath("//a[contains(@href, '/explore/locations/')]")
    search_box.send_keys(Keys.ENTER)
    delay = random.randint(1, 10)
    time.sleep(2)
    browser.find_element_by_class_name("v1Nh3").click()
    i = 1
    while i < no_of_posts:
        time.sleep(delay)
        browser.find_element_by_class_name("fr66n").click()
        time.sleep(delay)
        browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
        time.sleep(delay)
        i += 1


def unlike_posts(browser, search_tag, no_of_posts):
    signIn(browser)
    search_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        )
    )
    search_box.send_keys(search_tag)
    time.sleep(1)
    search_box.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    search_box = browser.find_element_by_xpath("//a[contains(@href, '/explore/tags/')]")
    search_box.send_keys(Keys.ENTER)
    delay = random.randint(1, 10)
    time.sleep(2)
    # downloading_images(browser)
    browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]").click()
    i = 1
    while i < no_of_posts:
        time.sleep(delay)
        browser.find_element_by_class_name("fr66n").click()
        time.sleep(delay)
        browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
        time.sleep(delay)
        i += 1

    # i = 1
    # # while i < no_of_posts:
    # time.sleep(delay)
    # # browser.find_element_by_xpath()
    # a = browser.get(browser.current_url + 'media')
    # time.sleep(3)
    # actionChains = ActionChains(browser)
    # actionChains.context_click(a).key_down(Keys.CONTROL).send_keys('s').perform()

    # a = browser.current_url()+'/media'
    # print(a)
    # unlike = browser.find_element_by_xpath("//*[@aria-label='Unlike']")
    # if unlike:
    #     unlike.click()
    # else:
    #     # browser.find_element_by_class_name("fr66n").click()
    #     time.sleep(delay)
    # browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
    # time.sleep(delay)
    # i += 1


def save_posts(browser, search_tag, no_of_posts):
    signIn(browser)
    delay = random.randint(1, 10)
    search_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
        )
    )
    search_box.send_keys(search_tag)
    time.sleep(1)
    search_box.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    search_box = browser.find_element_by_xpath("//a[contains(@href, '/explore/tags/')]")
    search_box.send_keys(Keys.ENTER)
    delay = random.randint(1, 10)
    time.sleep(2)
    browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]").click()
    i = 1
    while i < no_of_posts:
        time.sleep(delay)
        browser.find_element_by_class_name("wmtNn").click()
        time.sleep(delay)
        browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
        time.sleep(delay)
        i += 1


def unsave_posts(browser, no_of_posts):
    signIn(browser)
    browser.find_element_by_class_name("SKguc").click()
    delay = random.randint(1, 10)
    time.sleep(delay)
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/a[3]/span").click()
    time.sleep(2)
    try:
        browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/div[2]/article/div/div/div/div[1]/a/div[1]").click()
        time.sleep(delay)
    except:
        print("You have no Saved Post")
        time.sleep(delay)
        sys.exit()

    i = 1
    while i < no_of_posts:
        browser.find_element_by_class_name("wmtNn").click()
        time.sleep(delay)
        try:
            browser.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
        except:
            browser.find_element_by_xpath("/html/body/div[4]/div[3]/button").click()
            browser.refresh()
            time.sleep(4)
            sys.exit()
        time.sleep(delay)


def upload_pic(photopath, caption):
    username = "javvadasghar"
    passwd = "Mjawad1998"
    driverpth = "/Users/Jawad/Desktop/Automation/chromedriver.exe"

    options = Options()
    options.add_argument(
        '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
    browser = webdriver.Chrome(executable_path=driverpth, options=options)
    browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
    time.sleep(3)
    browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/form/div[4]/div/label/input").send_keys(username)
    time.sleep(0.5)
    browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/form/div[5]/div/label/input").send_keys(passwd)
    time.sleep(0.5)
    browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div/div/div/form/div[7]/button/div").click()
    time.sleep(3)
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div/section/div/button").click()
    time.sleep(5)
    browser.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]").click()
    time.sleep(2)
    browser.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    browser.find_element_by_css_selector(
        "#react-root > section > nav.NXc7H.f11OC > div > div > div.KGiwt > div > div > div.q02Nz._0TPg").click()
    time.sleep(2)
    autoit.win_active("Open")
    time.sleep(2)
    autoit.control_send("Open", "Edit1", photopath)
    time.sleep(1.5)
    autoit.control_send("Open", "Edit1", "{ENTER}")
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id='react-root']/section/div[1]/header/div/div[2]/button").click()
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id='react-root']/section/div[2]/section[1]/div[1]/textarea").send_keys(caption)
    time.sleep(2)
    browser.find_element_by_xpath("//*[@id='react-root']/section/div[1]/header/div/div[2]/button").click()
    time.sleep(4)
    browser.close()


def accept_requests(browser, requests):
    signIn(browser)
    time.sleep(2)
    browser.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]").click()
    time.sleep(2)
    browser.find_element_by_xpath(
        "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[3]/div/div[1]").click()
    time.sleep(2)
    i = 1
    for i in range(1, requests):
        str1 = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[4]/div/div/div[2]/div[2]/div/div/div[1]/div/div["
        str2 = "]/div[3]/div/div[1]"
        final_string = str1 + str(i) + str2
        time.sleep(3)
        try:
            browser.find_element_by_xpath(final_string).click()
            time.sleep(3)
        except:
            print("No Pending Friend Request")

            time.sleep(5)
            sys.exit()


def view_stories(browser):
    signIn(browser)
    time.sleep(2)
    try:
        browser.find_element_by_class_name('lri3b').click()
        time.sleep(20)
    except:
        print("No Story Found")


log = open("log.txt", 'a')


def _get_names(browser):
    time.sleep(2)
    scroll_box = browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul")
    scroll_to_bottom(browser)
    time.sleep(2)

    links = scroll_box.find_elements_by_tag_name('a')
    names = [name.text for name in links if name.text != '']

    browser.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button") \
        .click()
    return names


def follow_followers_of(browser, user):
    signIn(browser)
    time.sleep(2)
    browser.get('https://www.instagram.com/' + user + '/')
    time.sleep(5)

    no_f = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]").text
    fol = no_f.replace(" followers", "")
    fol = fol.replace(",", "")
    print("followers: ", int(fol))
    time.sleep(1)

    browser.find_element_by_xpath("//a[contains(@href,'/followers')]") \
        .click()
    time.sleep(2)
    scroll_by_number(browser, 9)
    time.sleep(2)
    count = 0
    clearline = '\033[A                             \033[A'
    for i in range(int(fol)):
        if (count < 100):
            try:
                button = browser.find_element_by_xpath(
                    "/html/body/div[4]/div/div[2]/ul/div/li[" + str(i + 1) + "]/div/div[2]/button")

                if button.text == 'Follow':
                    button.click()
                    count += 1
                    print(clearline)
                    print('followed : ', count)
                    time.sleep(2)
                else:
                    print(clearline)
                    print("Skipped! ")
                    time.sleep(0.25)
            except:
                try:
                    button = browser.find_element_by_xpath(
                        "/html/body/div[4]/div/div[2]/ul/div/li[" + str(i + 2) + "]/div/div[2]/button")

                    if button.text == 'Follow':
                        button.click()
                        count = count + 1
                        print(clearline)
                        print('followed : ', count)
                        time.sleep(2)
                    else:
                        print(clearline)
                        print("Skipped! ")
                        time.sleep(0.25)
                except:
                    try:
                        browser.find_element_by_xpath("//button[contains(text(), 'Cancel')]") \
                            .click()
                        time.sleep(1)
                    except:
                        print("Error: Terminating!")
                        break
        else:
            print("process terminated. follow requests > 100")
            break
    log.write("\tFollowed " + str(count) + " followers\n")
    count += count


def get_my_followers(browser, usernam):
    signIn(browser)
    time.sleep(2)
    list = open("myfollowers.txt", "w+")
    time.sleep(2)
    # username = 'javvadasghar'
    pw = 'Mjawad1998'
    browser.get('https://www.instagram.com/' + usernam + '/')
    time.sleep(4)
    no_f = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]").text

    fol = no_f.replace(" followers", "")
    print("followers: ", fol)
    time.sleep(2)
    browser.find_element_by_xpath("//a[contains(@href,'/followers')]") \
        .click()

    followers = _get_names(browser)

    list.writelines(["%s\n" % follower for follower in followers])
    list.close()


def scroll_to_bottom(browser):
    height = 0
    scroll_box = browser.find_element_by_xpath("//div[@class='isgrP']")
    ht = 1
    last_ht = 0

    while (last_ht < ht):
        time.sleep(1)
        last_ht = ht
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                               scroll_box)
        time.sleep(1)

        ht = browser.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                        return arguments[0].scrollHeight;
                        """, scroll_box)
        height = -ht
    browser.execute_script(str(height), scroll_box)


def scroll_by_number(browser, num):
    height = 0
    scroll_box = browser.find_element_by_xpath("//div[@class='isgrP']")
    ht = 1
    scroll = 0
    while scroll < num:
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                               scroll_box)
        time.sleep(2)
        ht = browser.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                        return arguments[0].scrollHeight;
                        """, scroll_box)
        height = -ht
        scroll += 1
    browser.execute_script(str(height), scroll_box)


def follow_likers(browser):
    signIn(browser)
    usr = input('Enter target username: ')
    browser.get('https://www.instagram.com/' + usr + '/')
    time.sleep(2)

    print('Open the post to scavenge likes. After the post is opened enter "scrap" to continue')
    ip = input('Continue? ')

    count = 0
    try:
        browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button') \
            .click()
    except:
        browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button') \
            .click()

    time.sleep(10)

    pb = browser.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div").value_of_css_property(
        "padding-bottom")
    match = False
    try:
        while not match:
            for i in range(1, 17):

                try:
                    time.sleep(1)
                    button = browser.find_element_by_xpath(
                        '/html/body/div[5]/div/div[2]/div/div/div[' + str(i) + ']/div[3]/button')

                    if button.text == 'Follow':
                        button.click()
                        count += 1
                    else:
                        time.sleep(0.5)
                except:
                    pass

            elements = browser.find_elements_by_xpath("//*[@id]/div/a")
            lastHeight = pb
            browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])

            time.sleep(1)

            pb = browser.find_element_by_xpath("/html/body/div[5]/div/div[2]/div/div").value_of_css_property(
                "padding-bottom")

            if lastHeight == pb or count < 100:
                match = True
    except:
        print("_______Error________")

    log.write("\tFollowed " + str(count) + " followers from " + usr + "'s post\n")
    count += count


def __del__(browser):
    try:
        browser.close()
    except:
        pass
    print("Bot is terminated! :(")


action = input("What do you want to perform? \n"
               "Press 1: Unfollow Actions \n"
               "Press 2: Search for a specific location \n"
               "Press 3: Like particular picture taken at a particular location \n"
               "Press 4: Follow other users followers\n"
               "Press 5: Comment on the picture of specific tag\n"
               "Press 6: Download or Unlike posts of a specific tag \n"
               "Press 7: Download and Unsave Saved Posts \n"
               "Press 8: Upload Picture\n"
               "Press 9: Unfollow user who dont follow you back\n"
               "Press 10:Auto View Stories\n"
               "Press 11:Accept Follow Requests\n"
               "Press 12:Get List your followers / follow followers of @xyz / follow likers of some post\n")
if action == "1":
    unfollowing = input("Who do you want to Unfollow? \n"
                        "Press 1: Unfollow a Specific User \n"
                        "Press 2: Unfollow your account followers \n")
    if unfollowing == "1":
        unfollow_user(chrome_driver(), "ali zafar")
    if unfollowing == "2":
        unfollow_users(chrome_driver(), 3)
    else:
        print("Invalid Search")
if action == "2":
    search_by_location(chrome_driver(), 'karachi', 5)
if action == "3":
    like_particular_picture(chrome_driver(), 'psl', 30)
if action == "4":
    another_user_followers(chrome_driver(), "cute.ahil", 50)
if action == "5":
    comment_particular_picture(chrome_driver(), "#psl", "Great Post!", 10)
if action == "6":
    furthur_action = input("What do you want to perform? \n"
                           "Press 1: To unlike posts \n"
                           "Press 2: Download Hashtag top Posts \n")
    if furthur_action == "1":
        unlike_posts(chrome_driver(), "#igtv", 10)
    if furthur_action == "2":
        print("Please enter in the terminal. 'Instagram-scraper --tag <tag-name without #> i.e. Instagram-scraper "
              "--tag igtv\n'")
        InstagramScraper()
    else:
        print("Invalid Search")
if action == "7":
    furthur_action = input("What do you want to perform? \n"
                           "Press 1: Save posts \n"
                           "Press 2: Unsave Posts \n"
                           "Press 3: Download Save Posts\n")
    if furthur_action == "1":
        save_posts(chrome_driver(), "#igtv", 10)
    if furthur_action == "2":
        unsave_posts(chrome_driver(), 100)
    if furthur_action == "3":
        print("Please Enter 'instaloader :saved --login=your_username' in the terminal")
        Instaloader()
    else:
        print("Invalid Search")
if action == "8":
    upload_pic("C:\\Users\Jawad\Desktop\imran.jpg", "My Brother")
if action == "9":
    print("Please Enter in the Terminal. <python unfollow.py <username> <password>")
if action == "10":
    view_stories(chrome_driver())
if action == "11":
    accept_requests(chrome_driver(), 10)
if action == "12":
    furthur_action = input("What do you want to perform? \n"
                           "Press 1: Get List of your followers\n"
                           "Press 2: Follow followers of @xyz\n"
                           "Press 3: Follow likers of some post\n"
                           "Press 00: Terminate Program\n")
    if furthur_action == "1":
        get_my_followers(chrome_driver(), 'javvadasghar')
    if furthur_action == "2":
        user = input("Username of account to be scrapped: ")
        follow_followers_of(chrome_driver(), user)
    if furthur_action == "3":
        follow_likers(chrome_driver())
    else:
        print("Invalid Search")
else:
    print("Invalid Search")
