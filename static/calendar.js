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




// Button in new_ad to reset dates selected
    $( "#calendar" ).multiDatesPicker({
        minDate: 0,
        dateFormat: 'dd-mm-yyyy'
    });

	$( "#reset" ).click(function() {
    	$( "#calendar" ).multiDatesPicker('resetDates', 'picked');
	});

/**
 * Create a calendar to show the available days
 * 
 * @param {Array.<String>} dates Start and end dates, ie:
 *      `[start_1, end_1, start_2, end_2, ... ]`
 * @param {Boolean} disable If the calendar should be disabled
 */
function getDates(dates, disable) {
    $( "#calendar" ).multiDatesPicker({
        disabled: disable,
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
    $("#calendar").multiDatesPicker({
        dateFormat: 'd-m-yy',
        addDisabledDates: disable
    });
}

