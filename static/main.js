const taskForm = document.querySelector("form");
const appHeader = document.querySelector("header");
const taskContainer = document.querySelector(".tasks");
const tasks = document.querySelectorAll(".task");
const noTaskContainer = document.querySelector(".notasks");
const countContainer = document.querySelector(".count");
const deleteButtons = document.querySelectorAll(".delete-btn");
const taskIds = document.querySelectorAll(".id");
const updateModal = document.querySelector("#update");
const updateButtons = document.querySelectorAll(".update-btn");
const updateForm = document.querySelector("#form-update");
const notificationModal = document.querySelector(".noti-modal");
const message = document.querySelector(".message");
const loadingSpinner=document.querySelector('.loading');

let p = document.createElement("p");

p.classList.add("count-all");
p.innerText = `Tasks: ${tasks.length}`;

countContainer.appendChild(p);

window.onload = function () {
  scrollWindow();
};

function scrollWindow() {
  if (document.documentElement.scrollTop > 100) {
    appHeader.style.backgroundColor = "dodgerblue";
  }
}

function closeModal(id) {
  let el = document.getElementById(id);

  el.style.display = "none";
}

if (tasks.length == 0) {
  noTaskContainer.style.display = "block";
} else if (tasks.length > 0) {
  noTaskContainer.style.display = "none";
}

//ading a task
taskForm.addEventListener("submit", (e) => {
  noTaskContainer.style.display = "none";
  let taskData = new FormData(taskForm);

  let new_task = {
    name: taskData.get("name"),
    description: taskData.get("description"),
  };

  let API_URL = `/api/tasks`;

  fetch(API_URL, {
    body: JSON.stringify(new_task),
    method: "POST",
    headers: { "content-type": "application/json" },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      let html = `
                <h3 class="task-name">
                    ${data.task.name}
                </h3>
                <p class="task-desc">
                   ${data.task.description}
                </p>
                <a href="#" class="delete-btn"><i class="fa fa-trash" aria-hidden="true"></i></a>
                <a href="#" class="update-btn"><i class="fa fa-pen" aria-hidden="true"></i></a>
            `;
      let newTask = document.createElement("div");

      newTask.classList.add("task");

      newTask.innerHTML = html;
      loadingSpinner.style.display="block";
      
     


      setTimeout(() => {
        taskContainer.insertBefore(newTask, taskContainer.childNodes[0]);
        loadingSpinner.style.display="none"
      }, 1800);

      setTimeout(() => {
        location.reload();
      }, 2000);
      
    });

  taskForm.reset();
  e.preventDefault();
});

//deleting a task
for (let i = 0; i < tasks.length; i++) {
  deleteButtons[i].addEventListener("click", () => {
    let RESOURCE_URL = `/api/task/${taskIds[i].innerText}`;

    fetch(RESOURCE_URL, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((data) => {
        notificationModal.style.display = "block";
        message.innerText = data.message;
        tasks[i].style.display = "none";
        setTimeout(() => {
          location.reload();
        }, 2000);
      });
  });
}

//display update form with data
for (let i = 0; i < tasks.length; i++) {
  updateButtons[i].addEventListener("click", () => {
    let RESOURCE_URL = `/api/task/${taskIds[i].innerText}`;
    updateModal.style.display = "block";

    fetch(RESOURCE_URL, { method: "GET" })
      .then((res) => res.json())
      .then((data) => {
        document.querySelector("#update-name").value = data.task.name;
        document.querySelector("#update-desc").value = data.task.description;
      });


      updateForm.addEventListener("submit", (e) => {
        let RESOURCE_URL = `/api/task/${taskIds[i].innerText}`;
    
        let updatedData = new FormData(updateForm);
    
        let updatedTask = {
          name: updatedData.get("name"),
          description: updatedData.get("description"),
        };
        updateModal.style.display = "none";
        fetch(RESOURCE_URL, {
          method: "PUT",
          headers: { "content-type": "application/json" },
          body: JSON.stringify(updatedTask),
        })
          .then((res) => res.json())
          .then((data) => {
            notificationModal.style.display = "block";
            message.innerText = data.message;
    
            setTimeout(() => {
              location.reload();
            }, 3000);
          });
    
        e.preventDefault();
      });
  });
}



