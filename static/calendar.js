// date range picker in new_ad
$(document).ready(function() {
var today = new Date();
$('.calRange').daterangepicker({
    minDate: today,
    locale: {
        cancelLabel: 'Clear'
    }
});
$('.calRange').on('apply.daterangepicker', function(ev,picker) {
    $(this).val(picker.startDate.format('DD/MM/YYYY') + " - " + picker.endDate.format('DD/MM/YYYY'));
});

$('.calRange').on('cancel.daterangepicker', function(ev, picker) {
    $(this).val('');
});
});

// Calendar in new_ad
$( function() {
    $( "#avail_date" ).multiDatesPicker({
        minDate: 0,
        dateFormat: 'd-m-yy'
    });
 });

// Button in new_ad to reset dates selected
$(document).ready(function() {
	$( "#reset" ).click(function() {
    	$( "#avail_date" ).multiDatesPicker('resetDates', 'picked');
	});
});
// calendar in book.html to show the available days
function getDates(dates) {
    // Change dates (given in ranges) to all dates
    $( "#avail_dates" ).multiDatesPicker({
        disabled: true,
        dateFormat: 'd-m-yy',
        addDates: dates
    });
}
// union two sets
function union(setA, setB) {
    var union = new Set(setA);
    for (var elem of setB) {
        union.add(elem);
    }
    return union;
}
// Find the difference of two sets
function difference(setA, setB) {
    var difference = new Set(setA);
    for (var elem of setB) {
        difference.delete(elem);
    }
    return difference;
}

// Get every date given a month and year
// Return as a set
function getDaysInMonth(month, year) {
     var date = new Date(Date.UTC(year, month, 1));
     var days = new Set();
     while (date.getMonth() === month) {
  		var day = (date.getDate() < 10 ? '0' : '').toString() + date.getDate().toString()
  	    + "-" +((date.getMonth() + 1) < 10 ? '0' : '').toString() + (date.getMonth() + 1) +"-"+ date.getFullYear().toString();
        days.add(day);
        date.setDate(date.getDate() + 1);
     }
     return days;
}

// Disables dates in the calendar except for dates(input)
function disableDates(dates) {
    // Get the dates for the next three months
    var today = new Date();
    var avail = new Set([dates]);
    var firstDate = today;
    var secDate = new Date();
    secDate.setDate(secDate.getDate() + 31);
    var thirdDate = new Date()
    thirdDate.setDate(thirdDate.getDate() + 62);
    // get the next three months from today
    var months = [firstDate.getMonth(), secDate.getMonth(), thirdDate.getMonth()];
    var years = [firstDate.getFullYear(),secDate.getFullYear(),thirdDate.getFullYear()];

    var allDates = new Set();
    var i;
    // Get all the dates for the next three months into a set
    for(i = 0;i < months.length;i++) {
    	let monthDates = getDaysInMonth(months[i], years[i]);
		allDates = union(allDates, monthDates);
    }
    // All the dates that should be disabled
    var toDisable = difference(allDates, avail);
    // convert to list
	const disable = [...toDisable];
	// Put into calendar
    $("#mdp-demo").multiDatesPicker({
        dateFormat: 'd-m-yy',
        addDisabledDates: disable
    });
}

//		var tableHeaders = new Array();
//		var dateCount = 0;
//		tableHeaders = ['Start Date', 'End Date', ''];

//		function createTable() {
//			var dateTable = document.createElement('table');
//			dateTable.setAttribute('id', 'dateTable');
//			// dateTable.setAttribute('name', 'dateRangeTable');
//			var tr = dateTable.insertRow(-1);
//
//			for (var h = 0; h < tableHeaders.length; h++) {
//				var th = document.createElement('th');
//				th.innerHTML = tableHeaders[h];
//				tr.appendChild(th);
//			}
//
//			var div = document.getElementById('t_cont');
//			div.appendChild(dateTable);
//			dateCount = 0;
//			addRange();
//		}

//		function addRange() {
//			var dateTable = document.getElementById('dateTable');
//
//			var rowCount = dateTable.rows.length;
//			var tr = dateTable.insertRow(-1); // Add row to end of table
//
//			for (var c = 0; c < tableHeaders.length; c++) {
//				var td = document.createElement('td');
//
//				td = tr.insertCell(c);
//
//				if (c == 2) {
//					if (rowCount > 1) {
//						// Add a remove button
//						var removeButton = document.createElement('input');
//
//						removeButton.setAttribute('type', 'button');
//						removeButton.setAttribute('value', 'Remove');
//						removeButton.setAttribute('onclick', 'removeRange(this)');
//
//						td.appendChild(removeButton);
//					}
//				} else {
//					// Add a date input field
//					var dateBox = document.createElement('input');
//
//					dateBox.setAttribute('type', 'date');
//					dateBox.setAttribute('name', 'dateRange_'+dateCount);
//					dateBox.setAttribute('value', '');
//
//					td.appendChild(dateBox);
//					dateCount++;
//					document.getElementById("dateCountOut").setAttribute('value', dateCount);
//
//				}
//			}
//		}
