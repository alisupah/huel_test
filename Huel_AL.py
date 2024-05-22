"""
This script searches for two product lines, add items to basket, and verify item quantity in basket.

This test script was written in python using a playwright library in VS code studio. I've organized it into three sections; global variables, functions, and the main test script. This format allows users to easily update and maintain the test script. I created a function to store all flavours that are visible on the website in a list, then iterate through the list to add items to the basket based on a specified quantity. This was my approach to minimize hard coding and handle any potential out of stock items. Each time an item is added to the basket, the variable "count" increases. This is to verify the correct amount of items have been added, as well as verifying that at least two items are present in the basket. 

"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    #Variables
    count = 0 #keep count of items
    continue_button = page.get_by_role('button', name="Continue") # Continue button
    summary_bar = page.locator('.InteractiveSummaryBarContent') #summary bar
    powder_flavours = [] #powder flavour list
    bar_flavours = [] #bar flavour list
    

    # functions
    #Search product
    def search(product):
        page.get_by_test_id("IconLink-Search").click() # Click on search icon
        page.get_by_test_id("SearchBar__input").fill(product) # Input product
        page.get_by_test_id("SearchBar__submit-button").click() # Enter

    # Create list of flavours
    def all_flavours(flavours):
        flavours = flavours
        flavour_card = page.get_by_test_id('ProductCardVariantFlavourPicker') #Parent class of flavour
        flavour_list = flavour_card.locator(page.locator('p.FlavourPicker__flavour-title')) #title class of flavour
        flavour_count = flavour_list.count() # Count amount of flavours
        # Iterate through each element to add flavor to list
        for i in range(flavour_count):
            flavor = flavour_list.nth(i)
            text = flavor.inner_html()
            flavours.append(text)
        return flavours

    #Add item to basket
    def add_flavour(item_qty, flavours2):
        flavours2 = flavours2
        global count
        #iterate through list items
        for i in range(item_qty):
            x = flavours2[i]
            increase_button = page.get_by_role('button',name= x + " Increase Quantity", exact=True)
            #Add one item to basket
            if increase_button.is_visible():
                increase_button.click()
                count += 1
                #Stop adding items to basket after item_qty reached
                if count >= item_qty:
                    return count
            #Item out of stock if button is hidden
            elif increase_button.is_hidden():
                print("Item is out of stock or unable to add to basket")

    # Start of script
    # Navigate to URL
    page.goto('https://huel.com')

    # Set location
    page.locator("#geolocation-app").get_by_text("Continue").click()

    # Close cookie
    page.get_by_role('button', name= "Accept").click()

    #Search for product
    search("Complete Protein Powder")

    #Click button to shop for powder
    page.get_by_text("Shop Powder").click()

    #Wait for page to load
    page.wait_for_load_state()

    # Create list of flavours
    all_flavours(powder_flavours)

    # Add an item
    # Range has to be two in order to add to basket
    add_flavour(2, powder_flavours)
    
    # Click continue
    summary_bar.locator(continue_button).click()

    #Default frequency is Subscription
    # Click continue
    continue_button.click()

    # Click Continue to Basket
    continue_button.click()

    #Search for product
    search("Complete Nutrition Bar")

    #Click button to shop for bar
    page.get_by_text("Shop Complete Nutrition Bar").click()

    #wait for page to load
    page.wait_for_load_state()

    #Create list of flavours
    all_flavours(bar_flavours)

    #Add items to basket
    add_flavour(1, bar_flavours)

    # Click Continue
    summary_bar.locator(continue_button).click()

    #Default frequency is Subscription
    # Click continue
    continue_button.click()

    # Click Continue to Basket
    continue_button.click()

    #Verify items
    #locate number of items in cart
    items = int(page.locator(".item_count").inner_text())
    #verify if items match count
    if items == count and items >= 2:
        print("Test script is successful")
    else:
        print("Test script failed - item count quantity is incorrect")

    browser.close()