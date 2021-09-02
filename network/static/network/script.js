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

    // Code here...

}