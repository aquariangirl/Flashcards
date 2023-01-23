const headers = {
    'Content-Type': 'application/json'
}

function deleteFlashcard(flashcard_id){
    var form = document.getElementById("del");
    function handleForm(event) { 
        event.preventDefault();
        let body = {flashcard_id:flashcard_id}
        fetch(`/delete-flashcard`, {
            method:'POST',
            body:JSON.stringify(body),
            headers:headers
        })
        
        window.location.replace('/my-flashcards');
        console.log("[KS]");
    } 
    form.addEventListener('submit', handleForm);
    }
    
    // .then(response => console.log("[KS] response: " + response.text()))
    // .then(data => console.log("[KS] data: " + data))
    // 



