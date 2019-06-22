let quizesUl = document.getElementById('quizList').getElementsByTagName("LI");

for (i = 0; i < quizesUl.length; i++) {
    quizesUl[i].addEventListener('click', startQuiz);
}

function startQuiz(e) {
    let input = e.target.getElementsByTagName('input');
    var url= input[0].getAttribute("data-url");
    window.location = url;
}