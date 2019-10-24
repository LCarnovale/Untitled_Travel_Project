// Calendar in new_ad
  $( function() {
    $( "#avail_date" ).multiDatesPicker({
    	dateFormat: 'dd-mm-yy'
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
    console.log(dates)
    $( "#avail_dates" ).multiDatesPicker({
        disabled: true,
        dateFormat: 'dd-mm-yy',
        addDates: dates
    });
}
