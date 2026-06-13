'use strict';

const apiBaseUrl = "http://localhost:8000/api";

class DataManager {
    constructor() {
        this.abortController = null;
    }

    async promptRequest(prompt) {
        this.abortController = new AbortController();

        try {
            const response = await fetch(`${apiBaseUrl}/prompt`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: prompt
                }),
                signal: this.abortController.signal
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const responseJson = await response.json();

            if (
                responseJson &&
                typeof responseJson.answer === "string"
            ) {
                return responseJson;
            }

            throw new Error("Invalid response format");
        } finally {
            this.abortController = null;
        }
    }

    isReady() {
        return this.abortController === null;
    }

    cancelRequest() {
        this.abortController?.abort();
    }
}

export const dataManagerInstance = new DataManager();