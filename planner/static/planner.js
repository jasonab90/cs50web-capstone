document.addEventListener('DOMContentLoaded', function() {

	
	document.querySelectorAll("input[name='checkbox']").forEach( item => {
		console.log(item.nextSibling.innerHTML)
	})

	document.querySelectorAll("#card-body").forEach( item => {
		console.log(item)
	})


})