questions = [];

function getQuestionValues() {
    const questionTextArea = document.getElementById("question");
    const answerTextArea = document.getElementById("answer");
    const hintTextArea = document.getElementById("hint");
    
    return {
        question: questionTextArea.value,
        answer: answerTextArea.value,
        hint: hintTextArea.value,
    };
}


function addQuestion(questionId, question, vocal, hints) {
    const questionsList = document.getElementById("questions-list");
    const questionDiv = document.createElement("div");
    if (hints.length === 0) {
        hints.push("");
    }
    questions.push({
        question: question,
        answer: "",
        vocal: vocal,
        hint: hints[0],
    });
    questionDiv.className = "mdl-list__item";
    questionDiv.innerHTML = `
        <span class="mdl-list__item-primary-content">
            <i class="material-icons mdl-list__item-avatar">question_answer</i>
            <span>${question}</span>
        </span>
        <span class="mdl-list__item-secondary-action">
            <button class="mdl-button mdl-js-button mdl-button--icon" onclick=openDialog(${questions.length - 1})>
                <i class="material-icons">edit</i>
            </button>
        </span>
        <span class="mdl-list__item-secondary-action">
            <button class="mdl-button mdl-js-button mdl-button--icon" onclick=deleteQuestion(${questions.length - 1})>
                <i class="material-icons">delete</i>
            </button>
        </span>
    `;
    questionsList.appendChild(questionDiv);
}

function createQuestion() {
    const question = getQuestionValues();
    questions.push(question);
    var dialog = document.querySelector('dialog');
    dialog.close();
    resetDialog();
    displayQuestions();
}

function editQuestion(editIndex) {
    const question = getQuestionValues();
    questions[editIndex] = question;
    var dialog = document.querySelector('dialog');
    dialog.close();
    resetDialog();
    displayQuestions();
}

function resetDialog() {
    const questionTextArea = document.getElementById("question");
    const answerTextArea = document.getElementById("answer");
    const hintTextArea = document.getElementById("hint");
    const submitButton = document.getElementById("submit-button");
    questionTextArea.value = "";
    answerTextArea.value = "";
    hintTextArea.value = "";
    submitButton.onclick = createQuestion;
    submitButton.innerHTML = "Ajouter l'exercice";
}

function openDialog(editIndex) {
    var dialog = document.querySelector('dialog');
    if (!dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    dialog.showModal();
    const questionTextArea = document.getElementById("question");
    const answerTextArea = document.getElementById("answer");
    const hintTextArea = document.getElementById("hint");
    const submitButton = document.getElementById("submit-button");
    if (editIndex !== undefined) {
        const question = questions[editIndex];
        questionTextArea.value = question.question;
        answerTextArea.value = question.answer;
        hintTextArea.value = question.hint;
        submitButton.onclick = editQuestion.bind(null, editIndex);
        submitButton.innerHTML = "Editer l'exercice";
    }
}

function displayQuestions() {
    const questionsDiv = document.getElementById("questions-list");
    questionsDiv.innerHTML = "";
    questions.forEach((question, index) => {
        const questionDiv = document.createElement("div");
        questionDiv.innerHTML = `
        <div class="mdl-list__item mdl-shadow--2dp">
            <span class="mdl-list__item-primary-content">
                <span>${index + 1}. ${question.question}</span>
            </span>
            <span style="margin-right: 10px;"></span>
            <a class="mdl-list__item" href="#" onclick="openDialog(${index})">
                <i class="material-icons">edit</i>
            </a>
        </div>
        `;
        questionsDiv.appendChild(questionDiv);
    });
}

function submitTest() {
    const title = document.getElementById("test-title").value;
    if (title === "") {
        alert("Le titre ne peut pas être vide !");
        return;
    }
    if (questions.length === 0) {
        alert("Le test doit contenir au moins une question !");
        return;
    }
    const data = {
        title,
        questions,
    };
    fetch("/api/addtest", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    }).then(response => {
        if (response.status === 200) {
            window.location.href = "/teacherEvaluations";
        }
    });
}