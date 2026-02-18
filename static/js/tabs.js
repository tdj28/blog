document.addEventListener("DOMContentLoaded", function () {
    const tabContainers = document.querySelectorAll(".code-tabs");

    tabContainers.forEach((container) => {
        const tabs = container.querySelectorAll(".code-tab");
        if (tabs.length === 0) return;

        // Create header container
        const header = document.createElement("div");
        header.className = "code-tabs-header";

        tabs.forEach((tab, index) => {
            const title = tab.getAttribute("data-title");
            const button = document.createElement("button");
            button.textContent = title;
            button.className = "tab-button";
            if (index === 0) {
                button.classList.add("active");
                tab.classList.add("active");
            }

            button.addEventListener("click", () => {
                // Deactivate all
                header.querySelectorAll(".tab-button").forEach((b) => b.classList.remove("active"));
                tabs.forEach((t) => t.classList.remove("active"));

                // Activate clicked
                button.classList.add("active");
                tab.classList.add("active");
            });

            header.appendChild(button);
        });

        // Insert header before the first tab
        container.insertBefore(header, tabs[0]);
    });
});
