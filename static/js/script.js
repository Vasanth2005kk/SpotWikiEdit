// Declare selectIndexs as a global variable
var selectIndexs = null;

// Clear the input values for search and replace fields when the clear button is clicked
document.getElementById('clearButton').addEventListener('click', function () {
    document.getElementById('Search_word').value = '';
    document.getElementById('Replace_word').value = '';
});

// Handle double-click events within the sandbox content
document.getElementById('sandboxContent').addEventListener('dblclick', function () {
    let textArea = document.getElementById('sandboxContent');
    let search_word = document.getElementById("Search_word");
    // Get the selected text 
    let selectedText = getSelectedText(textArea);
    search_word.value = selectedText;
    selectIndexs = getSelectIndexs(textArea)
});

// Get the selected text from the textarea
function getSelectedText(textArea) {
    let start = textArea.selectionStart;
    let end = textArea.selectionEnd;
    return textArea.value.substring(start, end).trim();
}

// Get the selected word and its start index from the textarea
function getSelectIndexs(textArea) {
    let words = textArea.value.split(" ");
    let start = textArea.selectionStart;

    let total = 0;

    for (let i = 0; i < words.length; i++) {
        total += words[i].length + 1; // Add 1 for the space between words

        if (start < total) {
            // Return an object containing the selected word and its starting index
            return { word: words[i], index: i };
        }
    }
}

// wiki username get 

var WikiUserNameGET = document.querySelector(".username")
let WikiUserName = WikiUserNameGET.innerHTML.substring(5).trim()

console.log("wiki user name :", WikiUserName)

document.getElementById("conformBTN").addEventListener("click", function () {

    let EditoOldWord = document.getElementById("Search_word").value;
    let EditNewText = document.getElementById('Replace_word').value;
    if (EditoOldWord && EditNewText) {
        let textArea = document.getElementById('sandboxContent').value.split(" ");

        alert(`old word ${EditoOldWord} : new word ${EditNewText} ,:indexes  ${selectIndexs.index} username :${WikiUserName} :sandbocContent: ${textArea}`)

        textArea[selectIndexs.index] = EditNewText


        let EditSandBoxContent = textArea.join(" ")

        alert(EditSandBoxContent)

        var data = {
            EditSandBoxContent: EditSandBoxContent
        }

        if (WikiUserName !== 'None') {
            fetch(`${window.origin}/receive_data`, {
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify(data),
                cache: 'no-cache',
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            }).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
                .then(data => console.log("Response from server:", data))
                .catch(error => console.error("Fetch error:", error));
        }
    }
})
