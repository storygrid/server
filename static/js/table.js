const rows = 4;
const alphas = ['A', 'B', 'C', 'D'];
const columns = alphas.length;
const players = ['P1', 'P2', 'P3', 'P4'];
const backendURL = 'http://127.0.0.1:5500'
let data = {}

function truncate(name) {
    return name.length > 15 ? name.substring(0, 12) + '...mp3' : name;
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

    const $deleteButton = $('<button>', {
        type: "button",
        class: "audioDeleteButton",
        text: "X",
    });

    $div.append($button, $inputElement, $deleteButton);
    $div.id = "sound" + id;

    return $div;
}

function fillCellDiv(id, $parentDiv) {
    let i = 0;
    for (let row = 0; row < 2; row++) {
        const $rowDiv = $('<div class="row"></div>');
        for (let col = 0; col < 2; col++) {
            const playerId = id + "_" + players[i];
            const $playerDiv = $('<div class="player"></div>').addClass(players[i]);
            $playerDiv.attr('id', playerId); // IDs are in the format A1_P1

            // Text
            const $textDiv = $('<div class="playerText"></div>').text(players[i]);
            $playerDiv.append($textDiv);

            // Get actions
            $playerDiv.append(getAudioDiv(playerId));

            // Check existing
            if (id in data && players[i] in data[id]) {
                $playerDiv.toggleClass('hasAudio');
                $playerDiv.find('.audioDiv').find('.audioUploadButton').text(truncate(data[id][players[i]]));
            }
            // Append to row
            $rowDiv.append($playerDiv);
            i += 1;
        }
        $parentDiv.append($rowDiv);
    }
}

function setup(callback) {
    $.ajax({
        url: backendURL + '/setup',
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            data = response;
            if (typeof callback === 'function') {
                callback();
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error('Error fetching data:', textStatus, errorThrown);
        }
    });
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
    $('#mainTable').on('click', '.audioUploadButton', function () {
        $(this).next('.audioInput').click();
    });

    $('#mainTable').on('change', '.audioInput', function () {
        const fileName = this.files[0] ? this.files[0].name : '';
        $(this).prev('.audioUploadButton').text(fileName ? `File: ${truncate(fileName)}` : 'Upload MP3');

        // Change the player opacity
        $(this).closest('.player').toggleClass('hasAudio', this.files.length > 0);
    });


    $('#mainTable').on('click', '.audioDeleteButton', function () {
        const $audioDiv = $(this).closest('.audioDiv');
        const $input = $audioDiv.find('.audioInput');
        const $uploadButton = $audioDiv.find('.audioUploadButton');

        $input.val('');
        $uploadButton.text('Upload MP3');
        $audioDiv.closest('.player').removeClass('hasAudio');

        const file_id = $audioDiv.closest('.player').attr('id');
        console.log(file_id)

        // Backend call
        $.ajax({
            url: backendURL + '/delete/' + file_id,
            type: 'DELETE',
            success: function (response) {
                console.log('File deleted successfully:', response);
            },
            error: function (xhr, status, error) {
                console.error('Failed to delete file:', status, error);
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', setup(fillRows));
