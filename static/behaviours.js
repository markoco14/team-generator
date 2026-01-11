function updateStudentCount() {
    let studentInputs = document.querySelectorAll("#student-list > li");
    const numberOfStudents = document.getElementById("student-count");
    numberOfStudents.textContent = studentInputs.length;

    if (studentInputs.length < 1) {
        const submitButton = document.querySelector("button[type='submit']")
        submitButton.setAttribute("disabled", "")
    } else {
        const submitButton = document.querySelector("button[type='submit']")
        submitButton.removeAttribute("disabled")
    }
}

function removeStudentInput(button) {
    const li = button.closest("li");
    li.remove();
    updateStudentCount();

    let studentInputs = document.querySelectorAll("#student-list > li");
    const numberOfStudents = document.getElementById("student-count");
    numberOfStudents.textContent = studentInputs.length;

    if (studentInputs.length < 1) {
        let error = document.querySelector(".error")
        error.textContent = ""
    }
}