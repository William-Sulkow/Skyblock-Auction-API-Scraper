import grequests
import json
import time
import pyperclip
import os
import winsound
frequency = 2500
duration = 1000
def item_process(i):
    i = i.replace("⚚ ","")
    i=i.replace("✦","")
    if i.count("✪") != 5:
        i=i.replace("✪","")
    reforges = ["Very Wise","Gentle","Odd","Fast","Fair","Epic","Sharp","Heroic","Spicy","Legendary","Dirty","Fabled","Suspicious","Gilded","Warped","Withered","Bulky","Salty","Treacherous","Stiff","Lucky","Deadly","Fine","Grand","Hasty","Neat","Rapid","Unreal","Awkward","Rich","Precise","Spiritual","Headstrong","Clean","Fierce","Heavy","Light","Mythic","Pure","Smart","Titanic","Wise","Perfect","Necrotic","Ancient","Spiked","Renowned","Cubic","Warped","Reinforced","Loving","Ridiculous","Empowered","Giant","Submerged","Jaded","Bizarre","Itchy","Ominous","Pleasant","Pretty","Shiny","Simple","Strange","Vivid","Godly","Demonic","Forceful","Hurtful","Keen","Strong","Superior","Unpleasant","Zealous","Moil","Toil","Blessed","Bountiful","Magnetic","Fruitful","Refined","Stellar","Mithraic","Auspicious","Fleet","Heated","Ambered","Shaded","Bloody"]
    first_word = i.split()[0]
    if first_word in reforges:
        return i.split(' ', 1)[1].strip()
    return i.strip()
used = []
go = True
while go:
    API_KEY = "103ae47c-385d-4385-9899-09fc22c48548"
    data = {}
    items = {}
    url_base = f"https://api.hypixel.net/skyblock/auctions?key={API_KEY}"
    resp = grequests.get(url_base)
    time_req = int(time.time())
    for res in grequests.map([resp]):
        data = json.loads(res.content)
        total_pages = data['totalPages']
        for auction_item in data["auctions"]:
            if "bin" in auction_item and auction_item["category"] != "blocks" and "Bejeweled" not in auction_item["item_name"] and "Enchanted Book" != auction_item["item_name"] and "Crab Hat" not in auction_item["item_name"] and "Cake Soul" not in auction_item["item_lore"] and "Furniture" not in auction_item["item_lore"] and "Skin" not in auction_item["item_name"]:
                if "[" not in auction_item["item_name"] or "[Lvl 100]" in auction_item["item_name"] and auction_item["claimed"] == False:
                    auction_item["item_name"] = item_process(auction_item["item_name"])
                    if (auction_item["item_name"],auction_item["tier"]) in items:
                        items[(auction_item["item_name"],auction_item["tier"])][3] += 1
                        if items[(auction_item["item_name"],auction_item["tier"])][0] > auction_item["starting_bid"]:
                            items[(auction_item["item_name"],auction_item["tier"])][2] = f"viewauction {auction_item['uuid']}"
                            items[(auction_item["item_name"],auction_item["tier"])][1] = items[(auction_item["item_name"],auction_item["tier"])][0]
                            items[(auction_item["item_name"],auction_item["tier"])][0] = auction_item["starting_bid"]
                            items[(auction_item["item_name"],auction_item["tier"])][4] = auction_item["start"]
                        elif items[(auction_item["item_name"],auction_item["tier"])][1] > auction_item["starting_bid"]:
                            items[(auction_item["item_name"],auction_item["tier"])][1] = auction_item["starting_bid"]
                    else:
                        items[(auction_item["item_name"],auction_item["tier"])] = [auction_item["starting_bid"],0,f"viewauction {auction_item['uuid']}",1,auction_item["start"]]


    urls = []
    for page_count in range(1, total_pages):
        urls.append(f"{url_base}&page={page_count}")
    resp = (grequests.get(url) for url in urls)
    for res in grequests.map(resp):
        data = json.loads(res.content)
        for auction_item in data["auctions"]:
            if "bin" in auction_item and auction_item["category"] != "blocks" and "Bejeweled" not in auction_item["item_name"] and "Enchanted Book" != auction_item["item_name"] and "Crab Hat" not in auction_item["item_name"] and "Cake Soul" not in auction_item["item_lore"] and "Furniture" not in auction_item["item_lore"] and "Skin" not in auction_item["item_name"]:
                if "[" not in auction_item["item_name"] or "[Lvl 100]" in auction_item["item_name"] and auction_item["claimed"] == False:
                    auction_item["item_name"] = item_process(auction_item["item_name"])
                    if (auction_item["item_name"],auction_item["tier"]) in items:
                        items[(auction_item["item_name"],auction_item["tier"])][3] += 1
                        if items[(auction_item["item_name"],auction_item["tier"])][0] > auction_item["starting_bid"]:
                            items[(auction_item["item_name"],auction_item["tier"])][2] = f"viewauction {auction_item['uuid']}"
                            items[(auction_item["item_name"],auction_item["tier"])][1] = items[(auction_item["item_name"],auction_item["tier"])][0]
                            items[(auction_item["item_name"],auction_item["tier"])][0] = auction_item["starting_bid"]
                            items[(auction_item["item_name"],auction_item["tier"])][4] = auction_item["start"]
                        elif items[(auction_item["item_name"],auction_item["tier"])][1] > auction_item["starting_bid"]:
                            items[(auction_item["item_name"],auction_item["tier"])][1] = auction_item["starting_bid"]
                    else:
                        items[(auction_item["item_name"],auction_item["tier"])] = [auction_item["starting_bid"],0,f"viewauction {auction_item['uuid']}",1,auction_item["start"]]
    for i in items.copy():
        if items[i][3] > 5 and items[i][1]-(items[i][0]+((items[i][1]-1)*0.01)) > 100000 and items[i][0] < 300000000 and i not in used and time_req-(items[i][4]/1000)<=120:
            items[i].append(items[i][1]-(items[i][0]+((items[i][1]-1)*0.01)))
        else:
            del items[i]
    if len(items) == 0:
        os.system("cls")
        print(None)
    else:
        items = sorted(items.items(), key=lambda e: e[1][5])
        used.append(items[-1][0])
        os.system("cls")
        print(f"Item: {items[-1][0]}")
        print(f"Profit: {round(items[-1][1][5])}")
        print(f"\nNew Lowest BIN: {items[-1][1][1]-1}")
        pyperclip.copy(items[-1][1][2])
        winsound.Beep(frequency, duration)
