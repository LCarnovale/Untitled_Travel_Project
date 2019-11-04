$(document).on('focus',".calRange", function(){
    $(this).daterangepicker({
        minDate: new Date(),
        locale: {
            cancelLabel: 'Clear',
            format: 'DD/MM/YYYY'
        }
    });
    $('.calRange').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });
});


var tableHeaders = new Array();
var dateCount = 0;
tableHeaders = ['Start and End Date', ''];

function createTable() {
	var dateTable = document.createElement('table');
	dateTable.setAttribute('id', 'dateTable');
	// dateTable.setAttribute('name', 'dateRangeTable');
	var tr = dateTable.insertRow(-1);
	for (var h = 0; h < tableHeaders.length; h++) {
		var th = document.createElement('th');
		th.innerHTML = tableHeaders[h];
		tr.appendChild(th);
	}

	var div = document.getElementById('t_cont');
	div.appendChild(dateTable);
	dateCount = 0;
	addRange();
}

function addRange() {
	var dateTable = document.getElementById('dateTable');
	var rowCount = dateTable.rows.length;
	var tr = dateTable.insertRow(-1); // Add row to end of table

	for (var c = 0; c < tableHeaders.length; c++) {
		var td = document.createElement('td');
		td = tr.insertCell(c);
		if (c == 1) {
			if (rowCount > 1) {
				// Add a remove button
				var removeButton = document.createElement('input');
				removeButton.setAttribute('type', 'button');
				removeButton.setAttribute('value', 'Remove');
				removeButton.setAttribute('onclick', 'removeRange(this)');
				td.appendChild(removeButton);
			}
		} else {
			// Add a date input field
			var dateBox = document.createElement('input');

			dateBox.setAttribute('type', 'text');
			dateBox.setAttribute('name', 'dateRange_'+dateCount);
			dateBox.setAttribute('class', 'calRange');
			dateBox.setAttribute('id', 'dateRange_'+dateCount);
			td.appendChild(dateBox);
			dateCount++;
			document.getElementById("dateCountOut").setAttribute('value', dateCount);
		}
	}
}

function removeRange(buttonObj) {
	var dateTable = document.getElementById('dateTable');
	// button <- td <- tr , tr has row index.
	dateTable.deleteRow(buttonObj.parentNode.parentNode.rowIndex);
	dateCount -= 1;
	document.getElementById("dateCountOut").setAttribute('value', dateCount);
}


