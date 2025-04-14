AOS.init();
    const dateInput = document.getElementById("date");
    const new_form = document.getElementById('new_consultation_form');
    dateInput.min = new Date().toISOString().split("T")[0];
    dateInput.addEventListener("change", () => {
      if (new Date(dateInput.value) < new Date(dateInput.min)) {
        dateInput.value = ""; // Clear the invalid date
      }
    });

    function review_form() {
      sessionStorage.setItem("reviewed_form", "true");
      // new_form.submit();
    }
    document.addEventListener('DOMContentLoaded', function() {
      if (sessionStorage.getItem("reviewed_form") === "true") {
        const alertBox = document.getElementById("alert_box_success");
        alertBox.classList.remove("hidden");
        setTimeout(() => {
          alertBox.classList.add("hidden");
          console.log('first');
        }, 4000);
        sessionStorage.removeItem("reviewed_form");
      }
      // JavaScript to toggle FAQ visibility
      document.getElementById("assistantButton").addEventListener("click", function(event) {
        const faqSection = document.getElementById("faqSection");
        const button = document.getElementById("assistantButton");
        faqSection.classList.toggle("hidden");
        let img = document.createElement('img');
        img.src = "/static/wave.svg";
        img.classList.add("w-8");
        img.classList.add("h-[12]");
        // Toggle the text of the button
        if (faqSection.classList.contains("hidden")) {
          button.textContent = "";
          button.appendChild(img);
        } else {
          button.textContent = "Hide FAQs"; // Button text when FAQs are visible
        }
        event.stopPropagation(); // Prevents click event from propagating to document
      });
      const splashScreen = document.getElementById("splash-screen");
      if (sessionStorage.getItem("splashShown") === "true") {
        splashScreen.classList.add("hidden");
      } else {
        setTimeout(() => {
          if (splashScreen) {
            splashScreen.classList.add("fade-out");
            setTimeout(() => {
              splashScreen.classList.add("hidden");
              sessionStorage.setItem("splashShown", "true");
            }, 1000);
          }
        }, 2000);
      }
    });