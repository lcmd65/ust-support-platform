const item = document.querySelectorAll(".pure-link-tree");

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
            idata[]

        });
});

function selectItemRequest() {
    return item;
}

function eventView() {
    key
}