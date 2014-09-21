from bs4 import BeautifulSoup
import mechanize
from stringcode import decode_string


def extract_string_from_script(script):
    split_script = script.split("'")
    result = ""
    for x in range(1, len(split_script), 2):
        result += split_script[x]
    return result


class Link:

    def __init__(self, text, url):
        self.text = text
        self.url = url

    def get_url(self):
        return self.url

    def __repr__(self):
        return self.text


class Wrapper:

    def __init__(self, url):
        self.br = mechanize.Browser()
        self.start_url = url
        self.grades_url = None
        self.logged_in = False
        self.students = []

        self.br.set_handle_robots(False)
        self.br.open(url)

    def login(self, username, password):
        if self.logged_in:
            raise Exception
        if self.br.geturl() != self.start_url:
            self.br.open(self.start_url)
        self.br.open(self.start_url)
        self.br.select_form("Form1")
        self.br["txtUserName"] = username
        self.br["txtPassword"] = password
        self.br.submit()

        if self.br.geturl() == self.start_url:
            raise Exception

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
        if not self.logged_in:
            raise Exception
        return self.students

    def get_student_grades_overview(self, student_id=None):
        if student_id is not None:
            if len(self.students) <= 1:
                raise Exception
            is_in_list = False
            for student in self.students:
                if student[0] == student_id:
                    is_in_list = True
            if not is_in_list:
                raise Exception

            self.br.select_form("aspnetForm")
            self.br["_ctl0:ddlStudents"] = [student_id]
            self.br.submit()

        soup = BeautifulSoup(self.br.response().read())
        script = soup.find(id="_ctl0_tdMainContent").find_all("script", language="Javascript")[0].string
        decoded_soup = BeautifulSoup(decode_string(extract_string_from_script(script)).replace("&nbsp;", ""))

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
                "grades": {"headers": headers,
                           "rows": rows}}

    def get_class_grades(self, link):
        soup = BeautifulSoup(self.br.open(self.grades_url+link.get_url()).read())
        script = soup.find(id="_ctl0_tdMainContent").find_all("script", language="Javascript")[1].string
        decoded_soup = BeautifulSoup(decode_string(extract_string_from_script(script)).replace("&nbsp;", ""))

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
                             "grades": {"headers": headers,
                                        "rows": rows}})

        return {"class_name": decoded_soup.find("h3", {"class": ["ClassName"]}).string,
                "current_average": decoded_soup.find("p", {"class": ["CurrentAverage"]}).string.split(":")[1].strip(),
                "sections": sections}
