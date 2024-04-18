const rows = 4;
const alphas = ['A', 'B', 'C', 'D'];
const columns = alphas.length;
const players = ['P1', 'P2', 'P3', 'P4'];


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
