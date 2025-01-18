from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

# 웹드라이버 옵션 설정 (헤드리스 모드 활성화)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
options.add_argument("--disable-gpu")  # GPU 사용 안 함 (헤드리스 모드에서 필요)
options.add_argument("--no-sandbox")  # 샌드박스 비활성화 (리눅스 환경에서 필요)

# 웹드라이버 초기화
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def random_wait():
    time.sleep(random.uniform(3, 6))

def post_to_tistory(username, password, tistory_url, title, content, tags):
    """
    :param username: Tistory 로그인 아이디
    :param password: Tistory 로그인 비밀번호
    :param tistory_url: Tistory URL
    :param title: 글 제목
    :param content: 글 내용
    :param tags: 태그 목록 (쉼표로 구분된 문자열)
    """

    try:
        move_login_page(tistory_url)

        select_kakao_login()

        login(password, username)

        move_write_page()

        check_alert()

        input_title(title)

        select_category()

        input_contents(content)

        input_tags(tags)

        click_pre_publish()

        select_public()

        publish()

        print("포스팅 완료!")

    except TimeoutException as e:
        print("페이지 로드 시간 초과:", e)

    finally:
        # 드라이버 종료
        time.sleep(5)
        driver.quit()


def publish():
    print("publish")
    publish_button = driver.find_element(By.ID, "publish-btn")
    publish_button.click()
    random_wait()


def select_public():
    print("select_public")
    publish_button = driver.find_element(By.ID, "open20")
    publish_button.click()
    random_wait()


def click_pre_publish():
    print("click_pre_publish")
    publish_button = driver.find_element(By.ID, "publish-layer-btn")
    publish_button.click()
    random_wait()


def input_tags(tags):
    print(f"input_tags: {tags}")
    for tag in tags.split(","):
        tag_input = driver.find_element(By.NAME, "tagText")
        tag_input.send_keys(tag.strip())
        tag_input.send_keys(Keys.RETURN)
        random_wait()


def input_contents(content):
    print("input_contents")
    iframe = driver.find_element(By.ID, "editor-tistory_ifr")  # iframe 선택
    driver.switch_to.frame(iframe)  # iframe으로 전환
    content_input = driver.find_element(By.ID, "tinymce")  # 에디터 내부의 입력 요소 선택
    content_input.click()
    random_wait()
    content_input.send_keys(content)  # 내용 입력
    random_wait()
    driver.switch_to.default_content()  # iframe에서 기본 컨텍스트로 전환


def select_category():
    print("select_category")
    category_dropdown = driver.find_element(By.ID, "category-btn")
    category_dropdown.click()
    category_algorithm = "category-item-672117"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, category_algorithm)))
    category_option = driver.find_element(By.ID, category_algorithm)
    category_option.click()
    random_wait()


def input_title(title):
    print("input_title")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "post-title-inp")))
    title_input = driver.find_element(By.ID, "post-title-inp")
    title_input.send_keys(title)
    random_wait()


def check_alert():
    # Alert 처리 (기존 글 작성 여부 확인)
    try:
        print("check_alert")
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.dismiss()  # "No"를 클릭하여 기존 글 무시
        random_wait()
    except TimeoutException:
        print("No Alert, Continue~")


def move_write_page():
    print("move_write_page")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn_tistory")))
    driver.find_element(By.CLASS_NAME, "btn_tistory").click()
    random_wait()


def login(password, username):
    print("login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "loginId")))
    driver.find_element(By.NAME, "loginId").send_keys(username)
    random_wait()
    driver.find_element(By.NAME, "password").send_keys(password)
    random_wait()
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    random_wait()


def select_kakao_login():
    print("select_kakao_login")
    driver.find_element(By.CLASS_NAME, "link_kakao_id").click()
    random_wait()


def move_login_page(tistory_url):
    print("move_login_page")
    login_url = f"https://{tistory_url}/manage"
    driver.get(login_url)
    random_wait()


# 사용 예시
if __name__ == "__main__":
    post_to_tistory(
        username="" # tistory ID,
        password="" # tistory PW,
        tistory_url="",
        title="Tistory 포스팅하기",
        content="글 작성 테스트",
        tags="algorithm, Leetcode, 알고리즘, 릿코드"
    )
