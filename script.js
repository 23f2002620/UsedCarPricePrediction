

document.getElementById("priceForm").addEventListener("submit", async function(event) {
  event.preventDefault();

  // Collect the form data
  const make = document.getElementById("make").value;
  const model = document.getElementById("model").value;
  const year = document.getElementById("year").value;
  const mileage = document.getElementById("mileage").value;
  const fuelType = document.getElementById("fuel-type").value;
  const ownerType = document.getElementById("owner-type").value;

  // Create the JSON object to send
  const carData = {
      make: make,
      model: model,
      year: year,
      mileage: mileage,
      "fuel-type": fuelType,
      "owner-type": ownerType
  };

  try {
      // Send the POST request to the backend
      const response = await fetch('http://127.0.0.1:5000/predict', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(carData)
      });

      // Check for successful response
      if (response.ok) {
          const result = await response.json();
          document.querySelector(".prediction-result").innerText = `Predicted Price: ₹${result.predicted_price}L`;
      } else {
          throw new Error('Failed to fetch prediction');
      }
  } catch (error) {
      console.error('Error:', error);
      document.querySelector(".prediction-result").innerText = `Error: ${error.message}`;
  }
});
