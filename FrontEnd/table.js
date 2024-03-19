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
            piece.appendChild(getCheckboxesDiv(id).get(0));
            action.appendChild(getActionDiv(id));
        }
    }
}

document.addEventListener('DOMContentLoaded', fillRows);