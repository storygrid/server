import {Cell} from "./cell.js";

const backendURL = 'http://127.0.0.1:5000'

$(document).ready(function () {
    $('#submitButton').click(function () {
        // Data to send to backend
        let data = {}
        $('#mainTable tbody tr').each(function () {
            const row = $(this);

            row.find('.player').each(function () {
                const $playerDiv = $(this);
                const id = $playerDiv.attr('id');
                data[id] = [];

                // Create new cell
                let cell = new Cell(id);

                const checkbox = $playerDiv.find('.playerCheckbox');
                if (checkbox.prop('checked')) {
                    cell.addAction('Sound');
                }

                data[id].push(cell.getPlainObject());
            })
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