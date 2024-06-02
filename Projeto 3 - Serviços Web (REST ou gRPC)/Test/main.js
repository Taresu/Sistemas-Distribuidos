document.addEventListener("DOMContentLoaded", () => {
    const itemsList = document.getElementById('items');

    function fetchItems() {
        fetch('/items')
            .then(response => response.json())
            .then(data => {
                itemsList.innerHTML = '';
                data.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = `${item.name}: ${item.description}`;
                    itemsList.appendChild(li);
                });
            });
    }

    const eventSource = new EventSource('/stream');
    eventSource.onmessage = function(event) {
        console.log(event);
        fetchItems();
    };

    fetchItems();
});