document.addEventListener('DOMContentLoaded', function() {

	document.querySelector("#search-cards").addEventListener('keyup', function(event) {

		let keyword = event.target.value.toLowerCase()

		document.querySelectorAll(".dropdown-menu a").forEach( function(event) {
			task = event.innerHTML.toLowerCase()

			if (task.indexOf(keyword) === -1 ) {
				event.style.display = "none";
			} else {
				event.style.display = "block";
			}
		})
	})

})