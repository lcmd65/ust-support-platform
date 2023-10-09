const item = document.querySelectorAll(".pure-link-tree");
const root_space = document.querySelector(".request-item-view");
const form_request = document.createElement("form");
form_request.classList.add(".new");

item.addEventListener("click", function itemClick(event) {
    fetch("/user_api", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            data = json.parse(data)
            for (let i = 0; i < data.length; i++)
                if (data["_id"] = id) {
                    const subjectInfo = data["subject"]
                    const questionInfo = data["request"]
                    const respone = data["respone"]
                    const workspace_item = document.createElement("div")
                    workspace_item.classList.add(".item-")
                }
        });
});

function selectItemRequest() {
    return item;
}

function eventView() {
    key
}