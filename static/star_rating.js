function star_click(num) {
    var i;
    for (i = 1; i <= num; i++) {
        star = document.getElementById('star'+i.toString());
        star.src = '/static/star_filled.png';
    }
    for (i = num+1; i <= 5; i++) {
        star = document.getElementById('star'+i.toString());
        star.src = '/static/star_empty.png';
    }

    document.getElementById('rating_input').value = num.toString();
    document.getElementById('review_submit').disabled = false;
}

function star_hover(num) {
    var i;
    for (i = 1; i <= num; i++) {
        star = document.getElementById('star'+i.toString());
        star.src = '/static/star_filled.png';
    }
    for (i = num+1; i <= 5; i++) {
        star = document.getElementById('star'+i.toString());
        star.src = '/static/star_empty.png';
    }
}

function star_unhover() {
    num = parseInt(document.getElementById('rating_input').value)
    var i;
    for (i = 1; i <= num; i++) {
        star = document.getElementById('star'+i.toString());
        star.src = '/static/star_filled.png';
    }
    for (i = num+1; i <= 5; i++) {
        star = document.getElementById('star'+i.toString());
        star.src = '/static/star_empty.png';
    }
}