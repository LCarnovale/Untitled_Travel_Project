var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "" && y[i].class == "required") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // Error check on the date ranges
  var dateCount = document.getElementById("dateCountOut").value;
  // Check if it has been filled
  if (dateCount == 1) {
    if (dateRange_0.value == "") {
        // empty, invalid
    }
  } else {
    // Check if the dates are not overlapping
  var start_date = new Array(dateCount);
var end_date = new Array(dateCount);
    // Get all the dates into a start date array and end date array
    for (var i = 0; i < dateCount; i++) {
        var date = eval('dateRange_' + i);
        start_date[i] = date.match("([0-9]{2}/[0-9]{2}/[0-9]{4}) - [0-9]{2}/[0-9]{2}/[0-9]{4}")[1];
        end_date[i] = date.match("[0-9]{2}/[0-9]{2}/[0-9]{4} - ([0-9]{2}/[0-9]{2}/[0-9]{4})")[1];
        document.getElementById("demo"+i).innerHTML = start_date[i];
    }
    // compare all start dates with end dates
    for (var j = 0; j < dateCount; j++) {
        var first_date = moment(start_date[j], "DD/MM/YYYY");
        var sec_date = moment(end_date[j], "DD/MM/YYYY");
        for (var k = dateCount-1; k > 0; k--) {
        	if (k ==j) break;
            var third_date = moment(start_date[j], "DD/MM/YYYY");
            var fourth_date = moment(end_date[j], "DD/MM/YYYY");
            if (third_date <= first_date <= fourth_date || third_date <= sec_date <= fourth_date) {
                alert("FALSE");
            }
        }
    }
  }

  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}
