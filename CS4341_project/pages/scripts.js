document.addEventListener("DOMContentLoaded", function () {
    let originalData;
    let selectedRowsData = [];
    let blob = null;

    // Function to handle CSV file
    function handleCSVFile() {
        // Adjust the path to your CSV file based on your project structure
        const csvFilePath = '../data/NBA_Player_Stats.csv';

        // Use Fetch API to fetch the CSV file
        fetch(csvFilePath)
            .then(response => response.text())
            .then(data => {
                originalData = data;
                displayCSVAsTable(data, 'dataTable', onRowClick);
            })
            .catch(error => {
                console.error('Error reading the CSV file:', error);
            });
    }

    // Function to display CSV as HTML table
    function displayCSVAsTable(csv, tableId, rowClickCallback) {
        const rows = csv.split('\n');
        const table = document.createElement('table');
        table.id = tableId;

        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].split(',');

            if (i === 0) {
                const headerRow = document.createElement('tr');
                for (let j = 0; j < cells.length; j++) {
                    const th = document.createElement('th');
                    th.textContent = cells[j];
                    headerRow.appendChild(th);
                }
                table.appendChild(document.createElement('thead')).appendChild(headerRow);
            } else {
                const dataRow = document.createElement('tr');
                dataRow.addEventListener('click', () => rowClickCallback(dataRow, cells));
                
                for (let j = 0; j < cells.length; j++) {
                    const td = document.createElement('td');
                    td.textContent = cells[j];
                    dataRow.appendChild(td);
                }
                table.appendChild(dataRow);
            }
        }

        document.getElementById(tableId).replaceWith(table);
    }

    // Function to handle row click
    function onRowClick(rowElement, rowData) {
        const rowIndex = selectedRowsData.findIndex(row => row.join(',') === rowData.join(','));

        if (rowIndex === -1) {
            if (selectedRowsData.length < 5) {
                selectedRowsData.push(rowData);
                rowElement.classList.add('selected');
            } else {
                alert('You can only select up to 5 players.');
            }
        } else {
            selectedRowsData.splice(rowIndex, 1);
            rowElement.classList.remove('selected');
        }
    }

    // Function to save selected rows to Blob
    window.saveSelectedRows = function () {
        if (selectedRowsData.length === 0) {
            alert('No players selected. Please click on players to select them.');
            return;
        }

        const selectedCSVData = selectedRowsData.map(row => row.join(',')).join('\n');

        // Create a Blob containing the selected CSV data
        blob = new Blob([selectedCSVData], { type: 'text/csv' });
        displayBlobAsTable(blob, 'blobTable');

        console.log(selectedRowsData);
    };

    // Function to clear Blob content and the displayed table
    window.clearBlob = function () {
        blob = null;
        // Clear the displayed table
        selectedRowsData = [];
        handleCSVFile();
        $("#blobTable tr").remove();

        console.log(selectedRowsData);
    };

    // Function to display Blob content as a table
    function displayBlobAsTable(blob, tableId) {
        const reader = new FileReader();

        reader.onload = function () {
            const blobContent = reader.result;
            const rows = blobContent.split('\n');
            const table = document.createElement('table');
            table.id = tableId;

            for (let i = 0; i < rows.length; i++) {
                const cells = rows[i].split(',');

                if (i === 0) {
                    const headerRow = document.createElement('tr');
                    for (let j = 0; j < cells.length; j++) {
                        const th = document.createElement('th');
                        th.textContent = cells[j];
                        headerRow.appendChild(th);
                    }
                    table.appendChild(document.createElement('thead')).appendChild(headerRow);
                } else {
                    const dataRow = document.createElement('tr');
                    for (let j = 0; j < cells.length; j++) {
                        const td = document.createElement('td');
                        td.textContent = cells[j];
                        dataRow.appendChild(td);
                    }
                    table.appendChild(dataRow);
                }
            }

            document.getElementById(tableId).replaceWith(table);
        };

        if (blob) {
            reader.readAsText(blob);
        } else {
            // If blob is null, display an empty table
            reader.onload();
        }
    }

    // Function to search for rows based on user input
    window.search = function() {
        const input = $('#searchInput').val().toLowerCase();
        const rows = $('#dataTable tr').slice(1); // Exclude header row

        rows.each(function() {
            const cells = $(this).find('td');
            let found = false;

            cells.each(function() {
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

    // Call handleCSVFile when the document is ready
    handleCSVFile();
});
