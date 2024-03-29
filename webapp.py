from flask import Flask, render_template, request, redirect
import hackbright_app

app = Flask(__name__)


@app.route("/")
def get_github():
    return render_template("get_github.html")
# point to HTML file --> styles.css in 'static'


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    
    student_github = request.args.get("github")
    
    row = hackbright_app.get_student_by_github(student_github)
    
    html = render_template("student_info.html", first_name = row[0], last_name = row[1], github = row[2])
    return html


@app.route("/allgrades")
def get_all_grade():
    hackbright_app.connect_to_db()
    
    student_github = request.args.get("github")
    
    rows = hackbright_app.show_all_grades(student_github)
    
    html = render_template("student_grades.html", student_github = student_github, grades = rows)
    return html


@app.route("/projects")
def get_student_grade():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project") 
    rows = hackbright_app.student_grade_project(project_title)
    html = render_template("project_info.html", project_title = project_title, grades = rows)
    return html


@app.route("/newstudent", methods=['POST'])
def new_student():
    hackbright_app.connect_to_db()
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)
    html = render_template("new_student.html", first_name = first_name, last_name = last_name, github = github)
    return html


@app.route("/newproject", methods=['POST'])
def new_project():
    hackbright_app.connect_to_db()
    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")
    hackbright_app.add_project(title, description, max_grade)

    # html = render_template("new_project.html", title = title, description = description, max_grade = max_grade)
    # return html
    return redirect("/projects?project=%s" % title)


@app.route("/givegrade")
def give_grade():
    hackbright_app.connect_to_db()

    student_github = request.args.get("github")
    project_title = request.args.get("title")
    grade = request.args.get("grade")
    
    hackbright_app.give_grade_to_student(student_github, project_title, grade)
    
    html = render_template("give_grade.html", student_github = student_github, project_title = project_title, grade = grade)
    return html


if __name__ == "__main__":
    app.run(debug=True)