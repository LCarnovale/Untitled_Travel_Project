//Function to designate whether the user would recommend the accommodations or not
//Parameter = "recc" (it's a constant)
function thumb_up(label) {
    up = document.getElementById(label+'_thumb_up');
    up.src = '/static/thumbs_up_selected.png';

    down = document.getElementById(label+'_thumb_down');
    down.src = '/static/thumbs_down_deselected.png';

    document.getElementById(label).value = 'yes';
}

function thumb_down(label) {
    up = document.getElementById(label+'_thumb_up');
    up.src = '/static/thumbs_up_deselected.png';

    down = document.getElementById(label+'_thumb_down');
    down.src = '/static/thumbs_down_selected.png';

    document.getElementById(label).value = 'no';
}