const rows = 4;
const alphas = ['A', 'B', 'C', 'D'];
const columns = alphas.length;

const tableRows = rows * columns;

const pieceNames = ["Piece 1", "Piece 2", "Piece 3", "Piece 4"];

function getPieceDiv(id) {
    const div = document.createElement('div');
    const selectElement = document.createElement('select');
    let pieceId = 1;
    for (const pieceName of pieceNames) {
        const optionElement = document.createElement('option');
        optionElement.value = pieceId.toString();
        optionElement.textContent = pieceName;
        selectElement.appendChild(optionElement);
        pieceId += 1;
    }

    div.appendChild(selectElement);
    div.id = id;
    return div;
}

function getActionDiv(id) {
    const div = document.createElement('div');
    const inputElement = document.createElement('input');
    inputElement.type = "file";

    div.appendChild(inputElement);
    div.id = id;

    return div;
}

function fillRows() {
    const table = document.getElementById("mainTable")
    const body = table.getElementsByTagName('tbody')[0]

    for (let r = 1; r < rows + 1; r++) {
        for (const alpha of alphas) {
            const row = body.insertRow();

            const pos = row.insertCell(0);
            const piece = row.insertCell(1);
            const action = row.insertCell(2);

            const id = alpha + r.toString();
            pos.textContent = id;
            piece.appendChild(getPieceDiv(id));
            action.appendChild(getActionDiv(id));
        }
    }
}

document.addEventListener('DOMContentLoaded', fillRows);