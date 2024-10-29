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

    // Get the selected text and the index data
    let selectedText = getSelectedText(textArea);
    selectIndexs = getSelectIndexs(textArea); // Update the global variable

    console.log(selectIndexs);

    // Set the search word value to the selected text
    search_word.value = selectedText;
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

// Confirm BTN - sends the selectIndexs data to the server
document.getElementById("conformBTN").addEventListener("click", function () {
    // Check if selectIndexs is set, to avoid sending null data
    if (selectIndexs) {
        fetch('http://localhost:5000/sandData', {
            method: 'POST', // Specify the request method
            headers: {
                'Content-Type': 'application/json', // Specify content type
            },
            body: JSON.stringify(selectIndexs) // Convert selectIndexs to JSON string
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();  // Handle the JSON response
        })
        .then(result => console.log(result)) // Process the result on the client
        .catch(error => console.error('Error:', error));
    } else {
        console.log("No text selected or index data available to send.");
    }
});