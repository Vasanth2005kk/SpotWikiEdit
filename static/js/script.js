// Clear the input values for search and replace fields when the clear button is clicked
document.getElementById('clearButton').addEventListener('click', function () {
    document.getElementById('Search_word').value = '';
    document.getElementById('Replace_word').value = '';
});

// Handle double-click events within the sandbox content
document.getElementById('sandboxContent').addEventListener('dblclick', function (event) {
    let textArea = document.getElementById('sandboxContent');
    let selectedText = getSelectedText(textArea);
    let selectIndexs = getSelectIndexs(textArea);

    // Creating the data object to send
    const data = {
        text: selectedText,
        indexs: selectIndexs
    };

    console.log(selectedText, selectIndexs);

    // Checking if both selectedText and selectIndexs are valid
    if (selectedText.OldText && selectIndexs.StartIndex !== undefined && selectIndexs.EndIndex !== undefined) {
        fetch('http://localhost:5000/sandboxContent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(responseData => {
            console.log(responseData);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

// Get the selected text from the textarea
function getSelectedText(textArea) {
    let start = textArea.selectionStart;
    let end = textArea.selectionEnd;
    return { OldText: textArea.value.substring(start, end).trim() };
}

// Get the selected indices from the textarea
function getSelectIndexs(textArea) {
    let start = textArea.selectionStart;
    let end = textArea.selectionEnd;
    return {
        StartIndex: start,
        EndIndex: end
    };
}
