import {Cell} from "./cell.js";

const backendURL = 'http://127.0.0.1:5000'

function loadBackend(data) {
    let formData = new FormData();

    for (const cell of data) {
        if (cell.isEnabled()) {
            if (cell.hasAudio()) {
                const key = cell.getId() + "+audio";
                formData.append(key, cell.getAudio());
            }
        }
    }

    // Send data to backend
    $.ajax({
        url: backendURL + '/load',
        type: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        success: function (response) {
            console.log('Response from backend:', response);
        },
        error: function (error) {
            console.error('Error sending data:', error);
        }
    });
}

$(document).ready(function () {
    $('#submitButton').click(function () {
        // Data to send to backend
        let data = []
        $('#mainTable tbody tr').each(function () {
            const row = $(this);

            row.find('.player').each(function () {
                const $playerDiv = $(this);
                const id = $playerDiv.attr('id');

                // Create new cell
                let cell = new Cell(id);

                const audioInput = $playerDiv.find('.audioInput')[0];
                if (audioInput && audioInput.files.length > 0) {
                    const file = audioInput.files[0];
                    cell.addAudio(file);
                }


                const checkbox = $playerDiv.find('.playerCheckbox');
                if (checkbox.prop('checked')) {
                    cell.setEnable(true);
                }

                data.push(cell);
            })
        });
        loadBackend(data);
    });
});