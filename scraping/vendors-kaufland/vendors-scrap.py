import time

from seleniumbase import SB

with open("linksvs.txt", "r") as file:
    links = file.readlines()

with open("vendors.txt", "r") as file:
    vendors = file.readlines()
    VENDORS = [v.strip() for v in vendors]

with SB(uc=True) as sb:
    for link in links[500:]:
        print(f"processing {link}")
        sb.get(link.strip())
        sb.uc_gui_click_captcha()
        try:
            sb.uc_click("#onetrust-reject-all-handler", timeout=5)
        except:
            pass
        sb.scroll_to_bottom()
        try:
            navigation = sb.locator("nav button:nth-last-child(2)", timeout=4).text
        except:
            continue
        for nav in range(1, int(navigation)+1):

            sb.get(link.strip()+f'?page={nav}')
            sb.uc_gui_click_captcha()
            time.sleep(2)
            for i in range(1, 35):
                try:
                    ven = sb.locator(f'(//span[@class="product__seller-info-badge"])[{i}]', timeout=3).text
                    if ven not in VENDORS:
                        print(ven)
                        VENDORS.append(ven)
                        with open("vendors.txt", "a") as f:
                            f.write(ven+"\n")
                except:
                    print(f"failed to process {i}-th product of {link.strip()+f'?page={nav}'}")
                    break