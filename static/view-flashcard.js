const headers = {
    'Content-Type': 'application/json'
}

function deleteFlashcard(flashcard_id){
    let body = {flashcard_id:flashcard_id}
    fetch(`/delete-flashcard`, {
        method:'POST',
        body:JSON.stringify(body),
        headers:headers
    })
    .then(response => response.text())
    .then(data => console.log(data))
    window.location.replace('/my-flashcards')
}


