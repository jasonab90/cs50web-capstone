document.addEventListener('DOMContentLoaded', function() {

	document.querySelector("[name=archive]").addEventListener('click', (event) => {
		const id = event.target.value

		fetch("/card/" + id + "/archive", {
			method: 'PUT',
			body: JSON.stringify({
				archived: true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result)

			try {
				message = document.querySelector("[name=message]");
				message.style.display="block"
				message.className = "alert alert-primary mt-3"
				message.innerHTML = ""
				message.innerHTML = "Card archived!"

			} catch {}

			document.querySelector("[name=archive]").style.display = "none";
			document.querySelector("[name=unarchive]").style.display = "block";
		})
		

	})

	document.querySelector("[name=unarchive]").addEventListener('click', (event) => {
		const id = event.target.value

		fetch("/card/" + id + "/archive", {
			method: 'PUT',
			body: JSON.stringify({
				archived: false
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result)

			try {
				message = document.querySelector("[name=message]");
				message.style.display="block"
				message.className = "alert alert-success mt-3"
				message.innerHTML = ""
				message.innerHTML = "Card restored!"

			} catch {}

			document.querySelector("[name=unarchive]").style.display = "none";
			document.querySelector("[name=archive]").style.display = "block";
		})
	})

	document.querySelectorAll("[name=edit-item]").forEach( (item) => {
		
		item.addEventListener('click', (event) => {
			list_item = item.parentElement
			content = list_item.innerText
			form = document.createElement('form')
			form.method = "POST"
			form.action = "/item/" + list_item.value + "/edit"

			hidden = document.createElement('hidden')
			hidden.name = "item"
			hidden.value = list_item.value

			text = document.createElement('input')
			text.type = "text"
			text.name = "edit-text"
			text.className = "form-control"
			text.value = content
			
			submit = document.createElement('submit')
			submit.style.display = "none"

			list_item.innerText = ""

			form.append(hidden)
			form.append(text)
			form.append(submit)
			list_item.append(form)
			text.focus()

		})
	})
	document.querySelectorAll("[name=complete-item]").forEach( (item) => {

		item.addEventListener('click', (event) => {
			id = item.parentElement.value;

			fetch("/item/" + id, {
				method: 'PUT',
				body: JSON.stringify({
					is_active: false
				})
			})
			.then(response => response.json())
			.then(result => {
				console.log(result)
				item.parentElement.style.textDecoration = "line-through";
				item.style.display = "none"
			})
		})
	})
	document.querySelector("[name=item]").addEventListener('keyup', (event) => {
		if (event.target.value.length > 0 ){
			document.querySelector("[name=submit]").disabled = false;

		} else {
			document.querySelector("[name=submit]").disabled = true;
		}
	})

	document.querySelector("[name=favorite]").addEventListener('click', () => {

		id = document.querySelector("[name=favorite]").value
		fetch("/card/" + id + "/favorite", {
			method: 'PUT',
			body: JSON.stringify({
				favorite: true
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result)
			try {
				message = document.querySelector("[name=message]");
				message.style.display="block"
				message.className = "alert alert-success mt-3"
				message.innerHTML = ""
				message.innerHTML = "Card favorited!"

			} catch {}
		})
		document.querySelector("[name=unfavorite]").style.display = "block";
		document.querySelector("[name=favorite]").style.display = "none";
	})

	document.querySelector("[name=unfavorite]").addEventListener('click', () => {

		id = document.querySelector("[name=favorite]").value
		fetch("/card/" + id + "/favorite", {
			method: 'PUT',
			body: JSON.stringify({
				favorite: false
			})
		})
		.then(response => response.json())
		.then(result => {
			console.log(result)

			try {
				message = document.querySelector("[name=message]");
				message.style.display="block"
				message.className = "alert alert-info mt-3"
				message.innerHTML = ""
				message.innerHTML = "Card has been removed from favorites."

			} catch {}
		})
		document.querySelector("[name=unfavorite]").style.display = "none";
		document.querySelector("[name=favorite]").style.display = "block";
	})

	document.querySelectorAll(".list-group-item").forEach( function(item) {

		item.addEventListener('mouseenter', function(event) {
			try {
			edit_item = item.firstChild.nextElementSibling
			complete_item = edit_item.nextElementSibling

			edit_item.style.display = "block";
			edit_item.style.cursor = "pointer";
			complete_item.style.display= "block";
			complete_item.style.cursor = "pointer";
		} catch {}
		})

		item.addEventListener('mouseleave', function(event) {
			try {
			edit_item = item.firstChild.nextElementSibling
			complete_item = edit_item.nextElementSibling

			edit_item.style.display = "none";
			complete_item.style.display= "none";
		} catch {}
		})


		/*item.addEventListener('click', function(item) {

			fetch("/item/" + item.target.value + "/status")
			.then(response => response.json())
			.then(result => {

				if (result.is_active == true) {
					fetch("/item/" + item.target.value, {
						method: "PUT",
						body: JSON.stringify({
							is_active: false
						})
					})
					.then(response => response.json())
					.then(result => {

						item.target.style.textDecoration ="line-through"

					})
				} else if (result.is_active == false) {

					console.log("was false!")
					fetch("/item/" + item.target.value, {
						method: "PUT",
						body: JSON.stringify({
							is_active: true
						})
					})
					.then(response => response.json())
					.then(result => {
						item.target.style.textDecoration = "none"
					})
				}
				})

		}) */
	})

})