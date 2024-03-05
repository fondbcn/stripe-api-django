document.addEventListener("DOMContentLoaded", function () {
	const tokenCheck = document.querySelector('[name=csrfmiddlewaretoken]')
	let csrftoken = ''
	
	if(tokenCheck){
		csrftoken = tokenCheck.value
	}
	
    const submitButt = document.getElementById("submit")
    
	if (submitButt) {
        submitButt.disabled = true;
	}
	
	let signUpToggle = document.getElementById("sign-up")
	let signInToggle = document.getElementById("sign-in")
	let signUpForm = document.querySelector(".sign-up")
	let signInForm = document.querySelector(".sign-in")
	if(signUpToggle){
		signUpToggle.addEventListener("click", (e)=>{
			e.preventDefault()
			signUpForm.classList.toggle("active")
			if(signInForm.classList.contains("active")){
				signInForm.classList.toggle("active")
			}
		})
	}
	if(signInToggle){
		signInToggle.addEventListener("click", (e)=>{
			e.preventDefault()
			signInForm.classList.toggle("active")
			if(signUpForm.classList.contains("active")){
				signUpForm.classList.toggle("active")
			}
		})
	}
	stripeElements()
	
	function stripeElements() {
	  stripe = Stripe('pk_test_51OOFpIJODblskrVixPPy0G5xSBHpc5LDX6ovbnBBFnvbjnvyWcYwxW1u1nKNdU9fx6XvQO4emQkCRHvsSBGc7BQC001hHsichc')

	  if (document.getElementById('card-element')) {
		let elements = stripe.elements()

		let style = {
		  base: {
			color: "#32325d",
			fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
			fontSmoothing: "antialiased",
			fontSize: "16px",
			"::placeholder": {
			  color: "#aab7c4"
			}
		  },
		  invalid: {
			color: "#fa755a",
			iconColor: "#fa755a"
		  }
		};

		card = elements.create('card', { style: style })

		card.mount('#card-element')

		card.on('focus', function () {
		  let el = document.getElementById('card-errors')
		  el.classList.add('focused')
		})

		card.on('blur', function () {
		  let el = document.getElementById('card-errors');
		  el.classList.remove('focused');
		})

		card.on('change', function (event) {
		  submitButt.disabled = event.empty
		  displayError(event)
		})
	  }
	}

	function displayError(event) {
	  let displayError = document.getElementById('card-errors')
	  if (event.error) {
		displayError.textContent = event.error.message;
	  } else {
		displayError.textContent = ''
	  }
	}
	
	function planSelect(name, price, priceId) {
		var inputs = document.getElementsByTagName('input');

		for(var i = 0; i<inputs.length; i++){
		  inputs[i].checked = false
		  if(inputs[i].name== name){
			inputs[i].checked = true
		  }
		}

		var n = document.getElementById('plan');
		var p = document.getElementById('price');
		var pid = document.getElementById('priceId');
		n.innerHTML = name
		p.innerHTML = price
		pid.innerHTML = priceId
			submitButt.disabled = false
	  }
	
	let subForm = document.getElementById('subscription-form')
	if (subForm) {
		subForm.addEventListener('submit', function (event) {
		  event.preventDefault()
		  changeLoadingState(true)
		  // create new payment method & create subscription
		  fetch("{% url 'create-sub' product.id %}", {
			method: "POST",
			headers: {
			  "Content-Type": "application/json",
			  'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
			  email: document.getElementById('email').value
			})
		  })
			.then(function(result) {
			  return result.json();
			})
			.then(function(data) {
			  payWithCard(stripe, card, data.clientSecret);
			})
		});
	  }

	let payForm = document.getElementById("payment-form");
	if(payForm){
		form.addEventListener("submit", function(event) {
		  event.preventDefault();
		  changeLoadingState(true);
		  // Complete payment when the submit button is clicked
		  fetch("{% url 'purchase-int' product.id %}", {
			method: "POST",
			headers: {
			  "Content-Type": "application/json",
			  'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
			  email: document.getElementById('email').value
			})
		  })
			.then(function(result) {
			  return result.json()
			})
			.then(function(data) {
			  payWithCard(stripe, card, data.clientSecret)
			})
		})
	}
	
	function payWithCard(stripe, card, clientSecret) {
      loading(true);
      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card
          }
        })
        .then(function(result) {
          if (result.error) {
            showError(result.error.message)
          } else {
            orderComplete(result.paymentIntent.id)
          }
        })
    }

	let loading = function(isLoading) {
	  if (isLoading) {
		submitButt.disabled = true
		document.querySelector("#spinner").classList.remove("hidden")
		document.querySelector("#button-text").classList.add("hidden")
	  } else {
		submitButt.disabled = false
		document.querySelector("#spinner").classList.add("hidden")
		document.querySelector("#button-text").classList.remove("hidden")
	  }
	}
	
	var addToCartButtons = document.querySelectorAll('.add-cart-btn');
    addToCartButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();  
            var item_id = this.getAttribute('data-item-id')
            addToCart(item_id)
        })
    })
	
	var deleteCartButtons = document.querySelectorAll('.del-cart-btn');
	if(deleteCartButtons){
		deleteCartButtons.forEach(function(button) {
			button.addEventListener('click', function(event) {
				event.preventDefault();  
				var order_id = this.getAttribute('data-order-id')
				deleteCart(order_id)
			})
		})
	}
	
	var quantity = document.querySelectorAll('.quantity-btn')
	if(quantity){
		quantity.forEach(function(button) {
		  button.addEventListener('click', function(event) {
			var action = null
			var order_id = this.getAttribute('data-order-id')
			if (event.target.classList.contains('decrease')) {
				action='decrease'
				}
			if (event.target.classList.contains('increase')) {
				action='increase'
			}
			fetch("quantity-cart/", {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrftoken
				},
				body: JSON.stringify({
					"order_id": order_id,
					"action": action
				})
			})
			.then(response => response.json())
			.then(data => {
				document.querySelector(`[data-order-id="${order_id}"].item-quantity`).textContent = data["quantity"]
			})
			.catch(error => console.log(error))
		  })
		})
	}
	
	var confCartButtons = document.querySelectorAll('.conf-cart-btn')
	if(confCartButtons){
		confCartButtons.forEach(function(button) {
			button.addEventListener('click', function(event) {
				event.preventDefault();  
				var order_id = this.getAttribute('data-order-id')
				var stripe_id = this.getAttribute('data-stripe-id')
				var quantity = document.querySelector(`.item-quantity[data-order-id="${order_id}"]`).textContent
				var ordersData = [{
					"order_id": order_id,
					"quantity": quantity,
					"stripe_id": stripe_id
				}]
				confCart(ordersData)
			})
		})
	}
	
	var confCartGeneral = document.querySelector('.conf-cart-gen')
	if(confCartGeneral){
		confCartGeneral.addEventListener('click', function() {
			var ordersData = []
			var prodElements = document.querySelectorAll('.prod');
			prodElements.forEach(function(prodElement) {
				var orderID = prodElement.getAttribute('data-order-id');
				var quantity = prodElement.querySelector('.item-quantity').innerText;
				var stripeID = prodElement.querySelector('.conf-cart-btn').getAttribute('data-stripe-id');
				ordersData.push({
					"order_id": orderID,
					"quantity": quantity,
					"stripe_id": stripeID
				});
			});
			confCart(ordersData)
		})
	}
	
	function addToCart(item_id) {
		fetch("/add-cart/", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({'item_id': item_id})
		})
		.then(response => response.json())
		.then(data => console.log("added"))
		.catch(error => console.log(error))
	}
	
	function deleteCart(order_id) {
		let del_ord = document.getElementById(`${order_id}`)
		fetch("/del-cart/", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({'0': order_id})
		})
		.then(response => {
			if (response.ok) {
				window.location.reload()
			} else {
				console.log("Failed to remove order");
			}
		})
		.catch(error => console.error("Error:", error));
	}
	
	async function confCart(orders) {
		const response = await fetch("purchase/", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify(orders)
		})
		const { clientSecret } = await response.json()
		let checkout = await stripe.initEmbeddedCheckout({
			clientSecret,
		});
		checkout.mount('#checkout')
		let stp_close = document.getElementById("close-stp")
		stp_close.classList.remove("hidden")
		stp_close.addEventListener("click",()=>{
			checkout.destroy()
			stp_close.classList.add("hidden")
			checkout = null;
		})
	}
	
	let details = document.querySelectorAll('.detail')
	if(details){
		details.forEach((detail)=>{
			detail.addEventListener("click", ()=>{
				let id = detail.parentElement.getAttribute('data-item-id')
				fetch(`detail-prod/${id}`)
				.then(response => window.location.href = `/detail-prod/${id}`)
			})
		})
	}
	
	let planButtons = document.querySelectorAll('.plan-btn')
	if(planButtons){
		planButtons.forEach(function(button) {
			button.addEventListener('click', function(event) {
				event.preventDefault();  
				let id = this.getAttribute('data-stripe-id')
				let email = this.getAttribute('data-email')
				let order = {
					"id": id,
					"email": email,
				}
				confPlan(order)
			})
		})
	}
	
	async function confPlan(order) {
		const response = await fetch(window.location.href, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify(order)
		})
		const { clientSecret } = await response.json()
		let checkout = await stripe.initEmbeddedCheckout({
			clientSecret,
		});
		checkout.mount('#checkout')
		let stp_close = document.getElementById("close-stp")
		stp_close.classList.remove("hidden")
		stp_close.addEventListener("click",()=>{
			checkout.destroy()
			stp_close.classList.add("hidden")
			checkout = null;
		})
	}

	let refundButtons = document.querySelectorAll('.refund-btn')
	if(refundButtons){
		refundButtons.forEach(function(button) {
			button.addEventListener('click', function(event) {
				event.preventDefault();  
				let pi = this.getAttribute('data-pi')
				let order = {
					"pi": pi,
				}
				confRefund(order)
			})
		})
	}
	
	async function confRefund(order) {
		await fetch("refund/", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify(order)
		})
		.then(resp=>{})
	}
}) 