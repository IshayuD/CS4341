document.addEventListener("DOMContentLoaded", function () {
    let originalData;
    let selectedRowsData = [];
    let blob = null;

    // Call displayCSVAsTable when the document is ready
    displayCSVAsTable();

    function displayCSVAsTable() {
        fetch('/get_csv')
            .then(response => response.text())
            .then(csv => {
                // Parse and display the CSV data as a table
                parseAndDisplayCSV(csv, 'dataTable', onRowClick);
            })
            .catch(error => console.error('Error fetching CSV:', error));
    }

    // Function to parse CSV and display as table
    // Function to parse CSV and display as table with row click
    function parseAndDisplayCSV(csv, tableId, onRowClick) {
        const rows = csv.split('\n');
        const table = document.createElement('table');
        table.id = tableId;

        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].split(',');

            // Create header row
            const row = document.createElement(i === 0 ? 'thead' : 'tr');

            for (let j = 0; j < cells.length; j++) {
                const cellType = i === 0 ? 'th' : 'td';
                const cell = document.createElement(cellType);
                cell.textContent = cells[j];
                row.appendChild(cell);
            }

            // Add event listener for row click
            if (i > 0 && typeof onRowClick === 'function') {
                row.addEventListener('click', function () {
                    onRowClick(row, cells);
                });
            }

            table.appendChild(row);
        }

        const existingTable = document.getElementById(tableId);
        if (existingTable) {
            existingTable.replaceWith(table);
        } else {
            document.body.appendChild(table);
        }
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

        //Calculate averages from the blob table
        computeColumnAverage();

        //Sends blob as a JSON to /save_json
        sendTableAsJSON();

        // Call the function to display recommended data in the table
        displayJsonAsTable(jsonData, 'recommendedTable');
    };

    // Function to clear Blob content and the displayed table
    window.clearBlob = function () {
        blob = null;
        // Clear the displayed table
        selectedRowsData = [];
        displayCSVAsTable();
        $("#blobTable tr").remove();
        Array.from(document.getElementsByClassName("curr_avg_stat")).forEach(element =>
            element.innerHTML = "");
    };

    // Function to display Blob content as a table with a fixed header
    function displayBlobAsTable(blob, tableId, headerTableId = 'dataTable') {
        const reader = new FileReader();

        reader.onload = function () {
            const blobContent = reader.result;

            const rows = blobContent.split('\n');
            const table = document.createElement('table');
            table.id = tableId;

            let headerRow = null;
            let headerIndices = [];

            const headerTable = document.getElementById(headerTableId);
            if (headerTable) {
                // Use the header row from the specified header table
                const headerCells = headerTable.getElementsByTagName('th');
                headerRow = document.createElement('tr');
                for (let j = 0; j < headerCells.length; j++) {
                    const th = document.createElement('th');
                    th.textContent = headerCells[j].textContent;
                    headerRow.appendChild(th);
                    headerIndices.push(j);
                }
            }

            for (let i = 0; i < rows.length; i++) {
                const cells = rows[i].split(',');

                // Create data rows
                const dataRow = document.createElement('tr');
                for (let j = 0; j < cells.length; j++) {
                    if (headerIndices.includes(j)) {
                        const td = document.createElement('td');
                        td.setAttribute('class', 'blob_col' + (j + 1));
                        td.textContent = cells[j];
                        dataRow.appendChild(td);
                    }
                }
                table.appendChild(dataRow);
            }

            // Append the header row to the thead section of the table
            table.appendChild(document.createElement('thead')).appendChild(headerRow);

            const existingTable = document.getElementById(tableId);
            if (existingTable) {
                existingTable.replaceWith(table);
            } else {
                document.body.appendChild(table);
            }
        };

        if (blob) {
            reader.readAsText(blob);
        } else {
            // If blob is null, display an empty table
            reader.onload();
        }
    }


    // Function to search for rows based on user input
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

    // Function to compute the average of a particular columns in the starting lineup table
    function computeColumnAverage() {

        const columnIndexes = [5, 1, 6, 7, 8]; // PTS - Rk - AST - STL - BLK
        const table = document.getElementById('blobTable');

        if (!table) {
            console.error('Table not found.');
            return;
        }

        columnIndexes.forEach(columnIndex => {
            var array = [];
            var collection = table.getElementsByClassName('blob_col' + columnIndex);

            for (let i = 0; i < collection.length; i++) {
                array.push(collection[i].textContent);
            }

            var sum = 0;
            var count = 0;
            var average = 0;

            array.forEach(element => {
                var num = Number(element);
                sum += num;
                count++;
            });
            average = (sum / count).toFixed(2);

            if (count === 0) {
                console.log('No valid values found in the column.');
            } else {
                document.getElementById('avg_' + columnIndex).textContent = average.toString();
            }
        });
    }

    // Function to send elements with class "blob_col2" as a JSON file to Flask
    function sendTableAsJSON() {
        const elements = document.getElementsByClassName('blob_col2');

        const jsonData = [];

        for (let i = 0; i < elements.length; i++) {
            const playerValue = elements[i].textContent;

            const rowData = {
                Player: playerValue
            };

            jsonData.push(rowData);
        }
        console.log(jsonData);

        // Send JSON data to Flask
        fetch('/save_json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Response from Flask:', data);
            })
            .catch(error => console.error('Error sending JSON to Flask:', error));
    }

    // function displayJsonAsTable(jsonData, tableId) {
    //     var existingTable = document.getElementById(tableId);

    //     // Clear existing content
    //     existingTable.innerHTML = '';

    //     // Create the header row
    //     var headerRow = existingTable.insertRow(0);
    //     for (var key in jsonData[0]) {
    //         var headerCell = headerRow.insertCell(-1);
    //         headerCell.textContent = key;
    //     }

    //     // Populate the table with data
    //     for (var i = 0; i < jsonData.length; i++) {
    //         var row = existingTable.insertRow(-1);
    //         for (var key in jsonData[i]) {
    //             var cell = row.insertCell(-1);
    //             cell.textContent = jsonData[i][key];
    //         }
    //     }
    // }
});