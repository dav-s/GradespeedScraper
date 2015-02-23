from bs4 import BeautifulSoup
import mechanize
from base64 import decodestring


class Link:
    """
    A container for holding a link and its test.

    It is intended to simulate the HTML anchor tag.
    """

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def get_url(self):
        return self.url

    def __repr__(self):
        return self.text


class Wrapper:
    """
    The main interface for interacting and transversing Gradespeed.
    """

    @staticmethod
    def extract_string_from_script(script):
        """
        Static method to extract the encoded string from the Javascript inside the script tag.

        :param script: JavaScript string that contains the fragmented encoded string.
        :return: The continuous encoded string.
        """
        split_script = script.split("'")
        result = ""
        for x in range(1, len(split_script), 2):
            result += split_script[x]
        return result

    def __init__(self, url):
        """
        Constructs the attributes for the wrapper.

        :param url: The url for the parent login page.
        """
        self.br = mechanize.Browser()
        self.start_url = url
        self.grades_url = None
        self.logged_in = False
        self.students = []

        self.br.set_handle_robots(False)
        self.br.open(url)

    def login(self, username, password):
        """
        Attempts to log into Gradespeed.

        This is required to pass to use the other methods.

        This method will fail if the login credentials do not work.

        :param username: The username string of the Gradespeed account.
        :param password: The password string of the Gradespeed account.
        """
        if self.logged_in:
            raise Exception("You are already logged in!")
        if self.br.geturl() != self.start_url:
            self.br.open(self.start_url)
        self.br.open(self.start_url)
        self.br.select_form("Form1")
        self.br["txtUserName"] = username
        self.br["txtPassword"] = password
        self.br.submit()

        if self.br.geturl() == self.start_url:
            raise Exception("Incorrect credentials.")

        soup = BeautifulSoup(self.br.response().read())
        sthtml = soup.find(id="_ctl0_ddlStudents")
        if sthtml is not None:
            for option in sthtml.children:
                self.students.append((option["value"], option.string))
        else:
            sthtml = soup.find(id="_ctl0_lblStudent")
            self.students = [sthtml.string]
        self.br.follow_link(text_regex="Grades")
        self.grades_url = self.br.geturl()
        self.logged_in = True

    def get_available_students(self):
        """
        Returns the student ids associated with the given account.

        This method will fail if the user has not successfully called the `login()` method.

        :return: A list of the student id strings associated with the given account.
        """
        if not self.logged_in:
            raise Exception("You need to be logged in to get the students!")
        return self.students

    def get_student_grades_overview(self, student_id=None):
        """
        Retrieves the overview grades for a specified student.

        This method will fail if the user has not successfully called the `login()` method.

        The result is in the format of a `student_name` (self explanatory) and `grades`.
        `grades` contains `headers`, which are the headings for each column of the table,
                and  `rows`, which is a list of the rows containing strings and `Links`.

        :param student_id: The id of the student for the overview (Optional for one student accounts).
        :return: A dictionary containing the student grades overview information.
        """
        if not self.logged_in:
            raise Exception("You need to be logged in to get the students!")

        if student_id is not None:
            if student_id not in self.students:
                raise Exception("A student with that id was not found!")
            if len(self.students) > 1:
                self.br.select_form("aspnetForm")
                self.br["_ctl0:ddlStudents"] = [student_id]
                self.br.submit()

        soup = BeautifulSoup(self.br.response().read())
        script = soup.find(id="_ctl0_tdMainContent").find_all("script", language="Javascript")[0].string
        decoded_soup = BeautifulSoup(decodestring(self.extract_string_from_script(script)).replace("&nbsp;", ""))

        headers = [child.string for child in decoded_soup.find("tr", {"class": ["TableHeader"]}).children]
        rows = []
        for row in decoded_soup.find_all("tr", {"class": ["DataRow", "DataRowAlt"]}):
            row_data = []
            for child in row.find_all(["th", "td"]):
                a_check = child.a
                if a_check is not None:
                    if a_check["class"][0] == "Grade":
                        row_data.append(Link(a_check.string, a_check["href"]))
                    else:
                        row_data.append(a_check.string)
                else:
                    row_data.append(child.string)
            rows.append(row_data)

        return {"student_name": decoded_soup.find("span", {"class": ["StudentName"]}).string,
                "grades": {"headers": headers, "rows": rows}}

    def get_class_grades(self, link):
        """
        Retrieves the specific grades for a class section.

        This method will fail if the user has not successfully called the `login()` method.

        The dictionary returned is in the format `class_name`, `current_average`, and `sections`.
        `sections` is in the format `name`, `average`, and `grades`.
        `grades` is in somewhat the same format as `grades` in the dictionary return of `get_student_grades_overview`,
                however it will not include links.

        :param link: A `Link` object linking to a specific class grade.
        :return: A dictionary containing information about that grade class section.
        """
        if not self.logged_in:
            raise Exception("You need to be logged in to get the students!")

        soup = BeautifulSoup(self.br.open(self.grades_url+link.get_url()).read())
        script = soup.find(id="_ctl0_tdMainContent").find_all("script", language="Javascript")[1].string
        decoded_soup = BeautifulSoup(decodestring(self.extract_string_from_script(script)).replace("&nbsp;", ""))

        sections = []
        zipped_sections = zip(decoded_soup.find_all("span", {"class": ["CategoryName"]}),
                              decoded_soup.find_all("table", {"class": ["DataTable"]}))
        for sect in zipped_sections:
            headers = [child.string for child in decoded_soup.find("tr", {"class": ["TableHeader"]}).children]
            rows = []
            average = sect[1].find_all("tr")[-1].find_all("td")[3].string
            for row in sect[1].find_all("tr", {"class": ["DataRow", "DataRowAlt"]}):
                row_data = []
                for child in row.find_all(["th", "td"]):
                    row_data.append(child.string)
                rows.append(row_data)
            sections.append({"name": sect[0].string,
                             "average": average if average != "--" else None,
                             "grades": {"headers": headers, "rows": rows}})

        return {"class_name": decoded_soup.find("h3", {"class": ["ClassName"]}).string,
                "current_average": decoded_soup.find("p", {"class": ["CurrentAverage"]}).string.split(":")[1].strip(),
                "sections": sections}
