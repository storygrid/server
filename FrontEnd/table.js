const rows = 4;
const alphas = ['A', 'B', 'C', 'D'];
const columns = alphas.length;
const players = ['P1', 'P2', 'P3', 'P4'];
const tableRows = rows * columns;

const pieceData =
    [
        {value: 'all', label: 'All Pieces'},
        {value: '1', label: 'Pieces 1'},
        {value: '2', label: 'Pieces 2'},
        {value: '3', label: 'Pieces 3'},
        {value: '4', label: 'Pieces 4'}
    ];

const backendURL = 'http://127.0.0.1:5000'

class Cell {
    constructor(piece) {
        this.piece = piece;
        this.actions = []
    }

    addAction(action) {
        this.actions.push(action)
    }

    getPlainObject() {
        return {
            piece: this.piece,
            actions: this.actions
        };
    }
}


function getAudioDiv(id) {
    const $div = $('<div class="audioDiv"></div>')
    const $button = $('<button>', {
        type: "button",
        class: "audioUploadButton",
        text: "Upload MP3",
    })
    const $inputElement = $('<input>', {
        type: 'file',
        class: 'audioInput',
        accept: 'audio/mp3'
    });
    $div.append($button);
    $div.append($inputElement);
    $div.id = "sound" + id;

    return $div;
}

function appendCheckBox(id, $parentDiv) {
    // Create the checkbox elements
    const boxId = 'checkbox_' + id;
    const $checkbox = $('<input>', {
        type: 'checkbox',
        id: boxId,
        value: id,
        checked: true,
        class: "playerCheckbox",
    });

    const $label = $('<label>', {
        for: boxId,
        text: "Enable",
    });

    $parentDiv.append($checkbox).append($label);
}

function fillCellDiv(id, $parentDiv) {
    let i = 0;
    for (let row = 0; row < 2; row++) {
        const $rowDiv = $('<div class="row"></div>');
        for (let col = 0; col < 2; col++) {
            const playerId = id + "_" + players[i];
            const $playerDiv = $('<div class="player"></div>').addClass(players[i]);
            $playerDiv.id = playerId; // IDs are in the format A1_P1

            // Text
            const $textDiv = $('<div class="playerText"></div>').text(players[i]);
            $playerDiv.append($textDiv);

            // Handle checkbox
            const $checkboxDiv = $('<div class="playerCheckboxDiv"></div>');
            appendCheckBox(playerId, $checkboxDiv);
            $playerDiv.append($checkboxDiv);

            // Get actions
            $playerDiv.append(getAudioDiv(playerId));
            // Append to row
            $rowDiv.append($playerDiv);
            i += 1;
        }
        $parentDiv.append($rowDiv);
    }
}

function fillRows() {
    const $body = $('#mainTable tbody');

    for (let col = 1; col < 5; col++) {
        const $row = $('<tr></tr>');
        const $rowHeader = $('<th scope="row"></th>').text(col);

        // Header
        $row.append($rowHeader);

        // Cell Div
        $.each(alphas, function (_, alpha) {
            const $cell = $('<td></td>');
            const $cellDiv = $('<div class="cellDiv"></div>')
            const id = alpha + col;
            fillCellDiv(id, $cellDiv);
            $cell.append($cellDiv);
            $row.append($cell);
        });
        $body.append($row);
    }
}

$(document).ready(function () {
    $('#submitButton').click(function () {
        // Data to send to backend
        let data = {}
        $('#mainTable tbody tr').each(function () {
            const row = $(this);
            const position = row.find('td:eq(0)').text();

            data[position] = [];

            // Parse checkboxes
            const checkboxes = row.find('td:eq(1) input[type=checkbox]:checked');
            checkboxes.each(function () {
                const checkbox = $(this);

                // Create new cell
                let cell = new Cell(checkbox.val());

                // If checked then check the action
                if (checkbox.prop('checked')) {
                    cell.addAction("Audio");
                }
                data[position].push(cell.getPlainObject());
            });
        });

        // Send data to backend
        $.ajax({
            url: backendURL + '/load',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function (response) {
                console.log('Response from backend:', response);
            },
            error: function (error) {
                console.error('Error sending data:', error);
            }
        });
    });
});

$(document).ready(function () {
    $('#mainTable').on('click', '.audioUploadButton', function () {
        $(this).next('.audioInput').click();
    });

    $('#mainTable').on('change', '.audioInput', function () {
        const fileName = this.files[0] ? this.files[0].name : '';
        const truncatedName = fileName.length > 15 ? fileName.substring(0, 12) + '...mp3' : fileName;
        $(this).prev('.audioUploadButton').text(fileName ? `File: ${truncatedName}` : 'Upload MP3');
    });
});

document.addEventListener('DOMContentLoaded', fillRows);
