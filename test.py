from helper.driver_helper import create_driver
from page import FacebookPage

USERNAME = "18021087@vnu.edu.vn"
PASSWORD = "Nguyenthanhson18021087@"
driver = create_driver()
facebook = FacebookPage(driver)

facebook.login(USERNAME, PASSWORD)

# facebook.post('Hom nay Helihe cac ban')
# facebook.like()
kwargs = {"name": "Nguyen Son", "city": "Ha Noi", "university": "Dai hoc cong nghe"}
facebook.searching_friend(**kwargs)