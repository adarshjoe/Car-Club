        const razorpayKey = 'rzp_test_AlrgvTMPmpzG2J';

        // Function to handle the payment
        const initPayment = (amount,description,oid,page) => {
            const options = {
                key: razorpayKey,
                amount: amount*100, // Amount in paise (e.g., 1000 paise = ₹10)
                currency: "INR",
                name: "Car Club",
                description: description,
                image: "http://127.0.0.1:8000/static/template/themes/images/carcare.png", // URL to your store's logo
                handler: function(response) {
                    // This function will be called after payment is successful
                    alert("Payment successful! Payment ID: " + response.razorpay_payment_id);
                    window.location='/payForOrderAction?order_id='+oid+'&amount='+amount+'&orderpage='+page;
                }
            };

            const rzp = new Razorpay(options);
            rzp.open();
        };