/*
document.addEventListener('DOMContentLoaded', function() {

    const editpost_button = document.createElement('button');
    editpost_button.onclick = edit(event);
    editpost_button.id = "editpost-button";
    editpost_button.innerHTML = 'Edit Post';

    const editpost_textarea = document.createElement('textarea');
    editpost_textarea.id = "editpost-textarea";
    editpost_textarea.style.display = 'none';


    const editpost_save = document.createElement('button');
    editpost_save.style.display = 'none';
    editpost_save.onclick = save(event);
    editpost_save.id = "editpost-save";
    editpost_save.innerHTML = 'Save';


    document.querySelector('.all-posts').append(editpost_button)
    document.querySelector('.all-posts').append(editpost_textarea)
    document.querySelector('.all-posts').append(editpost_save)

})
*/

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.editpost-button').forEach(button => {
        button.onclick = edit;
    });
})

function edit(event) {
    
    const postid = event.target.dataset.postid;

    document.querySelector(`#editpost-button-${postid}`).style.display = 'none';
    document.querySelector(`#editpost-textarea-${postid}`).style.display = 'block';
    document.querySelector(`#editpost-submit-${postid}`).style.display = 'block';
    document.querySelector(`#post-${postid}`).style.display = 'none';

    return false;
}

function save(event) {

    const postid = event.target.dataset.postid;
    const content = document.querySelector(`#editpost-textarea-${postid}`).value

    fetch('/edit_post', {
        method: 'POST',
        body: JSON.stringify({
            postid: postid,
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });

    document.querySelector(`#editpost-button-${postid}`).style.display = 'block';
    document.querySelector(`#editpost-textarea-${postid}`).style.display = 'none';
    document.querySelector(`#editpost-submit-${postid}`).style.display = 'none';
    document.querySelector(`#post-${postid}`).style.display = 'block';
    document.querySelector(`#post-${postid}`).innerHTML = `<b>${content}<b>`;

    return false
}

function like(event) {

    const postid = event.target.dataset.postid;
    const userid = event.target.dataset.userid;

    fetch('/like_post', {
        method: 'POST',
        body: JSON.stringify({
            postid: postid,
            userid: userid
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });

    let likes = Number(document.querySelector(`#likes-${postid}`).innerHTML);
    likes++;
    document.querySelector(`#likes-${postid}`).innerHTML = String(likes);

    document.querySelector(`#unlike-post-${postid}`).style.display = 'block';
    document.querySelector(`#like-post-${postid}`).style.display = 'none';

    return false;
}


function unlike(event) {
    
    const postid = event.target.dataset.postid;
    const userid = event.target.dataset.userid;

    fetch('/unlike_post', {
        method: 'POST',
        body: JSON.stringify({
            postid: postid,
            userid: userid
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });

    let likes = Number(document.querySelector(`#likes-${postid}`).innerHTML);
    likes--;
    document.querySelector(`#likes-${postid}`).innerHTML = String(likes);

    document.querySelector(`#like-post-${postid}`).style.display = 'block';
    document.querySelector(`#unlike-post-${postid}`).style.display = 'none';

    return false;
}