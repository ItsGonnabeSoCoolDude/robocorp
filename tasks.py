from robocorp.tasks import (
    task,
)  # The task decorator is what the sema4 extension hooks to run a bot
from robocorp import browser  # How to interact with browser windows

from RPA.HTTP import HTTP           # how to download files from remote web servers
from RPA.Excel.Files import Files   # Reads Excel files
from RPA.PDF import PDF             # Creates PDFs


@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""
    # By setting a higher value for slowmo we can slow down the robot execution even further.
    # This number represent the number of miliseconds the robot waits for between 2 actions.
    browser.configure(
        slowmo=100,
    )
    open_the_intranet_website()
    log_in()
    download_excel_file()
    fill_form_with_excel_data()
    collect_results()
    export_as_pdf()
    log_out()


def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/")


def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    # To find forms, fields, and other elements from an HTML web page, your robot needs to know their selectors.
    # Think of a selector as the street address for an element, such as the username field on the RobotSpareBin intranet login page.
    # These selectors along with their name and other instructions are stored in locators, in a file called locators.json,
    # from which they can be referenced in the code or used directly as in-line selectors.
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")


def fill_and_submit_sales_form(sales_rep):
    """Fills in the sales data and click the 'Submit' button"""
    # The sales target is not a simple text field but a select HTML element.
    # page.select_option() takes a selector and a value as arguments
    page = browser.page()
    page.fill("#firstname", sales_rep["First Name"])
    page.fill("#lastname", sales_rep["Last Name"])
    page.select_option("#salestarget", str(sales_rep["Sales Target"]))
    page.fill("#salesresult", str(sales_rep["Sales"]))
    page.click("text=Submit")


def download_excel_file():
    """
    Downloads excel file from the given URL
    """
    # The download() function requires a URL as an argument. We know that we can expect our Excel file at https://robotsparebinindustries.com/SalesData.xlsx each week.
    # In addition to the URL argument, we are also setting the overwrite argument to True.
    # This way, we can count on the local file being always the most recent version (if the file exists, the robot has our permission to overwrite it).
    http = HTTP()
    http.download(
        url="https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True
    )


def fill_form_with_excel_data():
    """Read data from excel and fill in the sales form"""
    # Now that we have the RPA.Excel.Files library, our robot can open the Excel file, using the open_workbook() function,
    # just don't forget to close your notebook after reading it!
    # We just need to pass it the file name:
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    worksheet = excel.read_worksheet_as_table("data", header=True)
    excel.close_workbook()

    # We can loop over the rows of the table, and call it each time passing the individual row to it:
    for row in worksheet:
        fill_and_submit_sales_form(row)


def collect_results():
    """Take a screenshot of the page"""
    # The robocorp.browser module provides the page.screenshot() function to help us with this step.
    # We give it a path to save the image file, and it'll take a screenshot of the current view.
    page = browser.page()
    page.screenshot(path="output/sales_summary.png")

def export_as_pdf():
    """Export the data to a pdf file"""
    # we want to put the HTML markup of that element into a variable, sales_results_html.
    # We can do this with the inner_html() function
    # You can find a whole example repo of working with PDFs here: https://github.com/robocorp/example-parse-pdf-invoice/blob/master/tasks.py
    page = browser.page()
    sales_results_html = page.locator("#sales-results").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")


def log_out():
    """Presses the 'Log out' button"""
    page = browser.page()  
    page.click("text=Log out")
