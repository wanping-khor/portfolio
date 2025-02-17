document.addEventListener("alpine:init", () => {
    Alpine.data("buttonActions", () => ({
        hireMe() {
            alert("Hire request sent!");
        },
        connect() {
            alert("Connected!");
        }
    }));
});
