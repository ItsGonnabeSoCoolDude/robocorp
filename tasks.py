from robocorp.tasks import task
from robocorp import browser


@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""
    browser.configure(
        slowmo=800,
    )
    open_the_intranet_website()
    log_in()
    fill_and_submit_sales_form()


def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/")


def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")


def fill_and_submit_sales_form():
    """Fills in the sales data and click the 'Submit' button"""
    page = browser.page()
    page.fill("#firstname", "John")
    page.fill("#lastname", "Smith")
    page.select_option("#salestarget", "10000")
    page.fill("#salesresult", "123")
    page.click("text=Submit")
