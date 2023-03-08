import time
import math
import base64
from io import BytesIO
from PIL import Image


def fullpage_screenshot(driver, file):
    # 1.scroll page to head, hide scroll bar
    driver.execute_script("window.scrollTo(0, 0)")
    driver.execute_script("window.document.styleSheets[0].insertRule('::-webkit-scrollbar {display: none;}',"
                          " window.document.styleSheets[0].cssRules.length);")
    # 2.get toal height and view widht/height, scale
    vp_total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    vp_height = driver.execute_script("return window.innerHeight")
    vp_width = driver.execute_script("return window.innerWidth")
    scale = driver.execute_script("return window.devicePixelRatio")
    # 3.caculate scroll parameter to list
    rectangles_vp = []
    vp = 0
    while vp < vp_total_height:
        vp_top_height = vp + vp_height
        if vp_top_height > vp_total_height:
            vp = vp_total_height - vp_height
            vp_top_height = vp_total_height
        rectangles_vp.append((0, vp, 0, vp_top_height))
        vp = vp + vp_height
    # 4. every scroll, paste current view port sreenshot to stitched_image
    stitched_image = Image.new('RGB', (int(vp_width * scale), int(vp_total_height * scale)))
    for i, rect_vp in enumerate(rectangles_vp):
        driver.execute_script("window.scrollTo({0}, {1})".format(0, rect_vp[1]))
        time.sleep(0.2)
        b64_img = driver.get_screenshot_as_base64()
        screenshot = Image.open(BytesIO(base64.b64decode(b64_img)))
        if (i + 1) * vp_height > vp_total_height:
            offset = (0, int((vp_total_height - vp_height) * scale))
        else:
            offset = (0, int(i * vp_height * scale - math.floor(i / 2.0)))
        stitched_image.paste(screenshot, offset)
    stitched_image.save(file)
    # 5.scroll page to head, show scroll bar
    driver.execute_script("window.scrollTo(0, 0)")
    driver.execute_script("window.document.styleSheets[0].deleteRule(window.document.styleSheets[0].cssRules.length-1)")
