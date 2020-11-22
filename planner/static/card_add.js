document.addEventListener('DOMContentLoaded', function() {

	document.querySelector("[name=title]").addEventListener('keyup', (item) => {
		if (item.target.value.length > 0) {
			document.querySelector("[name=submit]").disabled = false;
		} else {
			document.querySelector("[name=submit]").disabled = true;
		}
	})
	document.querySelector("#add-date").addEventListener('click', function(item) {
		console.log(item)

		if (item.target.checked === true) {
			document.querySelector("[name=month]").disabled = false
			document.querySelector("[name=day]").disabled = false
			document.querySelector("[name=year]").disabled = false
		} else {
			document.querySelector("[name=month]").disabled = true
			document.querySelector("[name=day]").disabled = true
			document.querySelector("[name=year]").disabled = true
		}
	})

	document.querySelector("[name=month]").addEventListener('change', function(item) {
		
		days = days_in_month(item.target.value);
		document.querySelector("[name=day]").innerHTML = "";

		for (let i = 1; i <= days; i++) {
			element = document.createElement('option')
			element.value = i;
			element.innerHTML = i;
			document.querySelector("[name=day]").append(element)
		}
	})

	function days_in_month(month) {

		thirty_one = ["1", "3", "5", "7", "8", "10", "12"]
		thirty = ["4", "6", "9", "11"]
		february = "2"
		if (thirty_one.indexOf(month) >= 0) {
			days = 31

		} else if (february.indexOf(month) >= 0) {
			days = 28
		} else {
			days = 30
		}

		return days;
	}


})