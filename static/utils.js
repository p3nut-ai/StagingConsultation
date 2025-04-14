
const dateInput = document.getElementById("date");
dateInput.min = new Date().toISOString().split("T")[0];
dateInput.addEventListener("change", () => {
  if (new Date(dateInput.value) < new Date(dateInput.min)) {
    dateInput.value = ""; // Clear the invalid date
  }
});



document.addEventListener('DOMContentLoaded', function() {
  const scheduleCards = document.querySelectorAll('.schedule-card');
  const modalDay = document.querySelector('#default-modal input#modal_day');
  const modalTime = document.getElementById('modal_time');
  scheduleCards.forEach(card => {
    card.addEventListener('click', function() {
      scheduleCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      const day = card.getAttribute('data-day');
      const startTime = card.getAttribute('data-start-time');
      const endTime = card.getAttribute('data-end-time');
      modalDay.value = day;
      modalTime.value = startTime + "-" + endTime;
    });
  });



  

  /* 
    TODO: create function that adds active class pag pinindot 
    
  */

  // faq edit
  const faqCards = document.querySelectorAll('.faq-card');
  const FaqModalTitle = document.getElementById('edit_faq_title');
  const FaqModalDescription = document.getElementById('edit_faq_description');
  faqCards.forEach(card => {
    card.addEventListener('click', function() {
      faqCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');

      // get FAQ title and description
      const FaqTitle = card.getAttribute('data-faq-title');
      const FaqDescription = card.getAttribute('data-faq-description');
    
      FaqModalTitle.value = FaqTitle;
      FaqModalDescription.value = FaqDescription;
    });
  });

});



/*

FAQ: EDIT AND DELETE FUNCTIONS

*/

function deleteFAQ() {
  const FaqId = document.querySelector('.faq-card.active').getAttribute('data-faq-id');
  
  console.log("FAQ ID" + FaqId);
  
  fetch(`/delete_faq/${FaqId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ id: FaqId }),
  })
    .then(response => {
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return response.json();
      } else {
        // If not JSON, handle it as text (or perform a redirect)
        return response.text();
      }
    })
    .then(data => {
      location.reload();

    })
    .catch(error => {
      console.error('Error:', error);
    });
  
}


function editFAQ() {
  const faqCard = document.querySelector('.faq-card.active');
  if (!faqCard) {
    alert('No schedule selected!');
    return;
  }
  const FaqId = faqCard.getAttribute('data-faq-id');
  const updatedFaqTitle = document.querySelector('#faq-modal input#edit_faq_title').value;
  const updatedFaqDescription = document.getElementById('edit_faq_description').value;


  fetch(`/edit_faq/${FaqId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: updatedFaqTitle,
      description: updatedFaqDescription
    }),
  }).then(response => {
    if (!response.ok) {
      return response.json().then(errorData => {
        throw new Error(errorData.message || 'Something went wrong');
      });
    }
    return response.json();
  }).then(data => {
    location.reload();
    localStorage.setItem('scheduleEditSuccess', 'true');
  });
}


// alam mo na yan bossing
function deleteSched() {
  const scheduleId = document.querySelector('.schedule-card.active').getAttribute('data-schedule-id');
  console.log(scheduleId);
  fetch(`/delete_sched/${scheduleId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: scheduleId
    }),
  }).then(response => {
    if (!response.ok) { // Check if the response is OK
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse JSON response
  }).then(data => {
    // alert(data.message); // Alert the success message from the JSON response
    location.reload(); // Reload the page to reflect changes
  }).catch(error => {
    alert('Error deleting the schedule. Please try again.');
  });
}

function editSchedule() {
  const scheduleCard = document.querySelector('.schedule-card.active');
  if (!scheduleCard) {
    alert('No schedule selected!');
    return;
  }
  const scheduleId = scheduleCard.getAttribute('data-schedule-id');
  const updatedDay = document.querySelector('#default-modal input#modal_day').value;
  const updatedTime = document.getElementById('modal_time').value;
  const timeArray = updatedTime.split('-');
  console.log(scheduleId);
  // Extract the start time and end time
  const startTime = timeArray[0].trim(); // "10:00 AM"
  const endTime = timeArray[1].trim(); // "01:30 PM"
  fetch(`/edit/${scheduleId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      day: updatedDay,
      timeStart: startTime,
      timeEnd: endTime
    }),
  }).then(response => {
    if (!response.ok) {
      return response.json().then(errorData => {
        throw new Error(errorData.message || 'Something went wrong');
      });
    }
    return response.json();
  }).then(data => {
    location.reload();
    localStorage.setItem('scheduleEditSuccess', 'true');
  }).catch(error => {
    const statusCode = error;
    if (statusCode.message === "The date cannot be set to a past date") {
      console.log("tangina");
      warning_alert = document.getElementById('alert_box_warning').classList;
      warning_alert.remove('hidden');
      setTimeout(() => {
        warning_alert.add('hidden'); // Hide the alert
      }, 4000);
    } else if (statusCode.message === "Failed to edit the schedule") {
      error_alert = document.getElementById('alert_box_error').classList;
      error_alert.remove('hidden');
      setTimeout(() => {
        error_alert.add('hidden'); // Hide the alert
      }, 4000);
    } else {}
  });
}
window.onload = () => {
  success_alert = document.getElementById('alert_box_success').classList;
  // Check if success flag is set in localStorage
  if (localStorage.getItem('scheduleEditSuccess') === 'true') {
    success_alert.remove('hidden'); // Show the success alert
    // Hide the alert after 4 seconds
    setTimeout(() => {
      success_alert.add('hidden'); // Hide the alert
      localStorage.removeItem('scheduleEditSuccess'); // Clear the success flag
    }, 4000);
  }
};
// Toggle theme
// Light/Dark Mode Toggle
const themeToggle = document.getElementById('theme-toggle');
const htmlElement = document.documentElement;
if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    if (htmlElement.classList.contains('dark')) {
      htmlElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    } else {
      htmlElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    }
  });
  // Persist theme on page reload
  if (localStorage.getItem('theme') === 'dark') {
    htmlElement.classList.add('dark');
  } else {
    htmlElement.classList.remove('dark');
  }
} else {
  console.warn("Theme toggle button not found.");
}






