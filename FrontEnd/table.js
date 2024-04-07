const rows = 4;
const alphas = ['A', 'B', 'C', 'D'];
const columns = alphas.length;

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


function getCheckboxesDiv(id) {
    const $div = $('<div class="pieces-checkboxes"></div>').attr('id', 'checkboxes_' + id);

    $.each(pieceData, function (index, piece) {

        // Create the checkbox elements
        const boxId = 'checkbox_' + id + '_' + piece.value;
        const $checkbox = $('<input>', {
            type: 'checkbox',
            id: boxId,
            value: piece.value,
            class: piece.value === 'all' ? 'all' : 'single',
            checked: piece.value === 'all',
            disabled: piece.value !== 'all',
        });

        const $label = $('<label>', {
            for: boxId,
            text: piece.label
        });

        // Handle selection
        $checkbox.change(function () {
            // all is selected
            if ($(this).hasClass('all')) {
                if (this.checked) {
                    $('.single', $div).prop('checked', false).prop('disabled', true);
                } else {
                    $('.single', $div).prop('disabled', false);
                }
            }
            // Individual piece selected
            else {
                $('.all', $div).prop('checked', false).prop('disabled', false);
            }
        });

        $div.append($checkbox).append($label).append('<br>');
    });

    return $div;
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
    const $body = $('#mainTable tbody');

    for (let col = 1; col < 5; col++) {
        const $row = $('<tr></tr>');
        const $rowHeader = $('<th scope="row"></th>').text(col);

        // Header
        $row.append($rowHeader);

        // Cell Div
        for (let j = 0; j < 4; j++) {
            const $cell = $('<td></td>');
            const $cellDiv = $('<div class="cellDiv"></div>')
            $cell.append($cellDiv);
            $row.append($cell);
        }
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

document.addEventListener('DOMContentLoaded', fillRows);