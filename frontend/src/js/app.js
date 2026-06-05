'use strict';

import DataManager from "./datamanager.js";

window.onload = function() {
    const dataManager = new DataManager();

    const form = document.getElementById("prompForm");
    const input = document.getElementById("queryInput");
    const responseContainer = document.getElementById("responseContainer");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const prompt = input.value;
        try {
            const data = await dataManager.promptRequest(prompt);
            responseContainer.textContent = JSON.stringify(data, null, 2);
            responseContainer.classList.remove("text-danger");
        } catch (error) {
            responseContainer.textContent = "Error: " + error.message;
            responseContainer.classList.add("text-danger");
        }
    });
};