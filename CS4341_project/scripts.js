// script.js

$(document).ready(function () {
    // Function to handle CSV file
    function handleCSVFile() {
        // Adjust the path to your CSV file based on your project structure
        const csvFilePath = '../data/NBA_Player_Stats.csv';

        // Use jQuery's AJAX to fetch the CSV file
        $.ajax({
            type: "GET",
            url: csvFilePath,
            dataType: "text",
            success: function (data) {
                displayCSVAsTable(data);
            },
            error: function (xhr, status, error) {
                console.error('Error reading the CSV file:', status, error);
            }
        });
    }

    // Function to display CSV as HTML table
    function displayCSVAsTable(csv) {
        const rows = csv.split('\n');
        const table = $('<table id="dataTable"></table>');

        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].split(',');

            if (i === 0) {
                // Create header row
                const headerRow = $('<tr></tr>');
                for (let j = 0; j < cells.length; j++) {
                    headerRow.append('<th>' + cells[j] + '</th>');
                }
                table.append('<thead>' + headerRow.html() + '</thead>');
            } else {
                // Create data rows
                const dataRow = $('<tr></tr>');
                for (let j = 0; j < cells.length; j++) {
                    dataRow.append('<td>' + cells[j] + '</td>');
                }
                table.append(dataRow);
            }
        }

        $('#tableContainer table').replaceWith(table);
    }

    // Call handleCSVFile when the document is ready
    handleCSVFile();

    // Global scope function for search
    window.search = function () {
        const input = $('#searchInput').val().toLowerCase();
        const rows = $('#dataTable tr').slice(1); // Exclude header row

        rows.each(function () {
            const cells = $(this).find('td');
            let found = false;

            cells.each(function () {
                const cellText = $(this).text().toLowerCase();
                if (cellText.includes(input)) {
                    found = true;
                    return false; // Break out of the loop
                }
            });

            if (found) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    };
});
